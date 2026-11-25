# Informe de migración — ctctelecom.mx (corporativo)

**Fecha:** 24 de noviembre de 2026
**Base:** build estático de Next.js en `..\ctctelecom.mx` (197 archivos, 24 rutas)
**Resultado:** proyecto Hugo en `ctc-hugo\` con 23 páginas + `404.html`
**Estado:** revisado y compilado. **No se modificó ni se subió nada del sitio actual.**

---

## 1. Resumen

Se reconstruyó el sitio completo sobre Hugo conservando el diseño, los textos y las URLs, y se
corrigió la capa SEO que hoy está ausente. El sitio pasa de **~1 MB de JavaScript por visita a 0 KB**,
y de **9 páginas sin ningún enlace interno a 0**.

Verificación ejecutada sobre el build final:

```
paginas: 23
huerfanas (0 enlaces internos): []
enlaces internos rotos: []
enlaces a assets inexistentes: []
sitemap urls: 23
PROBLEMAS: 0        (canonical, OG, Twitter, JSON-LD, h1 único)
```

---

## 2. Lo que quedó idéntico

| Elemento | Estado |
|---|---|
| URLs | Las 23 rutas, con barra final (`/datos/`, `/telefonia/`, …) |
| Diseño | Mismo CSS compilado de Tailwind (67 KB) + mismos componentes y clases |
| Textos | Migrados carácter por carácter; los textos legales regulados no se reescribieron |
| Imágenes y video | Los 38 assets referenciados (100 MB), mismos nombres y rutas |
| Header y footer | Mismo marcado, misma jerarquía visual |
| Botón de WhatsApp flotante | Igual (unificado a **55 1033 2515**) |
| Anclas de sección | Conservadas (`/datos/#internet-dedicado`, `#sdn`, `#mpls`, …) |
| Tipografía | Montserrat desde Google Fonts, mismos pesos |

Comparado visualmente contra producción (`/`, `/integracion/`, `/aviso-de-privacidad/`) a 1440 px y
390 px: la diferencia es solo la navegación de servicios (ver 3.1).

---

## 3. Cambios aplicados

### 3.1 El menú "Servicios" ahora sí existe en el HTML

Antes: `Servicios` era un `<button>` de Radix que dibujaba el submenú con JavaScript. En el HTML que
recibe Google **no había ni un solo enlace** a los servicios, por eso esas páginas no se rastreaban.

Ahora: `<details>` + CSS puro, con los 6 servicios y sus 25 anclas como enlaces reales
(`data/servicios.yaml`). Se abre sin JavaScript y funciona con teclado y en móvil.

### 3.2 Enlazado interno: de 9 huérfanas a 0

Se agregó una fila "Servicios" en el footer (sin alterar la retícula de 4 columnas) y se añadieron
`Tarifas IFT`, `Test de velocidad` y `Contrato de adhesión` a la lista de enlaces existente.

| Página | Antes | Ahora |
|---|---|---|
| `/datos/`, `/telefonia/`, `/data-center/`, `/infraestructura/`, `/integracion/`, `/carrier-interconnection/` | 0 enlaces internos | 23 (menú + footer) |
| `/contrato-de-adhesion/`, `/tarifas-ift/`, `/test-de-velocidad/` | 0 | 23 |

### 3.3 Metadatos SEO en las 23 páginas

Nuevo en cada página:

- `<link rel="canonical">` absoluto
- Open Graph completo (11 etiquetas) + imagen 1200×630 generada (`/assets/og/ctc-telecom-1200x630.png`)
- Twitter Card `summary_large_image`
- `hreflang` `es-MX` y `x-default`
- **2 o 3 bloques JSON-LD**: `Organization` en todas; `BreadcrumbList` en las internas; `WebSite` en la
  portada; y `Service` + `OfferCatalog` (con las secciones y anclas) en las 6 páginas de servicio
- `robots` con `max-image-preview:large`; `noindex` solo en el 404

### 3.4 Títulos y descripciones corregidos

Antes: 17 de 24 títulos superaban los 60 caracteres y 22 repetían `CTC Telecom | … | CTC Telecom`.
Ahora: **máximo 56 caracteres**, sin duplicar la marca, y sin descripciones de más de 160.

| Ruta | Antes | Ahora |
|---|---|---|
| `/` | CTC Telecom &#124; Red Propia en México y Conectividad Regional (58) | CTC Telecom &#124; Red de Fibra Óptica Propia en México (50) |
| `/datos/` | CTC Telecom &#124; Datos - Internet Dedicado, SDN, MPLS y Lan To Lan &#124; CTC Telecom (77) | Datos: Internet Dedicado, MPLS y SD-WAN &#124; CTC Telecom (53) |
| `/infraestructura/` | CTC Telecom &#124; Infraestructura - Fibra Óptica y Cableado Estructurado &#124; CTC Telecom (82) | Infraestructura: Fibra, Cableado y CCTV &#124; CTC Telecom (53) |
| `/neutralidad-de-red/` | …Gestión y Administración de Tráfico &#124; CTC Telecom (84) | Neutralidad de Red &#124; CTC Telecom (32) |
| `/contrato-de-adhesion/` | *tenía el título y la descripción de la portada* | Contrato de Adhesión &#124; CTC Telecom (34) |
| `/politica-de-cookies/` | *tenía el título y la descripción de la portada* | Política de Cookies &#124; CTC Telecom (33) |

### 3.5 Acordeones que ahora sí tienen contenido

En el sitio anterior, los paneles "Beneficios", "Casos de uso", "¿Por qué con CTC Telecom?" y
"Plataformas tecnológicas" estaban **vacíos** en el HTML (React los llenaba al hacer clic).

