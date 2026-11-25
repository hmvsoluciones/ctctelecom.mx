# -*- coding: utf-8 -*-
"""
Genera variantes WebP de alta calidad para las imágenes del sitio.

Perfil por defecto (calidad):
  - NO toca el archivo original: el respaldo <img> queda bit a bit igual.
  - WebP con calidad 92 (visualmente indistinguible en pantalla).
  - Variantes 480 / 960 / 1600 px + el ancho nativo cuando es mayor.
  - Registra dimensiones y variantes en data/medios.yaml.

Uso:
    python tools/optimizar_imagenes.py                 # perfil calidad (92)
    python tools/optimizar_imagenes.py --calidad 96    # aún más conservador
    python tools/optimizar_imagenes.py --calidad 82 --recomprimir   # perfil ligero
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

ANCHO_MAX = 2048
VARIANTES = (480, 960, 1600)
EXT = (".png", ".jpg", ".jpeg")


def leer_manifiesto():
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


def variantes_para(ancho):
    v = [w for w in VARIANTES if w < ancho]
    v.append(min(ancho, ANCHO_MAX))
    return sorted(set(v))


def procesar(nombre, calidad):
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

    os.makedirs(SALIDA, exist_ok=True)
    stem = os.path.splitext(nombre)[0]
    widths = variantes_para(ancho)
    # los PNG suelen ser capturas, diagramas o logos con texto: más calidad
    q = min(98, calidad + 3) if nombre.lower().endswith(".png") else calidad
    for w in widths:
        h = round(alto * w / ancho)
        v = img if w == ancho else img.resize((w, h), Image.LANCZOS)
        # exact=True conserva el color de los píxeles transparentes (logos, iconos)
        v.save(os.path.join(SALIDA, f"{stem}-{w}.webp"), "WEBP",
               quality=q, method=6, exact=True)
    return ancho, alto, widths


def main(argv):
    calidad = 92
    if "--calidad" in argv:
        calidad = int(argv[argv.index("--calidad") + 1])
    force = "--force" in argv
    recomprimir = "--recomprimir" in argv

    previo = leer_manifiesto()
    imagenes = sorted(f for f in os.listdir(ASSETS)
                      if f.lower().endswith(EXT) and os.path.isfile(os.path.join(ASSETS, f)))

    filas, total_webp = [], 0
    for nombre in imagenes:
        ruta = os.path.join(ASSETS, nombre)
        stem = os.path.splitext(nombre)[0]
        esperadas = variantes_para(Image.open(ruta).size[0])
        completas = all(os.path.isfile(os.path.join(SALIDA, f"{stem}-{w}.webp")) for w in esperadas)

        if nombre in previo and completas and not force:
            info = previo[nombre]
            filas.append((nombre, info["width"], info["height"], info["widths"]))
            total_webp += sum(os.path.getsize(os.path.join(SALIDA, f"{stem}-{w}.webp"))
                              for w in info["widths"])
            continue

        print(f"  → {nombre:52}", end="", flush=True)
        ancho, alto, widths = procesar(nombre, calidad)
        peso = sum(os.path.getsize(os.path.join(SALIDA, f"{stem}-{w}.webp")) for w in widths)
        total_webp += peso
        print(f" {ancho}x{alto}  webp {peso/1024:6.0f}K  q{calidad}")
        filas.append((nombre, ancho, alto, widths))

    if recomprimir:
        print("\n  (perfil ligero: recomprimiendo originales…)")
        for nombre, _, _, _ in filas:
            ruta = os.path.join(ASSETS, nombre)
            img = Image.open(ruta)
            buf = io.BytesIO()
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img.convert("RGBA").save(buf, "PNG", optimize=True)
            else:
                img.convert("RGB").save(buf, "JPEG", quality=82, optimize=True, progressive=True)
            if buf.tell() < os.path.getsize(ruta):
                with open(ruta, "wb") as f:
                    f.write(buf.getvalue())

    with io.open(MANIFIESTO, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Generado por tools/optimizar_imagenes.py\n")
        f.write(f"# WebP calidad {calidad}; los originales no se modifican.\n")
        f.write("medios:\n")
        for nombre, ancho, alto, widths in filas:
            f.write(f'  "{nombre}":\n')
            f.write(f"    width: {ancho}\n")
            f.write(f"    height: {alto}\n")
            f.write("    widths:\n")
            for w in widths:
                f.write(f"      - {w}\n")

    print()
    print(f"imágenes procesadas: {len(filas)}")
    print(f"WebP total: {total_webp/1048576:.2f} MB (calidad {calidad})")
    print(f"originales: intactos")
    print(f"manifiesto: {MANIFIESTO}")


if __name__ == "__main__":
    main(sys.argv[1:])
