# ctctelecom.mx — Sitio corporativo en Hugo

Reconstrucción del sitio corporativo de CTC Telecom (build de Next.js) sobre **Hugo**, con la misma
estructura visual, las mismas URLs y una capa SEO completa. Sin JavaScript de framework, sin npm,
sin dependencias: un binario y una carpeta de contenido.

- **URLs:** idénticas a las actuales, con barra final (`/datos/`, `/telefonia/`, …).
- **Peso:** 0 KB de JavaScript (antes ~1 MB en cada visita).
- **SEO:** canonical, Open Graph, Twitter Cards, JSON-LD, `sitemap.xml` y `robots.txt` en todas las páginas.

---

## Instalación de Hugo (una sola vez por equipo)

Se necesita **Hugo 0.158 o superior** (probado con 0.170.1). No hace falta la versión *extended*
(no usamos SCSS). Es un solo ejecutable: no hay `npm install` ni `node_modules`.

**Windows**

```powershell
winget install Hugo.Hugo          # o: scoop install hugo
hugo version                      # verificar
```

**macOS**

```bash
brew install hugo
hugo version
```

**Linux**

```bash
# opción recomendada: binario oficial (las versiones de los repos suelen ser viejas)
curl -LO https://github.com/gohugoio/hugo/releases/download/v0.170.1/hugo_0.170.1_linux-amd64.tar.gz
tar -xzf hugo_0.170.1_linux-amd64.tar.gz hugo
sudo install -m 755 hugo /usr/local/bin/hugo

# en ARM (Raspberry, servidores ARM) usa ..._linux-arm64.tar.gz
# alternativas: sudo snap install hugo   |   sudo apt install hugo   (revisa que sea >= 0.158)
hugo version
```

> En este equipo Windows ya hay una copia local del binario en `..\.tools\hugo\hugo.exe`.
> Si `hugo` no está en el PATH, usa esa ruta en lugar de `hugo` en todos los comandos de abajo.
> (Ese `.exe` no sirve en macOS/Linux: ahí instala Hugo con las instrucciones de arriba.)

---

## Comandos: ejecutar en local y compilar

Todos se ejecutan **dentro de esta carpeta** (`ctc-hugo`). Los mismos comandos funcionan igual en
Windows, macOS y Linux; solo cambia cómo se invoca el binario si no está en el PATH.

| Tarea | Comando |
|---|---|
| Servidor local con recarga automática | `hugo server` → http://localhost:1313 |
| Servidor visible desde el celular (misma red) | `hugo server --bind 0.0.0.0 --baseURL http://TU-IP-LOCAL:1313` |
| Compilar para publicar | `hugo --cleanDestinationDir` |
| Compilar y minificar HTML/CSS | `hugo --cleanDestinationDir --minify` |
| Compilar para un dominio de pruebas | `hugo --baseURL https://pruebas.ctctelecom.mx/` |
| Servir borradores (`draft: true`) | `hugo server -D` |
| Ver la versión del binario | `hugo version` |

El resultado de compilar queda en **`public/`**: eso es lo que se sube por FTP.
Build medido: **~300 ms** para las 23 páginas + `404.html`.

### Windows (PowerShell)

```powershell
cd C:\workspace\CTC-FTP\ctc-hugo

# con Hugo en el PATH
hugo server
hugo --cleanDestinationDir

# con el binario local de este equipo
..\.tools\hugo\hugo.exe server
..\.tools\hugo\hugo.exe --cleanDestinationDir
```

### macOS / Linux (bash o zsh)

```bash
cd ~/ruta/a/ctc-hugo

hugo server
hugo --cleanDestinationDir
# servidor accesible desde el teléfono:
hugo server --bind 0.0.0.0 --baseURL http://192.168.1.50:1313
```

Para detener el servidor: `Ctrl + C`.

---

## Verlo en local (con imágenes y estilos)

> ⚠️ **No abras `public/index.html` con doble clic.** Las rutas del sitio son absolutas
> (`/assets/...`, `/datos/`), así que el navegador las resuelve contra la raíz del disco
> (`file:///C:/assets/...`) y la página se ve **sin CSS y sin imágenes**. No es que falten los
> archivos: es que un sitio estático necesita servirse por HTTP. En producción esto no ocurre
> porque el dominio ya es la raíz.

La forma más simple, sin escribir comandos:

| Sistema | Qué hacer |
|---|---|
| **Windows** | Doble clic en **`ver-sitio.cmd`** |
| **macOS / Linux** | `chmod +x ver-sitio.sh` (una vez) y luego `./ver-sitio.sh` |

Ambos abren el navegador en **http://localhost:8080** y usan lo primero que encuentren:

1. `hugo` (si está en el PATH) → `hugo server`
2. el binario local `..\.tools\hugo\hugo.exe` (en este equipo Windows)
3. `python` / `python3` → `http.server` sobre la carpeta `public/` ya compilada

Opciones: `ver-sitio.cmd 9000` o `./ver-sitio.sh 9000` cambian el puerto, y `NO_OPEN=1` evita abrir
el navegador (útil en servidores o para pruebas automatizadas).

---

## Estructura

