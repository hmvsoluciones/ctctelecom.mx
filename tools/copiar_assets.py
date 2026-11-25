# -*- coding: utf-8 -*-
"""
Copia a static/assets todos los medios referenciados por el build original de
Next.js (../ctctelecom.mx): atributos src/href/poster, estilos en linea
(background-image) y el payload de React (*.txt).

Uso:  python tools/copiar_assets.py         (Windows)
      python3 tools/copiar_assets.py        (macOS / Linux)
"""
import os
import re
import io
import glob
import shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.dirname(AQUI)
SALIDA = os.path.dirname(DEST)
SRC = os.path.join(SALIDA, "ctctelecom.mx")

EXT = (".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".avif",
       ".mp4", ".webm", ".ico")

# Ojo: dentro de HTML el nombre puede venir escapado con &quot; / &#x27;
PATRON = re.compile(r'/assets/([^"\'\s\)>,;\\&]+)')


def archivos_fuente():
    for p in glob.glob(os.path.join(SRC, "**", "*.html"), recursive=True):
        if "_next" in p or os.sep + "assets" + os.sep in p:
            continue
        yield p
    for p in glob.glob(os.path.join(SRC, "**", "*.txt"), recursive=True):
        if "_next" in p:
            continue
        yield p
    for p in glob.glob(os.path.join(SRC, "_next", "**", "*.css"), recursive=True):
        yield p


def main():
    refs = set()
    for p in archivos_fuente():
        s = io.open(p, encoding="utf-8", errors="ignore").read()
        for m in PATRON.finditer(s):
            nombre = m.group(1)
            # recorta escapes residuales al final (p. ej. "map.svg&quot")
            for corte in ("&quot", "&#x27", "&#39", "&amp"):
                if corte in nombre:
                    nombre = nombre.split(corte)[0]
            if nombre.lower().endswith(EXT):
                refs.add(nombre)

    copiados, faltantes, total = 0, [], 0
    for r in sorted(refs):
        origen = os.path.join(SRC, "assets", r)
        if not os.path.isfile(origen):
            faltantes.append(r)
            continue
        destino = os.path.join(DEST, "static", "assets", r)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        if not os.path.isfile(destino) or os.path.getsize(destino) != os.path.getsize(origen):
            shutil.copy2(origen, destino)
            copiados += 1
        total += os.path.getsize(origen)

    print("referencias distintas:", len(refs))
    print("copiados/actualizados:", copiados)
    print("faltantes en el origen:", faltantes if faltantes else "ninguno")
    print("peso referenciado: %.1f MB" % (total / 1048576))


if __name__ == "__main__":
    main()
