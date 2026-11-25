# -*- coding: utf-8 -*-
"""
Optimiza las imágenes del sitio y genera variantes WebP responsivas.

Para cada PNG/JPG de static/assets:
  - reduce a 1600 px de ancho como máximo (si es más grande) y recomprime;
  - genera variantes WebP de 480 / 960 / 1600 px (las que quepan);
  - registra dimensiones y variantes en data/medios.yaml.

Es idempotente: si el manifiesto ya tiene la imagen y las variantes existen, la omite.

Uso:
    python tools/optimizar_imagenes.py
    python tools/optimizar_imagenes.py --force
"""
import io
import os
import sys

from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RAIZ, "static", "assets")
SALIDA = os.path.join(ASSETS, "opt")
MANIFIESTO = os.path.join(RAIZ, "data", "medios.yaml")

ANCHO_MAX = 1600
VARIANTES = (480, 960, 1600)
CALIDAD_WEBP = 82
CALIDAD_JPG = 82
EXT = (".png", ".jpg", ".jpeg")


def leer_manifiesto():
    """Devuelve {nombre: (ancho, alto, [variantes])} del manifiesto existente."""
    datos = {}
    if not os.path.isfile(MANIFIESTO):
        return datos
    actual = None
    for linea in io.open(MANIFIESTO, encoding="utf-8"):
        s = linea.strip()
        if s.startswith('"') and s.endswith('":'):
            actual = s[1:-2]
            datos[actual] = {"width": 0, "height": 0, "widths": []}
        elif actual and s.startswith("width:"):
            datos[actual]["width"] = int(s.split(":")[1])
        elif actual and s.startswith("height:"):
            datos[actual]["height"] = int(s.split(":")[1])
        elif actual and s.startswith("- "):
            datos[actual]["widths"].append(int(s[2:]))
    return datos


def procesar(nombre):
    origen = os.path.join(ASSETS, nombre)
    img = Image.open(origen)
    img = ImageOps.exif_transpose(img)
    tiene_alfa = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    img = img.convert("RGBA" if tiene_alfa else "RGB")

    ancho, alto = img.size
    if ancho > ANCHO_MAX:
        alto = round(alto * ANCHO_MAX / ancho)
        ancho = ANCHO_MAX
        img = img.resize((ancho, alto), Image.LANCZOS)

    # 1) recomprimir el original (mismo nombre y formato) solo si pesa menos
    antes = os.path.getsize(origen)
    buf = io.BytesIO()
    if tiene_alfa:
        img.save(buf, "PNG", optimize=True)
    else:
        img.save(buf, "JPEG", quality=CALIDAD_JPG, optimize=True, progressive=True)
    if buf.tell() < antes:
        with open(origen, "wb") as f:
            f.write(buf.getvalue())

    # 2) variantes WebP
    os.makedirs(SALIDA, exist_ok=True)
    stem = os.path.splitext(nombre)[0].replace("/", "-")
    generadas = []
    for w in VARIANTES:
        if w > ancho:
            continue
        h = round(alto * w / ancho)
        v = img.resize((w, h), Image.LANCZOS)
        destino = os.path.join(SALIDA, f"{stem}-{w}.webp")
        v.save(destino, "WEBP", quality=CALIDAD_WEBP, method=6)
        generadas.append(w)
    if not generadas:  # imágenes más pequeñas que 480: una sola variante
        destino = os.path.join(SALIDA, f"{stem}-{ancho}.webp")
        img.save(destino, "WEBP", quality=CALIDAD_WEBP, method=6)
        generadas = [ancho]

    return ancho, alto, generadas


def main():
    force = "--force" in sys.argv
    previo = leer_manifiesto()
    imagenes = sorted(f for f in os.listdir(ASSETS)
                      if f.lower().endswith(EXT) and os.path.isfile(os.path.join(ASSETS, f)))

    antes_total = despues_total = 0
    filas = []
    for nombre in imagenes:
        ruta = os.path.join(ASSETS, nombre)
        antes = os.path.getsize(ruta)
        stem = os.path.splitext(nombre)[0]
        variantes_ok = all(
            os.path.isfile(os.path.join(SALIDA, f"{stem}-{w}.webp"))
            for w in previo.get(nombre, {}).get("widths", [])) if nombre in previo else False

        if nombre in previo and variantes_ok and not force:
            despues = antes
            filas.append((nombre, antes, despues, previo[nombre]["width"],
                          previo[nombre]["height"], previo[nombre]["widths"]))
            antes_total += antes
            despues_total += despues
            continue

        print(f"  → {nombre:52}", end="", flush=True)
        ancho, alto, widths = procesar(nombre)
        despues = os.path.getsize(ruta)
        print(f" {antes/1024:6.0f}K → {despues/1024:6.0f}K  {widths}")
        filas.append((nombre, antes, despues, ancho, alto, widths))
        antes_total += antes
        despues_total += despues

    with io.open(MANIFIESTO, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Generado por tools/optimizar_imagenes.py\n")
        f.write("# dimensions + variantes WebP disponibles en /assets/opt/\n")
        f.write("medios:\n")
        for nombre, _, _, ancho, alto, widths in filas:
            f.write(f'  "{nombre}":\n')
            f.write(f"    width: {ancho}\n")
            f.write(f"    height: {alto}\n")
            f.write("    widths:\n")
            for w in widths:
                f.write(f"      - {w}\n")

    print()
    print(f"originales:  {antes_total/1048576:7.2f} MB")
    print(f"recomprimido:{despues_total/1048576:7.2f} MB")
    print(f"manifiesto:  {MANIFIESTO}")


if __name__ == "__main__":
    main()
