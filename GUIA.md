# Lumi · Guía para instalar, probar y publicar

Esta carpeta (`lumi-app`) es el proyecto completo de la app:

| Carpeta / archivo | Qué es |
|---|---|
| `www/` | La app ya lista (es lo que se instala en teléfonos y tablets). |
| `src/lumi.html` | El código fuente de la app. |
| `android/` | Proyecto Android (Capacitor). |
| `ios/` | Proyecto iPhone/iPad (Capacitor). |
| `.github/workflows/` | Robots de GitHub que compilan el APK y publican el enlace web solos. |
| `resources/` | Ícono y pantalla de inicio originales. |

Ya trae: voz nativa en Android/iPhone, compras dentro de la app (Premium), botón "atrás" de Android bloqueado para niños, funciona sin internet, íconos y pantalla de inicio.

---

## Paso 1 · El proyecto ya está en tu GitHub

Ya subí todo a **https://github.com/CarlosMonroy182/Lumi-App**. Cada vez que se actualiza, GitHub solo:
- compila el APK de Android y lo deja en un enlace de descarga directa;
- publica la versión web.

1. Abre **https://github.com/CarlosMonroy182/Lumi-App/actions** → verás **Android** y **Web**. Tardan ~5–10 min; al terminar tienen palomita verde ✅.
2. (Solo si el enlace web no abre después de 10 min) abre **https://github.com/CarlosMonroy182/Lumi-App/settings/pages** → en *Build and deployment* elige **Source: Deploy from a branch** → **Branch: gh-pages** / **(root)** → **Save**.

## Paso 2 · Probar en el teléfono de tu esposa y la tablet de tu hija

### Android (app real, recomendado)
Enlace de descarga directa (siempre la versión más nueva):

**https://github.com/CarlosMonroy182/Lumi-App/releases/download/apk-latest/Lumi.apk**

1. Abre ese enlace **en el teléfono/tablet** (mándatelo por WhatsApp).
2. Se descarga `Lumi.apk` → tócalo para abrirlo.
3. Android pedirá permiso para *instalar apps desconocidas* desde Chrome/WhatsApp → **Permitir** → regresa → **Instalar**.
4. Listo: aparece el ícono del elefante **Lumi**.
5. Recomendado para la niña: activa **Fijar aplicación** (Ajustes → Seguridad → *Fijar app / Screen pinning*) para que no pueda salirse.

Para actualizar después: abre el mismo enlace e instala encima (no hay que desinstalar).

### iPhone o cualquier teléfono (versión web instalable)
**https://carlosmonroy182.github.io/Lumi-App/**

- iPhone: ábrelo en **Safari** → botón **Compartir** → **Agregar a inicio**. Se abre en pantalla completa y funciona sin internet.
- Android también puede usarlo así (Chrome → menú ⋮ → **Instalar app**).

> Nota: en la versión web la compra de Premium no está disponible (solo en la app de la tienda). Para probar Premium usa *Configuración → Simular Premium*.

## Paso 3 · Versiones nuevas

Yo subo los cambios directo a tu repositorio; en ~10 minutos el enlace del APK y el web ya tienen la versión nueva. En el teléfono solo abre otra vez el enlace del APK e instala encima.

---

## Paso 4 · Plan de pago (Premium)

La app vende **un solo pago para siempre** llamado `lumi_premium` (tipo *no consumible*). El precio lo pones tú en cada tienda; la app lo lee y lo muestra solo.

- **Dónde compra el papá/mamá:** en la pantalla de inicio (botón ✦ Premium) o en Configuración → *Lumi Premium*. Siempre pide antes la suma de papás (exigido por Apple y Google para apps de niños).
- **Restaurar compras:** botón en las mismas pantallas (para cuando cambian de teléfono).
- En la app instalada desde la tienda desaparece el interruptor *Simular Premium*.

## Paso 5 · Publicar en Google Play

1. Crea tu cuenta de desarrollador: https://play.google.com/console (pago único de 25 USD).
2. **Llave de firma** (ya te la generé, viene en `Lumi-LLAVES-PlayStore.zip`, **guárdala y no la subas a GitHub**):
   - En GitHub: repo → **Settings → Secrets and variables → Actions → New repository secret**. Crea los 4 secretos que vienen en `LEEME-LLAVES.txt` (copiar y pegar).
   - En **Actions → Android → Run workflow**. Al terminar, en Releases aparece también **Lumi-PlayStore.aab**.
3. En Play Console: **Crear app** → nombre *Lumi* → App → Gratis.
4. **Público objetivo**: menores de 5 años → acepta la política de **Familias**. No tiene anuncios. *Seguridad de datos*: "No se recopilan datos" (todo se guarda en el teléfono).
5. **Política de privacidad**: Google la pide para apps de niños. Puede ser una página sencilla (te la redacto cuando quieras).
6. **Pruebas → Prueba interna** → sube `Lumi-PlayStore.aab` → agrega tu correo y el de tu esposa como testers.
7. **Monetizar → Productos → Productos integrados en la app → Crear producto**:
   - ID del producto: `lumi_premium` (exactamente así)
   - Nombre: Lumi Premium · Precio: el que decidan → **Activar**.
8. **Configuración → Pruebas de licencia**: agrega sus correos para comprar en modo prueba sin cobro real.
9. Cuando todo esté bien: **Producción → Crear versión** con el mismo `.aab` → enviar a revisión.

> El identificador de la app es `com.lumikids.aprende`. **No se puede cambiar** después de publicarla; si quieres otro, dímelo antes de subirla.

## Paso 6 · Publicar en App Store (iPhone/iPad)

Apple exige dos cosas que no se pueden evitar:
- **Cuenta Apple Developer** (99 USD al año): https://developer.apple.com/programs
- **Una Mac con Xcode** (o una Mac en la nube como Codemagic: https://codemagic.io — tiene minutos gratis).

En la Mac (te explico cada comando):
1. Instala **Xcode** desde la App Store de la Mac y **Node.js 22** desde https://nodejs.org
2. Copia la carpeta `lumi-app` a la Mac. Abre la app **Terminal** y escribe, uno por uno:
   - `cd ~/Downloads/lumi-app` → entra a la carpeta del proyecto.
   - `npm ci` → descarga las piezas del proyecto (tarda 1–2 min).
   - `npx cap sync ios` → copia la app al proyecto de iPhone.
   - `npx cap open ios` → abre el proyecto en Xcode.
3. En Xcode: clic en **App** (izquierda) → pestaña **Signing & Capabilities**:
   - **Team**: tu cuenta de Apple Developer.
   - **+ Capability → In-App Purchase**.
4. En https://appstoreconnect.apple.com: **Apps → + → Nueva app** (Bundle ID `com.lumikids.aprende`, categoría **Niños / Kids, 5 años o menos**).
   - **Monetización → Compras dentro de la app → +** → tipo **No consumible** → ID `lumi_premium` → precio.
5. En Xcode: menú **Product → Archive** → **Distribute App → App Store Connect → Upload**.
6. En App Store Connect → **TestFlight**: instálala en el iPhone de tu esposa con la app TestFlight para probar (las compras ahí son de prueba, sin cobro).
7. Cuando esté lista: **Enviar a revisión**.

---

## Si algo falla
- **Proceso rojo en Actions**: entra al proceso → paso en rojo → copia las últimas líneas y mándamelas.
- **La app se trabó**: Configuración (mantener presionado el engrane) → **Diagnóstico → Copiar** y mándamelo.
