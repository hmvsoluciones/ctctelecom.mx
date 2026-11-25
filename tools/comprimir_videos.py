# -*- coding: utf-8 -*-
"""
Recomprime los videos con perfil de calidad y genera un poster por cada uno.

Perfil por defecto (calidad):
  - Resolución nativa, con tope de 1920 px de ancho (más que eso no se muestra).
  - H.264 CRF 21, preset slow, sin audio, +faststart.
  - Variante móvil de 720 px para los videos grandes (se sirve con <source media>).

Uso:
    python tools/comprimir_videos.py                  # perfil calidad (CRF 21)
    python tools/comprimir_videos.py --crf 18         # más conservador todavía
    python tools/comprimir_videos.py --crf 28 --max-ancho 1280   # perfil ligero
    python tools/comprimir_videos.py --force

Requiere ffmpeg/ffprobe en el PATH (o define FFMPEG_DIR).
Los originales se respaldan en ../_medios_originales (fuera del repo) para poder
comparar calidad después.
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RAIZ, "static", "assets")
RESPALDO = os.path.join(os.path.dirname(RAIZ), "_medios_originales")
MANIFIESTO = os.path.join(RAIZ, "data", "videos.yaml")

CRF = 21
MAX_ANCHO = 1920
ANCHO_MOVIL = 720
CRF_MOVIL = 24
UMBRAL_MOVIL_MB = 3.0


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


def original_respaldo(nombre):
    p = os.path.join(RESPALDO, nombre)
    return p if os.path.isfile(p) else None


def codificar(origen, destino, ancho, crf, preset):
    cmd = [FFMPEG, "-y", "-i", origen]
    if ancho:
        cmd += ["-vf", f"scale={ancho}:-2"]
    cmd += ["-c:v", "libx264", "-crf", str(crf), "-preset", preset,
            "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", destino]
    subprocess.run(cmd, check=True, capture_output=True)


def poster(origen, destino, ancho):
    subprocess.run([FFMPEG, "-y", "-ss", "1", "-i", origen, "-frames:v", "1",
                    "-vf", f"scale={ancho}:-2", "-q:v", "2", destino],
                   check=True, capture_output=True)


def main(argv):
    global CRF, MAX_ANCHO
    if "--crf" in argv:
        CRF = int(argv[argv.index("--crf") + 1])
    if "--max-ancho" in argv:
        MAX_ANCHO = int(argv[argv.index("--max-ancho") + 1])
    force = "--force" in argv

    if not FFMPEG or not FFPROBE:
        print("No se encontró ffmpeg/ffprobe. Instálalos o define FFMPEG_DIR.")
        sys.exit(1)

    os.makedirs(RESPALDO, exist_ok=True)
    previo = io.open(MANIFIESTO, encoding="utf-8").read() if os.path.isfile(MANIFIESTO) else ""

    videos = sorted(f for f in os.listdir(ASSETS) if f.lower().endswith(".mp4")
                    and not f.endswith("-720.mp4"))
    lineas = []
    antes_total = despues_total = 0

    for v in videos:
        ruta = os.path.join(ASSETS, v)
        stem = os.path.splitext(v)[0]

        # respaldo del original (solo la primera vez)
        orig = original_respaldo(v)
        if not orig:
            shutil.copy2(ruta, os.path.join(RESPALDO, v))
            orig = os.path.join(RESPALDO, v)

        antes = os.path.getsize(orig)
        ya_hecho = f'"{v}":' in previo and os.path.getsize(ruta) < antes * 0.95
        if ya_hecho and not force:
            print(f"  = {v:34} {os.path.getsize(ruta)/1048576:6.1f} MB (ya optimizado)")
            a, h = dimensiones(ruta)
            info = {"poster": f"/assets/{stem}-poster.jpg", "width": a, "height": h}
            movil = os.path.join(ASSETS, f"{stem}-720.mp4")
            if os.path.isfile(movil):
                info["mobile"] = f"/assets/{stem}-720.mp4"
            lineas.append((v, info))
            antes_total += antes
            despues_total += os.path.getsize(ruta)
            continue

        a, h = dimensiones(orig)
        ancho = min(MAX_ANCHO, a)
        print(f"  → {v:34} {antes/1048576:6.1f} MB  {a}x{h} ...", end="", flush=True)

        tmp = os.path.join(tempfile.gettempdir(), "ctc-" + v)
        codificar(orig, tmp, ancho if ancho < a else None, CRF, "slow")
        shutil.move(tmp, ruta)

        info = {"poster": f"/assets/{stem}-poster.jpg",
                "width": ancho, "height": round(h * ancho / a)}
        poster(ruta, os.path.join(ASSETS, stem + "-poster.jpg"), min(1280, ancho))

        if os.path.getsize(ruta) / 1048576 > UMBRAL_MOVIL_MB and ancho > ANCHO_MOVIL:
            movil = os.path.join(ASSETS, f"{stem}-720.mp4")
            codificar(orig, movil, ANCHO_MOVIL, CRF_MOVIL, "slow")
            info["mobile"] = f"/assets/{stem}-720.mp4"

        despues = os.path.getsize(ruta)
        antes_total += antes
        despues_total += despues
        print(f" {despues/1048576:6.1f} MB")
        lineas.append((v, info))

    with io.open(MANIFIESTO, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Generado por tools/comprimir_videos.py\n")
        f.write(f"# H.264 CRF {CRF}, preset slow, sin audio, tope {MAX_ANCHO}px\n")
        f.write("videos:\n")
        for v, info in lineas:
            f.write(f'  "{v}":\n')
            f.write(f'    poster: "{info["poster"]}"\n')
            f.write(f'    width: {info["width"]}\n')
            f.write(f'    height: {info["height"]}\n')
            if info.get("mobile"):
                f.write(f'    mobile: "{info["mobile"]}"\n')

    print()
    print(f"antes:   {antes_total/1048576:7.1f} MB")
    print(f"después: {despues_total/1048576:7.1f} MB "
          f"({100 - despues_total*100/max(antes_total,1):.0f}% menos)")
    print(f"manifiesto: {MANIFIESTO}")


if __name__ == "__main__":
    main(sys.argv[1:])