```
hugo.toml                 configuración (dominio, SEO, seguridad de contenido)
ver-sitio.cmd             lanzador local para Windows  (doble clic)
ver-sitio.sh              lanzador local para macOS / Linux
data/
  site.yaml               teléfonos, correo, dirección, redes sociales  ← editar aquí
  servicios.yaml          catálogo del menú de Servicios                ← editar aquí
layouts/
  _default/baseof.html    esqueleto HTML (head + header + footer + WhatsApp)
  _default/single.html    páginas normales
  _default/servicio.html  plantilla de las 6 páginas de servicio
  index.html              portada
  404.html                página de error
  sitemap.xml             sitemap filtrado (excluye noindex)
  partials/               head (SEO), header, footer, whatsapp, jsonld
content/
  _index.html             portada
  <slug>/index.html       páginas heredadas (18)
  <slug>/_index.md        servicios con datos estructurados (6)
static/
  assets/                 imágenes, video, CSS compilado + ctc.css
  robots.txt
tools/
  copiar_assets.py        copia desde ../ctctelecom.mx todo medio referenciado
  extraer_contenido.py    vuelve a extraer el contenido desde ../ctctelecom.mx
```

---

## Cómo hacer cambios (los 3 casos)

### 1. Cambiar un teléfono, correo o red social
Un solo archivo: [`data/site.yaml`](data/site.yaml). Se actualiza en el header, footer y botón de WhatsApp.

### 2. Editar una página legal o informativa
[`content/aviso-de-privacidad/index.html`](content/aviso-de-privacidad/index.html) y similares.
Es HTML semántico simple (`<h2>`, `<p>`, `<ul>`), sin clases raras. El título y la descripción SEO
están en el bloque `---` del inicio.

```html
---
title: "Aviso de Privacidad | CTC Telecom"
description: "Consulta el Aviso de Privacidad de CTC Telecom…"
---
<section class="py-20">…</section>
```

### 3. Editar una página de servicio (`/datos/`, `/integracion/`, …)
[`content/integracion/_index.md`](content/integracion/_index.md). **No es HTML**: es una ficha con
los datos de la página y la plantilla dibuja el diseño.

```yaml
hero:
  video: "/assets/soluciones-empresariales.mp4"
  title: "Empresariales"
  accent: "Soluciones"
  leads: ["Primer párrafo…", "Segundo párrafo…"]
sections:
  - id: "servidores"
    badge: "Cómputo de Misión Crítica"
    title: "Infraestructura"
    accent: "de Servidores"
    lead: "Descripción de la sección…"
    img: "/assets/servidoresdell-ibm.jpg"
    panels:
      - title: "Características clave"
        items:
          - "Un bullet"
          - "Otro bullet"
```

Para **agregar un servicio nuevo**: crea `content/<slug>/_index.md` con `layout: servicio`, copia la
estructura de otro servicio y agrega su entrada en [`data/servicios.yaml`](data/servicios.yaml) para
que aparezca en el menú. La URL `/slug/` queda lista automáticamente.

> Los acordeones usan `<details>` nativo: funcionan sin JavaScript, su contenido **sí** está en el
> HTML (Google lo lee) y el primero se abre por defecto, igual que antes.

---

## Regenerar el contenido desde el sitio original

Solo si se actualiza el export de Next.js en `../ctctelecom.mx`. Requiere Python 3.9+ con `lxml`
(`pip install lxml` / `pip3 install lxml`).

**Windows**

```powershell
python tools\copiar_assets.py
python tools\extraer_contenido.py
hugo --cleanDestinationDir
```

**macOS / Linux**

```bash
python3 tools/copiar_assets.py
python3 tools/extraer_contenido.py
hugo --cleanDestinationDir
```

`copiar_assets.py` recorre el build original y copia a `static/assets/` **todo** medio referenciado:
`<img src>`, `poster`, imágenes de fondo en estilos en línea (`background-image:url(...)`), `url()`
del CSS y las referencias del payload de React. Es idempotente: solo copia lo que falta o cambió.
Hoy reporta **39 archivos, 101.9 MB, 0 faltantes**.

`extraer_contenido.py` vuelve a leer cada `index.html` y `index.txt` (payload de React), extrae
textos y acordeones, y reescribe `content/`. Luego revisa el `git diff` antes de publicar.

---

## Despliegue

1. Compilar: `hugo --cleanDestinationDir`
2. Subir **el contenido de `public/`** por FTP a la raíz del dominio.
3. Verificar que el servidor sirva `index.html` en carpetas (`/datos/` → `/datos/index.html`) y
   que use `404.html` como página de error.

Si el FTP pide un archivo comprimido, se puede empaquetar `public/`:

```powershell
# Windows
Compress-Archive -Path public\* -DestinationPath deploy.zip -Force
```

```bash
# macOS / Linux
cd public && zip -r ../deploy.zip . && cd ..
```

> El `server.js` de la carpeta original solo sirve para probar en local; en producción es hosting
> estático.

---

## Pendientes conocidos (fuera del alcance de esta entrega)

| Tema | Estado |
|---|---|
| Formulario de `/contacto/` | **No envía** (heredado: sin `action`, sin `name` en los campos). Requiere servicio de formularios o integración con CRM. |
| Looking Glass | El widget era React; hoy muestra la interfaz pero no ejecuta consultas. Requiere endpoint. |
| Optimización de imágenes/video | Se migraron los originales (100 MB). Falta convertir a WebP/AVIF y recortar los videos (fase 2). |
| GA4 / Search Console | No existen. Falta crear propiedades y verificar el dominio. |
| Menú móvil / overflow horizontal | El sitio original ya lo presenta (verificado en producción). Conviene revisarlo en dispositivo real. |
