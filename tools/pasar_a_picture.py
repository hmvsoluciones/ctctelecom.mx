# -*- coding: utf-8 -*-
"""Pasa las <img> del contenido a shortcodes {{< picture >}} y agrega poster a los <video>.

Uso: python tools/pasar_a_picture.py
"""
import io
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(RAIZ, "content")

IMG_RE = re.compile(r'<img\s([^>]*?)>', re.S)
ATTR_RE = re.compile(r'([a-zA-Z-]+)="([^"]*)"')

VIDEO_RE = re.compile(r'<video\s([^>]*)>', re.S)

POSTERS = {}
for linea in io.open(os.path.join(RAIZ, "data", "videos.yaml"), encoding="utf-8"):
    s = linea.strip()
    if s.startswith('"') and s.endswith('":'):
        actual = s[1:-2]
    elif s.startswith("poster:"):
        POSTERS[actual] = s.split('"')[1]


def img_a_shortcode(m):
    attrs = dict(ATTR_RE.findall(m.group(1)))
    src = attrs.get("src")
    if not src:
        return m.group(0)
    partes = [f'src="{src}"', f'alt="{attrs.get("alt", "")}"']
    for clave, destino in (("class", "class"), ("style", "style"),
                           ("loading", "loading"), ("sizes", "sizes")):
        if clave in attrs:
            partes.append(f'{destino}="{attrs[clave]}"')
    return "{{< picture " + " ".join(partes) + " >}}"


def video_con_poster(m):
    attrs = dict(ATTR_RE.findall(m.group(1)))
    src = None
    return m.group(0)


def main():
    cambios = 0
    for dirpath, _, files in os.walk(CONTENT):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dirpath, f)
            s = io.open(p, encoding="utf-8").read()
            nuevo = IMG_RE.sub(img_a_shortcode, s)

            # poster + preload en los <video> que apunten a un mp4 del manifiesto
            def arreglar_video(mm):
                bloque = mm.group(0)
                m2 = re.search(r'src="(/assets/[^"]+\.mp4)"', bloque)
                if not m2:
                    return bloque
                poster = POSTERS.get(os.path.basename(m2.group(1)))
                if not poster:
                    return bloque
                b = bloque
                if "preload=" not in b:
                    b = b.replace("<video ", '<video preload="none" ', 1)
                if "poster=" not in b:
                    b = b.replace("<video ", f'<video poster="{poster}" ', 1)
                return b

            nuevo = re.sub(r"<video[\s\S]*?</video>", arreglar_video, nuevo)

            if nuevo != s:
                io.open(p, "w", encoding="utf-8", newline="\n").write(nuevo)
                print("actualizado:", os.path.relpath(p, RAIZ))
                cambios += 1
    print("archivos modificados:", cambios)


if __name__ == "__main__":
    main()
