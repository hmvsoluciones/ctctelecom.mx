# Rendimiento — rama `feature/performance`

Optimización **sin pérdida de calidad visible**, alineada con la mejora 8 del análisis de HMV
Soluciones («Optimizar imágenes y medir rendimiento»).

La regla que se aplicó: **los originales no se tocan** (quedan como respaldo `<img>` bit a bit
idénticos) y lo que se sirve son variantes WebP de alta calidad. Cada cambio está medido con
**SSIM/PSNR** en [`calidad-medios.md`](calidad-medios.md).

---

## 1. Qué cambió

| Métrica | Antes | Ahora | Δ |
|---|---:|---:|---:|
| Portada, escritorio | 43.4 MB | **20.9 MB** | −52 % |
| Portada, móvil (video 720p) | 43.4 MB | **≈ 4.6 MB** | −89 % |
| `/data-center/` | 16.1 MB | 6.8 MB | −58 % |
| `/integracion/` | 5.0 MB | 3.1 MB | −39 % |
| Videos (8) | 65.7 MB | **34.2 MB** | −48 % |
| Imágenes: WebP servido | — | 11.0 MB en 114 variantes | — |
| `public/` completo | 103.3 MB | 88.7 MB | −14 % |

El total del despliegue baja poco **a propósito**: los archivos originales se conservan como
respaldo para navegadores sin WebP. Lo que baja de verdad es lo que se descarga cada visitante.

### Calidad medida

| Tipo | SSIM medio | SSIM mínimo | PSNR |
|---|---:|---:|---:|
| Imágenes (original vs WebP) | **0.9943** | 0.9807 | 44–52 dB |
| Videos (original vs recomprimido, a 1440 px) | **0.9901** | 0.9828 | 39–48 dB |

Referencia: SSIM 1.0 = idéntico; por encima de 0.98 la diferencia no se aprecia a simple vista y un
PSNR sobre 40 dB se considera visualmente sin pérdida. Detalle por archivo en
[`calidad-medios.md`](calidad-medios.md).

---

## 2. Decisiones de calidad

### Imágenes

- **WebP calidad 92** (95 en PNG, que suelen ser capturas, diagramas o logos con texto).
- `method=6` (mejor compresión) y **`exact=True`**: conserva el color de los píxeles transparentes,
  que es lo que degrada los logos con alfa en WebP.
- **Sin reescalar**: la variante mayor usa el tamaño nativo (tope 2048 px). El `srcset` ofrece
  480 / 960 / 1600 / nativo, así que el móvil descarga menos sin pérdida en escritorio.
- El `<img>` de respaldo apunta **al archivo original intacto**: cero pérdida para navegadores sin WebP.

### Video

- **H.264 CRF 21, preset slow**, resolución nativa con tope **1920 px** (más ancho no se muestra en
  pantalla y solo engorda el archivo).
- **Sin pista de audio**: siempre se reproducen `muted`; quitarla no cambia nada perceptible y ahorra
  unos kbps.
- **`+faststart`** para que empiece antes.
- **Variante de 720 px** para pantallas ≤ 700 px, servida con `<source media="(max-width: 700px)">`.
  En móvil el video del hero pasa de 19.8 MB a **2.9 MB**.
- **Poster JPEG** en todos: evita el hueco negro mientras carga.

---

## 3. Cómo se genera

```powershell
# 1) imágenes: WebP de alta calidad (no toca los originales)
python tools\optimizar_imagenes.py

# 2) videos: CRF 21 a 1920 px + variante 720p + poster
python tools\comprimir_videos.py

# 3) variante móvil en el contenido ya existente
python tools\insertar_video_movil.py

# 4) compilar y medir
hugo --cleanDestinationDir
python tools\peso.py
python tools\verificar_calidad.py --md docs\calidad-medios.md
```

Ambas herramientas son idempotentes: si el manifiesto ya tiene el archivo y las variantes existen,
lo saltan. Los originales de imagen y video se respaldan en `../_medios_originales` (fuera del repo)
para poder comparar calidad.

### Si algún día se prioriza el peso sobre la calidad

Existe un perfil agresivo, que es el que se usó en la primera pasada de esta rama:

```powershell
python tools/optimizar_imagenes.py --calidad 82 --recomprimir
python tools/comprimir_videos.py --crf 28 --max-ancho 1280
```

Resultado de ese perfil: `public/` 37 MB, portada 4.5 MB, con SSIM ≈ 0.95–0.97 (se nota en
degradados y texto pequeño). **No es el que queda activo.**

---

## 4. Pendiente (siguiente iteración)

| Tema | Detalle |
|---|---|
| **Video del hero con carga diferida** | es el 95 % del peso de escritorio; cargarlo tras el primer render (IntersectionObserver) o solo si `navigator.connection` no es `saveData` reduce el impacto sin tocar la calidad |
| **AV1 o HEVC como `<source>` extra** | con el mismo SSIM bajaría a ~8 MB; requiere probar compatibilidad (Safari/HEVC, Chrome+Firefox/AV1) |
| **Montserrat self-hosted + subset** | hoy son 2 conexiones a Google Fonts que bloquean el render |
| **Cabeceras de caché** | sin `Cache-Control` se vuelve a descargar todo en cada visita: ver [`servidor/cache-y-compresion.md`](servidor/cache-y-compresion.md) |
| **Medición de campo** | GA4 + Search Console para comprobar el efecto real |

---

## 5. Archivos de esta rama

```
tools/peso.py                     mide el peso real por página
tools/optimizar_imagenes.py       WebP de alta calidad + data/medios.yaml
tools/comprimir_videos.py         H.264 CRF 21 + 720p + posters + data/videos.yaml
tools/insertar_video_movil.py     <source media> en los <video> del contenido
tools/pasar_a_picture.py          migra <img> del contenido al shortcode
tools/verificar_calidad.py        SSIM/PSNR por archivo → docs/calidad-medios.md
layouts/partials/picture.html     <picture> con srcset, dimensiones y lazy
layouts/shortcodes/picture.html   {{< picture … >}}
layouts/_default/servicio.html    picture + poster + video móvil
data/medios.yaml                  dimensiones y variantes (generado)
data/videos.yaml                  posters, dimensiones y variante móvil (generado)
static/assets/opt/*.webp          114 variantes (generado)
```