Se extrajo su contenido del *payload* de React (`.txt`) y ahora está en el HTML, en `<details>`
nativos: **98 paneles con contenido (477 viñetas)**, sin JavaScript, abribles por Google y
accesibles por teclado.

### 3.6 Sitemap y robots

- `sitemap.xml` con las 23 URLs, prioridad y frecuencia (excluye `noindex`).
- `robots.txt` con `Allow: /`.
- Antes: ninguno de los dos existía.

### 3.7 Página 404

Antes: "404: This page could not be found." en inglés, sin menú, dentro del sitio indexable.
Ahora: `404.html` en español, con header, footer, enlaces a servicios y `noindex`.
La ruta `/404/` deja de existir como página indexable (es una página de error: es lo correcto).

### 3.8 Contadores de la portada

Antes la portada mostraba `0,000 KM`, `0 POPS` y `0.00% SLA` hasta que el JavaScript animaba los
números. Con JS desactivado (o antes de hidratar) quedaba en cero.

Ahora están fijos en el HTML con los valores reales del componente: **24,000 km**, **525 PoPs**,
**99.99% SLA**.

### 3.9 Test de velocidad

El widget nPerf se cargaba desde el componente React. Se reinsertó el *script* oficial de nPerf
(el mismo que ya usaba `/speedtest.html`) para que la herramienta funcione.

### 3.10 Rendimiento

| Métrica | Antes | Ahora |
|---|---|---|
| JavaScript | 1,014 KB (8 *chunks* en todas las páginas) | **0 KB** |
| Peticiones de JS por página | 6 | 0 |
| HTML promedio | 59 KB (máx. 150 KB) | 51 KB (máx. 115 KB) |
| CSS | 67 KB | 67 KB (+ 2 KB de correcciones) |
| Build | ~40 s (Next + export) | **~0.3 s** |

### 3.11 Medios completos y verificados

Se copiaron **todos** los medios que el build original usa, incluidos los que no están en atributos
`src`/`href` sino en estilos en línea o en el payload de React. Así aparecieron dos que faltaban:

| Archivo | Dónde se usa |
|---|---|
| `map.svg` | Fondo del mapa de red de la portada (`style="background-image:url(...)"`) |
| `FONDOCTC.jpg` | Fondo del hero de `/test-de-velocidad/` |

Verificación sobre el build final: **43 referencias distintas a `/assets` → 43 resueltas, 0 rotas**
(incluye `src`, `poster`, `url()` del CSS y estilos en línea). El script `tools/copiar_assets.py`
deja el paso reproducible.

> Nota importante para revisarlo: el sitio debe **servirse por HTTP** (`ver-sitio.cmd` /
> `ver-sitio.sh` / `hugo server`). Abrir `public/index.html` con doble clic deja la página sin CSS ni
> imágenes, porque las rutas son absolutas (`/assets/…`). No es un archivo faltante: es el protocolo
> `file://`. En el dominio publicado no ocurre.

---

## 4. Incidencias heredadas que conviene resolver (no se tocaron)

1. **El formulario de `/contacto/` no envía nada.** No tiene `action`, los campos no tienen `name` y
   no hay manejador. Quien lo llena no genera un lead. Requiere decidir destino: servicio de
   formularios (Formspree/Netlify Forms), endpoint propio o reemplazo por WhatsApp/teléfono.
2. **Looking Glass** muestra la interfaz pero no ejecuta consultas (era React + un endpoint que no
   existe en un export estático; probablemente tampoco funciona hoy en producción).
3. **Desbordamiento horizontal en móvil.** Verificado que el sitio **actual en producción** presenta
   el mismo problema a 390 px (el contenido se corta y el botón de menú queda fuera de pantalla).
   Es previo a esta migración; conviene revisarlo en dispositivo real y corregirlo en la fase 2.
4. **Peso de medios.** Se migraron los originales: 100 MB, con PNG/JPG sin redimensionar y 70 MB de
   video (uno de 41 MB). La fase 2 debería convertirlos a WebP/AVIF, generar `srcset` y recomprimir
   los MP4. Hugo ya trae ese pipeline, no requiere nada extra.
5. **Sin analítica ni Search Console.** No hay GA4, ni verificación de dominio, ni envío de sitemap.

---

## 5. Siguiente fase sugerida (en este orden)

1. **Desplegar** el build actual y comparar con producción URL por URL (30 min).
2. **Search Console + GA4 + Bing/IndexNow**, enviar `sitemap.xml` (1 h).
3. **Arreglar el formulario** de contacto y medir envíos (2 h).
4. **Optimizar medios**: WebP/AVIF + `srcset` + posters de video → de 100 MB a ~25 MB (3 h).
5. **Enriquecer contenido** de las páginas con menos de 250 palabras (soporte, tarifas IFT,
   manual de pagos, infografía) y agregar FAQ con `FAQPage` (1-2 días).
6. **Corregir el responsive móvil** y el menú (medio día).

---

## 6. Cómo revisarlo antes de publicar

El sitio necesita servirse por HTTP (las rutas son absolutas). Lo más rápido:

| Sistema | Acción |
|---|---|
| Windows | doble clic en **`ver-sitio.cmd`** |
| macOS / Linux | `chmod +x ver-sitio.sh` y luego `./ver-sitio.sh` |

Abre `http://localhost:8080` con el sitio completo (imágenes, CSS y navegación funcionando). También
sirve `hugo server` si ya tienes Hugo instalado.

---

## 7. Cómo revertir

Nada del sitio actual fue tocado. Para volver al estado anterior basta con seguir subiendo la
carpeta `..\ctctelecom.mx` por FTP como hasta hoy; el proyecto Hugo vive aparte, en `ctc-hugo\`.
