# -*- coding: utf-8 -*-
"""
Mide el peso de cada página del build (HTML + CSS + imágenes + video referenciados).

Uso (desde la raíz del proyecto, con el sitio ya compilado):
    python tools/peso.py
    python3 tools/peso.py

Opcional:
    python tools/peso.py --top 15
"""
import os
import re
import sys
import io

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(RAIZ, "public")

EXT_ASSET = (".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp",
             ".avif", ".mp4", ".webm", ".ico", ".woff2", ".woff")


def kb(n):
    return n / 1024


def peso_archivo(rel):
    p = os.path.join(PUB, rel.lstrip("/").replace("/", os.sep))
    return os.path.getsize(p) if os.path.isfile(p) else 0


def paginas():
    for dirpath, _, files in os.walk(PUB):
        if "index.html" in files:
            yield dirpath, os.path.join(dirpath, "index.html")


def referencias(html):
    """Separa lo que descarga un navegador moderno (WebP) de los respaldos.

    Devuelve (estimado, todo). `estimado` usa la variante WebP más grande de cada
    <picture> y descarta el original que solo sirve de respaldo.
    """
    todo = set()
    estimado = set()

    # 1) bloques <picture>: cuenta la variante webp más grande, no el fallback
    for m in re.finditer(r"<picture>(.*?)</picture>", html, re.S):
        bloque = m.group(1)
        webps = [u for u in re.findall(r"/assets/opt/[^\"'\s,]+\.webp", bloque)]
        if webps:
            mejor = max(webps, key=lambda u: int(re.search(r"-(\d+)\.webp$", u).group(1)))
            estimado.add(mejor)
            todo.add(mejor)
        for u in re.findall(r'src="([^"]+)"', bloque):
            todo.add(u)

    resto = re.sub(r"<picture>.*?</picture>", "", html, flags=re.S)

    for m in re.finditer(r'(?:src|href|poster)="([^"]+)"', resto):
        u = m.group(1).split("#")[0].split("?")[0]
        if u.startswith("/") and u.lower().endswith(EXT_ASSET):
            todo.add(u)
            estimado.add(u)
    for m in re.finditer(r'url\((["\']?)(/assets/[^)"\']+)\1\)', resto):
        todo.add(m.group(2))
        estimado.add(m.group(2))

    return estimado, todo


def main():
    top = 10
    if "--top" in sys.argv:
        top = int(sys.argv[sys.argv.index("--top") + 1])

    filas, globales = [], {}
    for dirpath, html_path in paginas():
        rel = os.path.relpath(dirpath, PUB).replace("\\", "/")
        url = "/" if rel == "." else "/" + rel + "/"
        html = io.open(html_path, encoding="utf-8", errors="ignore").read()
        propios = os.path.getsize(html_path)
        est, todo = referencias(html)
        peso_refs = sum(peso_archivo(r) for r in est)
        filas.append((url, propios, peso_refs, len(est)))
        for r in est:
            globales[r] = peso_archivo(r)

    filas.sort(key=lambda f: -(f[1] + f[2]))
    print(f"{'página':32} {'HTML':>8} {'assets':>10} {'total':>10}  refs")
    print("-" * 74)
    for url, h, a, n in filas[:top]:
        print(f"{url:32} {kb(h):7.0f}K {kb(a):9.0f}K {kb(h+a):9.0f}K  {n}")

    total_public = 0
    for dirpath, _, files in os.walk(PUB):
        for f in files:
            total_public += os.path.getsize(os.path.join(dirpath, f))

    print()
    print("assets más pesados referenciados:")
    for r, s in sorted(globales.items(), key=lambda x: -x[1])[:8]:
        print(f"  {kb(s):8.0f}K  {r}")

    print()
    print(f"public/ completo: {total_public/1048576:.1f} MB")
    print(f"páginas medidas: {len(filas)}")


if __name__ == "__main__":
    main()
