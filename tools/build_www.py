import base64,hashlib,json,os,re,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS=[a for a in sys.argv[1:] if not a.startswith('--')]
TESTER='--tester' in sys.argv
SRC=ARGS[0] if ARGS else os.path.join(ROOT,'src','lumi.html')
FONTS=os.path.join(ROOT,'src','fonts')
h=open(SRC,encoding='utf-8').read()
def ff(fam,w,f):
  b=base64.b64encode(open(os.path.join(FONTS,f),'rb').read()).decode()
  return f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b}) format('woff2')}}"
fonts='<style>'+''.join([ff('Grandstander',600,'grandstander-latin-600-normal.woff2'),ff('Grandstander',800,'grandstander-latin-800-normal.woff2'),
  ff('Atkinson Hyperlegible',400,'atkinson-hyperlegible-latin-400-normal.woff2'),ff('Atkinson Hyperlegible',700,'atkinson-hyperlegible-latin-700-normal.woff2')])+'</style>'
h=re.sub(r'<link rel="preconnect"[^>]*>\s*','',h)
h=re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>',fonts,h)
title=re.search(r'<title>.*?</title>',h).group(0);h=h.replace(title,'',1)
ver=hashlib.sha1(h.encode()).hexdigest()[:10]
head=f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
{title}
<meta name="theme-color" content="#8b5cf6">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Lumi">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>[hidden]{{display:none!important}}html,body{{background:#fff8ef}}</style>
</head>
<body>
'''+('<script>window.LUMI_TESTER=1</script>\n' if TESTER else '')
tail=f'''
<script>
(function(){{var nat=window.Capacitor&&window.Capacitor.isNativePlatform&&window.Capacitor.isNativePlatform();
if(!nat&&'serviceWorker' in navigator&&/^https?:/.test(location.protocol)){{window.addEventListener('load',function(){{navigator.serviceWorker.register('sw.js?v={ver}').catch(function(){{}});}});}}}})();
</script>
</body>
</html>
'''
out=os.path.join(ROOT,'www');os.makedirs(out,exist_ok=True)
open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(head+h+tail)
man={"name":"Lumi · Aprende jugando","short_name":"Lumi","description":"App educativa bilingüe para niños de 1.5 a 3 años","lang":"es","start_url":"./","scope":"./","display":"fullscreen","orientation":"any","background_color":"#efe7ff","theme_color":"#8b5cf6",
 "icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
          {"src":"icons/maskable-192.png","sizes":"192x192","type":"image/png","purpose":"maskable"},{"src":"icons/maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]}
open(os.path.join(out,'manifest.webmanifest'),'w',encoding='utf-8').write(json.dumps(man,ensure_ascii=False,indent=1))
sw=f'''const CACHE='lumi-{ver}';
const FILES=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png','./icons/maskable-192.png','./icons/maskable-512.png','./icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()));}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));}});
self.addEventListener('fetch',e=>{{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);if(u.origin!==location.origin)return;
  if(e.request.mode==='navigate'){{e.respondWith(fetch(e.request).then(r=>{{const c=r.clone();caches.open(CACHE).then(x=>x.put('./index.html',c));return r;}}).catch(()=>caches.match('./index.html')));return;}}
  e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request)));
}});
'''
open(os.path.join(out,'sw.js'),'w',encoding='utf-8').write(sw)
print('www listo',ver,len(head+h+tail))
