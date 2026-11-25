# -*- coding: utf-8 -*-
"""
Mide cuánta calidad se pierde con la optimización (SSIM y PSNR).

Compara cada imagen original (respaldo en ../_medios_originales o el propio static)
contra la variante WebP más grande, y cada video original contra el recomprimido,
a resolución de visualización (1440 px de ancho).

Uso:
    python tools/verificar_calidad.py            # imprime la tabla
    python tools/verificar_calidad.py --md docs/calidad-medios.md

Referencia de SSIM: 1.0 = idéntico. Por encima de 0.98 no se distingue a simple vista;
por debajo de 0.95 empieza a notarse en degradados y texto.
"""
import io
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(RAIZ, "static", "assets")
RESPALDO = os.path.join(os.path.dirname(RAIZ), "_medios_originales")
MANIFIESTO = os.path.join(RAIZ, "data", "medios.yaml")
ANCHO_VISTA = 1440


# ------------------------------------------------------------------ SSIM
def _filtro_media(a, k=7):
    """Media en ventana kxk usando sumas acumuladas (rápido, sin scipy)."""
    pad = k // 2
    p = np.pad(a, pad, mode="reflect")
    c = np.cumsum(np.cumsum(p, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)), mode="constant")
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def ssim(a, b, k=7, L=255.0):
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    C1, C2 = (0.01 * L) ** 2, (0.03 * L) ** 2
    mu_a, mu_b = _filtro_media(a, k), _filtro_media(b, k)
    va = _filtro_media(a * a, k) - mu_a ** 2
    vb = _filtro_media(b * b, k) - mu_b ** 2
    cov = _filtro_media(a * b, k) - mu_a * mu_b
    s = ((2 * mu_a * mu_b + C1) * (2 * cov + C2)) / \
        ((mu_a ** 2 + mu_b ** 2 + C1) * (va + vb + C2))
    return float(s.mean())


def psnr(a, b):
    mse = np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)
    if mse == 0:
        return float("inf")
    return float(10 * np.log10(255.0 ** 2 / mse))


def gris(img):
    return np.asarray(img.convert("L"), dtype=np.uint8)


def sobre_blanco(img):
    """Compone sobre blanco: así se ve un PNG con transparencia en la página."""
    if "A" in img.getbands():
        fondo = Image.new("RGBA", img.size, (255, 255, 255, 255))
        return Image.alpha_composite(fondo, img.convert("RGBA")).convert("RGB")
    return img.convert("RGB")


# ------------------------------------------------------------------ imágenes
def comparar_imagen(nombre, ancho_max):
    original = os.path.join(RESPALDO, nombre)
    if not os.path.isfile(original):
        original = os.path.join(ASSETS, nombre)
    stem = os.path.splitext(nombre)[0]
    webp = os.path.join(ASSETS, "opt", f"{stem}-{ancho_max}.webp")
    if not os.path.isfile(webp):
        return None

    a = ImageOps.exif_transpose(Image.open(original))
    b = Image.open(webp)
    if b.size != a.size:
        a = a.resize(b.size, Image.LANCZOS)
    a, b = sobre_blanco(a), sobre_blanco(b)
    ga, gb = gris(a), gris(b)
    return {
        "tipo": "imagen",
        "nombre": nombre,
        "tamano": f"{a.size[0]}x{a.size[1]}",
        "peso_original": os.path.getsize(original),
        "peso_opt": os.path.getsize(webp),
        "ssim": ssim(ga, gb),
        "psnr": psnr(ga, gb),
    }


# ------------------------------------------------------------------ video
def ffmpeg_exe(nombre):
    base = os.environ.get("FFMPEG_DIR")
    if base:
        p = os.path.join(base, nombre + (".exe" if os.name == "nt" else ""))
        if os.path.isfile(p):
            return p
    from shutil import which
    return which(nombre)


def medir_video(ff, opt, orig, filtro, ancho):
    """Corre un filtro (ssim o psnr) y devuelve el valor medio."""
    cadena = (f"[0:v]scale={ancho}:-2[a];[1:v]scale={ancho}:-2[b];[a][b]{filtro}")
    res = subprocess.run([ff, "-i", opt, "-i", orig, "-lavfi", cadena, "-f", "null", "-"],
                         capture_output=True, text=True)
    for linea in res.stderr.splitlines():
        if filtro == "ssim" and "SSIM" in linea and "All:" in linea:
            return float(linea.split("All:")[1].split()[0])
        if filtro == "psnr" and "PSNR" in linea and "average:" in linea:
            try:
                return float(linea.split("average:")[1].split()[0])
            except ValueError:
                return None
    return None


