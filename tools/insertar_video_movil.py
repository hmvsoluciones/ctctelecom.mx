# -*- coding: utf-8 -*-
"""
Inserta la variante móvil de video (<source media="(max-width: 700px)">) en el
contenido HTML, usando data/videos.yaml.

Uso: python tools/insertar_video_movil.py
"""
import io
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(RAIZ, "content")
MANIFIESTO = os.path.join(RAIZ, "data", "videos.yaml")

MOVILES = {}
actual = None
for linea in io.open(MANIFIESTO, encoding="utf-8"):
    s = linea.strip()
    if s.startswith('"') and s.endswith('":'):
        actual = s[1:-2]
    elif s.startswith("mobile:") and actual:
        MOVILES[actual] = s.split('"')[1]

MOD = 'media="(max-width: 700px)"'


def procesar(bloque, moviles):
    m = re.search(r'src="(/assets/[^"]+\.mp4)"', bloque)
    if not m:
        return bloque
    movil = moviles.get(os.path.basename(m.group(1)))
    if not movil or movil in bloque:
        return bloque
    nuevo = f'<source src="{movil}" type="video/mp4" {MOD}>'
    # se inserta antes del primer <source ...> del bloque
    return bloque.replace("<source ", nuevo + "<source ", 1)


def main():
    cambios = 0
    for dirpath, _, files in os.walk(CONTENT):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dirpath, f)
            s = io.open(p, encoding="utf-8").read()
            nuevo = re.sub(r"<video[\s\S]*?</video>", lambda m: procesar(m.group(0), MOVILES), s)
            if nuevo != s:
                io.open(p, "w", encoding="utf-8", newline="\n").write(nuevo)
                print("actualizado:", os.path.relpath(p, RAIZ))
                cambios += 1
    print("archivos modificados:", cambios, "| videos con variante móvil:", len(MOVILES))


if __name__ == "__main__":
    main()
