# Rendimiento — rama `feature/performance`

Trabajo de performance sobre el sitio Hugo, alineado con la **mejora 8** del análisis de HMV
Soluciones del 24-11-2026 («Optimizar imágenes y medir rendimiento»).

Resumen: **`public/` pasó de 103.3 MB a 37.1 MB** y la portada de **43.4 MB a 4.5 MB** de primera
carga, sin cambios visuales.

---

## 1. Punto de partida (rama `main`)

Medido con `python tools/peso.py` sobre el build de `main`:

| Página | HTML | Medios | Total |
|---|---:|---:|---:|
| `/` | 73 KB | 43,280 KB | **43.4 MB** |
| `/telefonia/` | 115 KB | 16,447 KB | 16.6 MB |
| `/data-center/` | 92 KB | 16,039 KB | 16.1 MB |
| `/infraestructura/` | 46 KB | 8,366 KB | 8.4 MB |
| `/nosotros/` | 37 KB | 8,366 KB | 8.4 MB |
| `/manual-de-pagos/` | 27 KB | 7,147 KB | 7.2 MB |

Causas:

- **Video**: 8 MP4 sumaban **65.7 MB**, con un solo fondo de portada de **41.2 MB** (2048×1162, 30 s).
- **Imágenes**: 39 archivos PNG/JPG de **35.1 MB**, varios de 4–7 MB servidos a tamaño completo.
- Sin `width`/`height` en las imágenes → *layout shift*.
- Sin variantes responsive ni WebP: el móvil descargaba la imagen de escritorio.

---

## 2. Resultado

| Métrica | Antes | Después | Δ |
|---|---:|---:|---:|
| `public/` completo | 103.3 MB | **37.1 MB** | −64 % |
| Portada (primera carga) | 43.4 MB | **4.5 MB** | −90 % |
| `/data-center/` | 16.1 MB | 2.7 MB | −83 % |
| `/telefonia/` | 16.6 MB | 1.4 MB | −92 % |
| `/manual-de-pagos/` | 7.2 MB | 0.9 MB | −87 % |
| Videos (8) | 65.7 MB | **8.2 MB** | −88 % |
| Imágenes originales (39) | 35.1 MB | **23.6 MB** | −34 % |
| Variantes WebP nuevas | — | 65 archivos / 2.7 MB | — |
| Posters de video | — | 8 archivos / 0.6 MB | — |

---

## 3. Qué se hizo

### 3.1 Videos (`tools/comprimir_videos.py`)

- Se escalan a **1280 px** de ancho máximo (son fondos decorativos detrás de un degradado).
- **H.264 CRF 30**, sin pista de audio (siempre van `muted`), `+faststart` para arrancar antes.
- Se genera un **poster JPEG** por video (primer fotograma) para que no haya hueco negro.
- El manifiesto `data/videos.yaml` guarda poster y dimensiones; lo consume la plantilla.

| Archivo | Antes | Después |
|---|---:|---:|
| `TELECOM-FONDO.mp4` | 41.2 MB | **3.8 MB** |
| `Banner-web-3.mp4` | 7.6 MB | 0.7 MB |
| `data-center-connectivity.mp4` | 7.1 MB | 1.6 MB |
| `soluciones-empresariales.mp4` | 3.3 MB | 0.7 MB |
| `soporte2.mp4` | 2.0 MB | 0.5 MB |
| `datos.mp4` | 1.8 MB | 0.4 MB |
| `telefonia.mp4` | 1.5 MB | 0.4 MB |
| `carrier-interconexion.mp4` | 1.2 MB | 0.2 MB |

Además todos los `<video>` llevan ya `poster` y `preload="none"`.

### 3.2 Imágenes (`tools/optimizar_imagenes.py`)

- Recompresión de los originales: máximo **1600 px** de ancho (JPEG q82 progresivo / PNG optimizado).
- **Variantes WebP** de 480 / 960 / 1600 px en `static/assets/opt/` (65 archivos, 2.7 MB).
- Manifiesto `data/medios.yaml` con dimensiones reales y variantes disponibles.

### 3.3 Markup (`layouts/partials/picture.html` + shortcode)

Cada imagen se emite como:

```html
<picture>
  <source type="image/webp" srcset="/assets/opt/foto-480.webp 480w, /assets/opt/foto-960.webp 960w" sizes="…">
  <img src="/assets/foto.jpg" alt="…" width="1536" height="1024" loading="lazy" decoding="async">
</picture>
```

Esto aporta:

- **WebP** para todos los navegadores actuales (≈30–60 % menos peso que JPEG/PNG) y respaldo al original.
- **`sizes`/`srcset`**: el móvil descarga la variante de 480 px, no la de 1600.
- **`width`/`height`**: reserva el espacio y elimina el *layout shift* (CLS).
- **`loading="lazy"`** en todo salvo la imagen principal; las de las secciones de servicio también.
- En el hero, la imagen (si la hubiera) va con `fetchpriority="high"`.

Desde el contenido se usa el shortcode:

```html
{{< picture src="/assets/foto.jpg" alt="Descripción" class="..." >}}
```

### 3.4 Otros ajustes

- **PeeringDB** pasó de `http://` a `https://www.peeringdb.com/net/41652` (mejora 6 del análisis).
- Las portadas de sección usan poster en vez de video a pantalla completa sin `poster`.

---

## 4. Cómo medir

```powershell
hugo --cleanDestinationDir
python tools\peso.py --top 12
```

```bash
hugo --cleanDestinationDir
python3 tools/peso.py --top 12
```

El script usa, para cada `<picture>`, la variante WebP más grande en lugar del original de respaldo,
así que el número se parece a lo que descarga un navegador moderno (no suma las dos).

Para Core Web Vitals reales hace falta el sitio desplegado: PageSpeed Insights o Lighthouse sobre
la URL publicada.

---

## 5. Pendiente en esta rama (siguiente iteración)

| Tema | Por qué |
|---|---|
| **Carga diferida del video del hero** | es el 80 % del peso de la portada; conviene cargarlo tras el primer render (IntersectionObserver) o servir un *still* en móvil con `prefers-reduced-data` |
| **Montserrat self-hosted + subset** | hoy son 2 conexiones a `fonts.googleapis.com` / `fonts.gstatic.com` que bloquean el render |
| **Cabeceras de caché y compresión** | depende del hosting; hay ejemplos en `docs/servidor/cache-y-compresion.md` |
| **Medición de campo** | GA4 + Search Console (mejora 15 del análisis) para saber si el cambio mueve algo |
| **AVIF** | se puede añadir como `<source>` extra; WebP ya cubre el 97 % de los navegadores |

---

## 6. Archivos que toca esta rama

```
tools/peso.py                     mide el peso por página
tools/optimizar_imagenes.py       recompresión + WebP + data/medios.yaml
tools/comprimir_videos.py         recompresión + posters + data/videos.yaml
tools/pasar_a_picture.py          pasa <img> del contenido a shortcode
layouts/partials/picture.html     <picture> responsive
layouts/shortcodes/picture.html   {{< picture … >}}
layouts/_default/servicio.html    usa el partial en las secciones
data/medios.yaml                  dimensiones y variantes (generado)
data/videos.yaml                  posters y dimensiones (generado)
static/assets/opt/*.webp          65 variantes (generado)
```
