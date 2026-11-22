import re

FEAT = re.compile(r'cq[wh]|[ds]vh|clamp\(|min\(|max\(|env\(|^inset$')


def split_top(s, sep):
    out, depth, q, cur = [], 0, None, ''
    for ch in s:
        if q:
            cur += ch
            if ch == q:
                q = None
            continue
        if ch in '"\'':
            q = ch
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def repl_funcs(v):
    while True:
        m = re.search(r'\b(clamp|min|max|env)\(', v)
        if not m:
            return v
        i = m.end()
        depth, j = 1, i
        while j < len(v) and depth:
            depth += {'(': 1, ')': -1}.get(v[j], 0)
            j += 1
        args = [a.strip() for a in split_top(v[i:j - 1], ',')]
        f = m.group(1)
        if f == 'env':
            pick = args[1] if len(args) > 1 else '0px'
        elif f == 'clamp':
            pick = args[1] if len(args) == 3 else args[0]
            px = [re.fullmatch(r'(\d*\.?\d+)px', a) for a in (args[0], args[-1])]
            if len(args) == 3 and all(px):
                pick = f'{round((float(px[0].group(1)) + float(px[1].group(1))) / 2, 1)}px'
        else:
            pick = args[0]
        if re.search(r'\s[-+*/]\s', pick):
            pick = 'calc(' + pick + ')'
        v = v[:m.start()] + pick + v[j:]


def fix_value(v):
    v = repl_funcs(v)
    v = re.sub(r'(-?\d*\.?\d+)cq([wh])', r'calc(\1v\2 / var(--z,1))', v)
    v = re.sub(r'(\d*\.?\d+)[ds]vh', r'\1vh', v)
    return v


def fix_decls(body):
    out, changed = [], False
    for d in split_top(body, ';'):
        if ':' not in d:
            continue
        p, v = d.split(':', 1)
        p, v = p.strip(), v.strip()
        if p.startswith('--'):
            if FEAT.search(v):
                out.append(f'{p}:{fix_value(v)}')
                changed = True
            continue
        if p == 'inset' and '(' not in v:
            parts = v.replace('!important', '').split()
            t = parts + [parts[0]] * 4 if len(parts) == 1 else parts
            if len(parts) == 2:
                t = [parts[0], parts[1], parts[0], parts[1]]
            elif len(parts) == 3:
                t = [parts[0], parts[1], parts[2], parts[1]]
            imp = ' !important' if '!important' in v else ''
            out += [f'top:{fix_value(t[0])}{imp}', f'right:{fix_value(t[1])}{imp}', f'bottom:{fix_value(t[2])}{imp}', f'left:{fix_value(t[3])}{imp}']
            changed = True
        elif FEAT.search(v):
            out.append(f'{p}:{fix_value(v)}')
            changed = True
    return ';'.join(out), changed


def blocks(css):
    i, n = 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0:
            return
        pre = css[i:j].strip()
        depth, k = 1, j + 1
        q = None
        while k < n and depth:
            ch = css[k]
            if q:
                if ch == q:
                    q = None
            elif ch in '"\'':
                q = ch
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
            k += 1
        yield pre, css[j + 1:k - 1]
        i = k


def legacy(css):
    css = re.sub(r'/\*[\s\S]*?\*/', '', css)
    out = []
    for pre, body in blocks(css):
        if pre.startswith('@container') or pre.startswith('@font-face') or pre.startswith('@supports'):
            continue
        if pre.startswith('@media'):
            inner = legacy(body)
            if inner:
                out.append(f'{pre}{{{inner}}}')
        elif pre.startswith('@keyframes'):
            frames, any_c = [], False
            for fp, fb in blocks(body):
                nb, c = fix_decls(fb)
                any_c |= c
                rest = [d for d in split_top(fb, ';') if ':' in d and not FEAT.search(d.split(':', 1)[1]) and d.split(':', 1)[0].strip() != 'inset']
                frames.append(f'{fp}{{{";".join([x.strip() for x in rest] + ([nb] if nb else []))}}}')
            if any_c:
                out.append(f'{pre}{{{"".join(frames)}}}')
        elif not pre.startswith('@'):
            nb, c = fix_decls(body)
            if c:
                out.append(f'{pre}{{{nb}}}')
    return ''.join(out)


def wrap(css):
    l = legacy(css)
    return f'@supports not (width:1cqw){{{l}}}' if l else ''


if __name__ == '__main__':
    t = '.a{width:clamp(28px,7cqw,42px);inset:0;color:red}.b{left:calc(env(safe-area-inset-left,0px) / var(--z,1))}@media (max-width:5px){.c{height:100dvh}}@container lumi (max-width:3px){.d{width:3cqw}}@keyframes k{0%{transform:translateX(2cqw);opacity:0}to{opacity:1}}.e{--g:min(4cqw, 30px);gap:2px}'
    r = legacy(t)
    print(r)
    assert '.a{width:35.0px;top:0;right:0;bottom:0;left:0}' in r
    assert '.b{left:calc(0px / var(--z,1))}' in r
    assert '@media (max-width:5px){.c{height:100vh}}' in r
    assert '.d' not in r
    assert '@keyframes k{0%{opacity:0;transform:translateX(calc(2vw / var(--z,1)))}to{opacity:1}}' in r
    assert '.e{--g:calc(4vw / var(--z,1))}' in r
    print('ok')
