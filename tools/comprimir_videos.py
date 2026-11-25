# -*- coding: utf-8 -*-
"""
Recomprime los videos del sitio y genera un poster por cada uno.

- Escala a 1280 px de ancho como máximo (los videos son fondos decorativos).
- H.264 CRF 30, sin audio, `+faststart` (arranca antes en el navegador).
- Poster en JPEG (primer fotograma útil) para evitar el hueco negro.

Uso (desde la raíz del proyecto):
    python tools/comprimir_videos.py            # procesa los que falten
    python tools/comprimir_videos.py --force    # vuelve a procesar todo

Requiere ffmpeg y ffprobe en el PATH (o define FFMPEG_DIR).
Genera/actualiza data/videos.yaml con el resultado.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RAIZ, "static", "assets")
MANIFIESTO = os.path.join(RAIZ, "data", "videos.yaml")

CRF = "30"
MAX_ANCHO = 1280


def buscar_exe(nombre):
    p = shutil.which(nombre)
    if p:
        return p
    base = os.environ.get("FFMPEG_DIR")
    if base:
        cand = os.path.join(base, nombre + (".exe" if os.name == "nt" else ""))
        if os.path.isfile(cand):
            return cand
    return None


FFMPEG = buscar_exe("ffmpeg")
FFPROBE = buscar_exe("ffprobe")


def dimensiones(ruta):
    salida = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "json", ruta],
        capture_output=True, text=True, check=True).stdout
    st = json.loads(salida)["streams"][0]
    return int(st["width"]), int(st["height"])


def cargar_manifiesto():
    if not os.path.isfile(MANIFIESTO):
        return {}
    datos = {}
    for linea in open(MANIFIESTO, encoding="utf-8"):
        if ": " in linea and linea.startswith("  "):
            k, v = linea.strip().split(": ", 1)
            datos[k] = v.strip('"')
    return datos


def crear_poster(ruta, destino_poster, ancho):
    subprocess.run([FFMPEG, "-y", "-ss", "1", "-i", ruta, "-frames:v", "1",
                    "-vf", f"scale={ancho}:-2", "-q:v", "4", destino_poster],
                   check=True, capture_output=True)


def comprimir(ruta, force):
    nombre = os.path.basename(ruta)
    poster = os.path.splitext(nombre)[0] + "-poster.jpg"
    destino_poster = os.path.join(ASSETS, poster)
    a, h = dimensiones(ruta)
    ancho = min(MAX_ANCHO, a)
    tmp = os.path.join(tempfile.gettempdir(), "ctc-" + nombre)

    cmd = [FFMPEG, "-y", "-i", ruta,
           "-vf", f"scale={ancho}:-2",
           "-c:v", "libx264", "-crf", CRF, "-preset", "medium",
           "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart",
           tmp]
    subprocess.run(cmd, check=True, capture_output=True)

    if os.path.getsize(tmp) < os.path.getsize(ruta) or force:
        shutil.move(tmp, ruta)
    else:
        os.remove(tmp)

    subprocess.run([FFMPEG, "-y", "-ss", "1", "-i", ruta, "-frames:v", "1",
                    "-vf", f"scale={ancho}:-2", "-q:v", "4", destino_poster],
                   check=True, capture_output=True)
    return {"poster": "/assets/" + poster, "width": ancho, "height": int(h * ancho / a)}


def main():
    if not FFMPEG or not FFPROBE:
        print("No se encontró ffmpeg/ffprobe. Instálalos o define FFMPEG_DIR.")
        sys.exit(1)

    force = "--force" in sys.argv
    previo = cargar_manifiesto()
    videos = sorted(f for f in os.listdir(ASSETS) if f.lower().endswith(".mp4"))
    total_antes = total_despues = 0
    lineas = []

    for v in videos:
        ruta = os.path.join(ASSETS, v)
        antes = os.path.getsize(ruta)
        # idempotencia: si ya está en el manifiesto y ya es pequeño, se omite
        before = antes
        hecho = previo.get(v)
        if hecho and antes < 3 * 1024 * 1024 and not force:
            info = comprimir_metadata(v, ruta)
            poster_abs = os.path.join(ASSETS, os.path.basename(info["poster"]))
            if not os.path.isfile(poster_abs):
                crear_poster(ruta, poster_abs, info["width"])
            print(f"  = {v:34} {antes/1048576:6.1f} MB (ya optimizado)")
            total_antes += before
            total_despues += antes
            lineas.append((v, info))
            continue

        print(f"  → {v:34} {antes/1048576:6.1f} MB ...", end="", flush=True)
        info = comprimir(ruta, force)
        despues = os.path.getsize(ruta)
        total_antes += antes
        total_despues += despues
        print(f" {despues/1048576:6.1f} MB")
        lineas.append((v, info))

    with open(MANIFIESTO, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Generado por tools/comprimir_videos.py\nvideos:\n")
        for v, info in lineas:
            f.write(f'  "{v}":\n')
            f.write(f'    poster: "{info["poster"]}"\n')
            f.write(f'    width: {info["width"]}\n')
            f.write(f'    height: {info["height"]}\n')

    print()
    print(f"antes:   {total_antes/1048576:7.1f} MB")
    print(f"después: {total_despues/1048576:7.1f} MB "
          f"({100 - total_despues*100/max(total_antes,1):.0f}% menos)")
    print(f"manifiesto: {MANIFIESTO}")


def comprimir_metadata(nombre, ruta):
    a, h = dimensiones(ruta)
    poster = os.path.splitext(nombre)[0] + "-poster.jpg"
    return {"poster": "/assets/" + poster, "width": a, "height": h}


if __name__ == "__main__":
    main()