def comparar_video(nombre, ancho):
    orig = os.path.join(RESPALDO, nombre)
    opt = os.path.join(ASSETS, nombre)
    if not os.path.isfile(orig) or not os.path.isfile(opt):
        return None
    ff = ffmpeg_exe("ffmpeg")
    if not ff:
        return None
    ssim_v = medir_video(ff, opt, orig, "ssim", ancho)
    if ssim_v is None:
        return None
    return {
        "tipo": "video",
        "nombre": nombre,
        "tamano": f"{ancho}px (vista)",
        "peso_original": os.path.getsize(orig),
        "peso_opt": os.path.getsize(opt),
        "ssim": ssim_v,
        "psnr": medir_video(ff, opt, orig, "psnr", ancho),
    }


def leer_medios():
    filas = []
    actual = None
    for linea in io.open(MANIFIESTO, encoding="utf-8"):
        s = linea.strip()
        if s.startswith('"') and s.endswith('":'):
            actual = s[1:-2]
        elif actual and s.startswith("- "):
            filas.append((actual, int(s[2:])))
    return filas


def main(argv):
    filas = []
    for nombre, ancho in leer_medios():
        r = comparar_imagen(nombre, ancho)
        if r:
            filas.append(r)

    ff = ffmpeg_exe("ffmpeg")
    if ff:
        videos = sorted(f for f in os.listdir(ASSETS)
                        if f.lower().endswith(".mp4") and not f.endswith("-720.mp4"))
        for v in videos:
            r = comparar_video(v, ANCHO_VISTA)
            if r:
                filas.append(r)

    def linea(r):
        return (f"| {r['nombre']} | {r['tamano']} | {r['peso_original']/1024:.0f} KB | "
                f"{r['peso_opt']/1024:.0f} KB | {r['ssim']:.4f} | "
                f"{('%.1f dB' % r['psnr']) if r['psnr'] else '—'} |")

    encabezado = ("| archivo | tamaño | original | optimizado | SSIM | PSNR |\n"
                  "|---|---|---:|---:|---:|---:|")

    print(encabezado)
    for r in filas:
        print(linea(r))

    img = [r for r in filas if r["tipo"] == "imagen"]
    vid = [r for r in filas if r["tipo"] == "video"]
    if img:
        print(f"\nimágenes: SSIM medio {np.mean([r['ssim'] for r in img]):.4f} "
              f"(mínimo {min(r['ssim'] for r in img):.4f})")
    if vid:
        print(f"videos:   SSIM medio {np.mean([r['ssim'] for r in vid]):.4f} "
              f"(mínimo {min(r['ssim'] for r in vid):.4f})")

    if "--md" in argv:
        destino = argv[argv.index("--md") + 1]
        with io.open(destino, "w", encoding="utf-8", newline="\n") as f:
            f.write("# Calidad de los medios optimizados\n\n")
            f.write("Generado con `python tools/verificar_calidad.py --md "
                    "docs/calidad-medios.md`.\n\n")
            f.write("SSIM compara el original con el archivo que sirve el sitio, a resolución de "
                    "visualización (1440 px para video). **1.0 = idéntico**; por encima de 0.98 la "
                    "diferencia no se aprecia a simple vista.\n\n")
            f.write(encabezado + "\n")
            for r in filas:
                f.write(linea(r) + "\n")
            f.write("\n")
            if img:
                f.write(f"- Imágenes: SSIM medio **{np.mean([r['ssim'] for r in img]):.4f}**, "
                        f"mínimo {min(r['ssim'] for r in img):.4f}.\n")
            if vid:
                f.write(f"- Videos: SSIM medio **{np.mean([r['ssim'] for r in vid]):.4f}**, "
                        f"mínimo {min(r['ssim'] for r in vid):.4f}.\n")
        print("escrito:", destino)


if __name__ == "__main__":
    main(sys.argv[1:])
