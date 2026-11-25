# -*- coding: utf-8 -*-
"""
Extrae el contenido del build original de Next.js (../ctctelecom.mx) hacia este
proyecto Hugo.

- 6 paginas de servicio -> front matter YAML estructurado (content/<slug>/_index.md)
- 17 paginas restantes -> HTML heredado limpio (content/<slug>/index.html)

Uso:  python tools/extraer_contenido.py
"""
"""
Genera el proyecto Hugo de ctctelecom.mx a partir del build de Next.js.
- 6 paginas de servicio -> data estructurada (YAML) + plantilla
- 17 paginas restantes + 404 -> HTML heredado limpio
"""
import io, os, re, json, sys
from lxml import html as LH, etree

AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.dirname(AQUI)                       # raiz del proyecto Hugo
SALIDA = os.path.dirname(DEST)                     # carpeta que contiene el proyecto
ROOT = os.path.join(SALIDA, "ctctelecom.mx")        # build original de Next.js
CONTENT = os.path.join(DEST, "content")

SERVICES = ["datos", "telefonia", "data-center", "infraestructura",
            "integracion", "carrier-interconnection"]

# slug: (title, description)
SEO = {
    "index": ("CTC Telecom | Red de Fibra Óptica Propia en México",
              "Operador con red de fibra óptica propia en México y LATAM. Internet dedicado, telefonía IP, data center e infraestructura para empresas."),
    "nosotros": ("Nosotros: Carrier con Red Propia | CTC Telecom",
                 "Conoce a CTC Telecom: carrier mexicano con ingeniería interna, red propia y control técnico directo. Misión, visión y equipo detrás de la operación."),
    "soporte": ("Soporte Técnico y NOC 24/7 | CTC Telecom",
                "Atención técnica especializada y Centro de Operaciones de Red (NOC) 24/7 que garantiza la máxima disponibilidad y estabilidad de tus servicios."),
    "contacto": ("Contacto: Habla con un Especialista | CTC Telecom",
                 "Ponte en contacto con CTC Telecom para recibir asesoría sobre conectividad, telefonía e infraestructura para tu empresa."),
    "looking-glass": ("Looking Glass: Diagnóstico de Red | CTC Telecom",
                      "Herramienta Looking Glass para diagnósticos de red, trazas de ruta y pruebas de conectividad desde los nodos de CTC Telecom."),
    "test-de-velocidad": ("Test de Velocidad: Mide tu Conexión | CTC Telecom",
                          "Verifica el rendimiento de tu enlace con el Test de Velocidad de CTC Telecom: latencia, descarga y carga con alta precisión."),
    "aviso-de-privacidad": ("Aviso de Privacidad | CTC Telecom",
                            "Consulta el Aviso de Privacidad de CTC Telecom. Información detallada sobre el tratamiento y protección de tus datos personales."),
    "politica-de-cookies": ("Política de Cookies | CTC Telecom",
                            "Conoce qué cookies utiliza CTC Telecom, con qué finalidad y cómo puedes administrarlas o deshabilitarlas en tu navegador."),
    "terminos-y-condiciones": ("Términos y Condiciones | CTC Telecom",
                               "Consulta los términos y condiciones del servicio de CTC Telecom: cobertura, requisitos de contratación, costos y vigencia."),
    "contrato-de-adhesion": ("Contrato de Adhesión | CTC Telecom",
                             "Contrato de adhesión de los servicios de CTC Telecom registrado ante el IFT: derechos, obligaciones y condiciones del servicio."),
    "carta-de-derechos-minimos": ("Carta de Derechos Mínimos | CTC Telecom",
                                  "Conoce tus derechos fundamentales como usuario de telecomunicaciones. CTC Telecom cumple las normativas de IFT y PROFECO."),
    "codigo-practicas-comerciales": ("Código de Prácticas Comerciales | CTC Telecom",
                                     "Políticas operativas y comerciales de CTC Telecom: servicios, coberturas, tarifas y atención al suscriptor."),
    "neutralidad-de-red": ("Neutralidad de Red | CTC Telecom",
                           "Política de Neutralidad de Red de Servicios Giga Best, S.A.P.I. de C.V.: gestión de tráfico, administración de IPs y derechos del usuario."),
    "recomendaciones-de-seguridad": ("Recomendaciones de Seguridad | CTC Telecom",
                                     "Mantén tu empresa segura: consejos prácticos sobre software, contraseñas y prevención de programas maliciosos."),
    "manual-de-pagos": ("Manual de Pagos | CTC Telecom",
                        "Guía para realizar tus pagos en CTC Telecom: métodos bancarios, transferencias y atención a facturación."),
    "infografia-derechos-minimos": ("Infografía de Derechos Mínimos | CTC Telecom",
                                    "Infografía oficial de los derechos mínimos de los usuarios de telecomunicaciones. CTC Telecom, transparencia en cada servicio."),
    "tarifas-ift": ("Tarifas IFT y Registro de Concesiones | CTC Telecom",
                    "Consulta el registro de tarifas de CTC Telecom ante el Instituto Federal de Telecomunicaciones (IFT). Transparencia y cumplimiento normativo."),
    "datos": ("Datos: Internet Dedicado, MPLS y SD-WAN | CTC Telecom",
              "Conectividad empresarial: Internet Dedicado 1:1, SDN, MPLS, SD-WAN y Lan to Lan para redes de alto desempeño, baja latencia y seguridad."),
    "telefonia": ("Telefonía IP: PBX Cloud, SIP y UCaaS | CTC Telecom",
                  "Telefonía en la nube, SIP Trunking internacional, UCaaS, telefonía celular triple carrier y roaming para empresas."),
    "data-center": ("Data Center: DCI, Cross Connect y Cloud | CTC Telecom",
                    "Conectividad a data centers: Cross Connects, DCI, acceso a ecosistemas cloud y arquitectura redundante de alta disponibilidad."),
    "infraestructura": ("Infraestructura: Fibra, Cableado y CCTV | CTC Telecom",
                        "Construcción de fibra óptica, cableado estructurado, CCTV y torres autosoportadas. Ingeniería y despliegue llave en mano."),
    "integracion": ("Soluciones Empresariales: Servidores y Red | CTC Telecom",
                    "Servidores de alto desempeño, ciberseguridad Fortinet y redes empresariales Huawei. Integración de infraestructura crítica."),
    "carrier-interconnection": ("Carrier & Interconnection: Peering y CDN | CTC Telecom",
                                "Hub de interconexión regional: Carrier Interconnection, DCI, Cloud Connect, Peering/IX y CDN para operadores y grandes empresas."),
    "404": ("Página no encontrada | CTC Telecom", ""),
}

SERVICE_TEXT = {
    "datos": ("Conectividad empresarial de alto desempeño", "Datos"),
    "telefonia": ("Telefonía empresarial flexible", "Telefonía"),
    "data-center": ("Interconexión a ecosistemas de data centers", "Data Center"),
    "infraestructura": ("Ingeniería y despliegue de infraestructura", "Infraestructura"),
    "integracion": ("Soluciones tecnológicas empresariales", "Soluciones"),
    "carrier-interconnection": ("Interconexión regional para operadores", "Carrier"),
}

CSS_HINTS = ("flex ", "text-", "bg-", "border", "w-full", "space-y", "px-", "py-",
             "mb-", "mt-", "lg:", "md:", "sm:", "gap-", "mx-auto", "rounded",
             "shadow", "items-", "justify-", "relative", "absolute", "hidden",
             "object-", "aspect-", "max-w", "scroll-mt", "container ", "overflow",
             "transition", "hover:", "inline-", "grid", "font-", "tracking-",
             "leading-", "uppercase", "duration-", "opacity-", "z-", "pl-", "pt-",
             "pb-", "inset-", "min-h", "backdrop", "strokeWidth", "strokeLinecap",
             "strokeLinejoin", "data-", "aria-", "defaultValue", "className")
TITLES = ["Características clave", "Beneficios para tu empresa", "Casos de uso",
          "¿Por qué con CTC Telecom?", "Plataformas tecnológicas", "Aplicaciones",
          "Incluye", "Ventajas", "Especificaciones"]
BADVALS = {"round", "none", "numeric", "off", "polite", "lazy", "initial", "vertical",
           "parallel", "auto", "inherit", "circle", "path", "0 0 24 24"}


# ---------------------------------------------------------------- utilidades
def clean_json_str(s):
    try:
        return json.loads('"' + s + '"')
    except Exception:
        return s


def is_item(v):
    v = v.strip()
    if len(v) < 8 or v in TITLES or v in BADVALS:
        return False
    if re.fullmatch(r"[\d\s\.\-]+", v):
        return False
    if v.startswith("$") or v.startswith("http") or v.startswith("/assets"):
        return False
    if any(h in v for h in CSS_HINTS):
        return False
    if re.match(r"^[a-z0-9\-/\.\[\]&>#%:\s]+$", v) and " " not in v:
        return False
    if not re.match(r"^[A-ZÁÉÍÓÚÑ0-9¿¡\(\"“]", v):
        return False
    if "| CTC Telecom" in v or "CTC Telecom |" in v or "width=device-width" in v:
        return False
    if re.search(r"[\{\}]", v):
        return False
    return True


CUT_MARKERS = ('"border-none bg-', '"w-full max-w-xl space-y-4"', '"w-full space-y-4"',
               '"$2c:metadata"', '"_ssgManifest"')

BULLET_RE = re.compile(r'"\$undefined"\]\}\],\s*"((?:[^"\\]|\\.)*)"')


def items_from_segment(seg):
    """Los bullets del acordeon son hijos de <li> tras el icono ($undefined)."""
    bullets = [clean_json_str(b).strip() for b in BULLET_RE.findall(seg)]
    bullets = [b for b in bullets if len(b) > 3 and not b.startswith("$")]
    if bullets:
        out, seen = [], set()
        for b in bullets:
            if b.lower() not in seen:
                seen.add(b.lower())
                out.append(b)
        return out
    return []


def rsc_segments(rsc_text, titles):
    pos = []
    for t in titles:
        for m in re.finditer(re.escape('"' + t + '"'), rsc_text):
            pos.append((m.start(), t))
    pos.sort()
    out = {}
    for i, (p, t) in enumerate(pos):
        end = pos[i + 1][0] if i + 1 < len(pos) else min(len(rsc_text), p + 7000)
        seg = rsc_text[p:end]
        items = items_from_segment(seg)
        if not items:
            # paneles sin checklist (p. ej. "Plataformas tecnológicas"): filtro general
            cut = seg
            for mk in CUT_MARKERS:
                j = cut.find(mk, 60)
                if j > 0:
                    cut = cut[:j]
            seen = set()
            for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', cut):
                v = clean_json_str(m.group(1)).strip()
                if not is_item(v):
                    continue
                k = v.lower()
                if k in seen:
                    continue
                seen.add(k)
                items.append(v)
        if items:
            out.setdefault(t, []).append(items)
    return out


def text(el):
    if isinstance(el, list):
        el = el[0] if el else None
    if el is None:
        return ""
    return " ".join(el.text_content().split())


def cls(el):
    return (el.get("class") or "") if el is not None else ""


def parse_h2(h2):
    """Devuelve (title, accent, accent_first) respetando el orden del HTML.

    Casos que aparecen en el sitio:
      <h2>Texto <span>acento</span></h2>            -> ("Texto", "acento", False)
      <h2><span>Texto</span> resto</h2>             -> ("resto", "Texto", True)
      <h2>Texto</h2>                                -> ("Texto", "", False)
    """
    before = (h2.text or "").strip()
    spans = h2.xpath("./span")
    if not spans:
        return before, "", False
    sp = spans[0]
    accent = text(sp)
    after = (sp.tail or "").strip()
    if before:
        return before, (accent + (" " + after if after else "")).strip(), False
    return after, accent, True


def yaml_scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    return json.dumps(v, ensure_ascii=False)


def to_yaml(obj, indent=0):
    pad = "  " * indent
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                out.append(f"{pad}{k}:")
                out.append(to_yaml(v, indent + 1))
            elif isinstance(v, list) and not v:
                out.append(f"{pad}{k}: []")
            elif isinstance(v, dict) and not v:
                out.append(f"{pad}{k}: {{}}")
            else:
                out.append(f"{pad}{k}: {yaml_scalar(v)}")
    elif isinstance(obj, list):
        for it in obj:
            if isinstance(it, dict):
                lines = to_yaml(it, indent + 1).split("\n")
                first = lines[0].strip()
                out.append(f"{pad}- {first}")
                out.extend(lines[1:])
            elif isinstance(it, list):
                out.append(f"{pad}-")
                out.append(to_yaml(it, indent + 1))
            else:
                out.append(f"{pad}- {yaml_scalar(it)}")
    return "\n".join(out)


def parse_service(slug):
    doc = LH.parse(os.path.join(ROOT, slug, "index.html"))
    rsc = io.open(os.path.join(ROOT, slug, "index.txt"), encoding="utf-8").read()
    page_titles = []
    for btn in doc.xpath("//main/section[position()>1]//button[@aria-controls]"):
        t = text(btn)
        if t and t not in page_titles:
            page_titles.append(t)
    segs = rsc_segments(rsc, page_titles)
    ptr = {}

    hero_el = doc.xpath("//main/section[1]")[0]
    h1 = hero_el.xpath(".//h1")[0]
    h1_spans = h1.xpath("./span")
    if len(h1_spans) >= 2:
        h1_accent, h1_title = text(h1_spans[0]), text(h1_spans[1])
    elif len(h1_spans) == 1:
        h1_title, h1_accent = "", text(h1_spans[0])
    else:
        h1_title, h1_accent, _ = parse_h2(h1)
    leads = [text(p) for p in hero_el.xpath(".//p") if text(p)]
    vsrc = hero_el.xpath(".//video/source/@src")
    vposter = hero_el.xpath(".//video/@poster")
    imgs = hero_el.xpath(".//img/@src")
    ctas = [{"label": text(a), "href": a.get("href")}
            for a in hero_el.xpath(".//a[contains(@class,'inline-flex')]")]

    sections = []
    for sec in doc.xpath("//main/section[position()>1]"):
        badge = text(sec.xpath(".//div[contains(@class,'rounded-full')][1]"))
        h2 = sec.xpath(".//h2")
        stitle, saccent, sfirst = parse_h2(h2[0]) if h2 else ("", "", False)
        img_el = sec.xpath(".//img[1]")
        img = img_el[0] if img_el else None
        media_inner = img.getparent() if img is not None else None
        media_outer = media_inner.getparent() if media_inner is not None else None
        text_outer = None
        for d in sec.xpath(".//div[contains(@class,'lg:w-1/2')]"):
            if d.xpath(".//h2"):
                text_outer = d
                break
        lead_el = sec.xpath(".//p[1]")
        row = sec.xpath(".//div[contains(@class,'gap-16')]")
        panels = []
        # el primer panel viene renderizado en el HTML (completo y exacto)
        html_bullets = [text(li) for li in sec.xpath('.//ul[contains(@class,"space-y-2")]/li')]
        for a_idx, btn in enumerate(sec.xpath(".//button[@aria-controls]")):
            t = text(btn)
            lst = segs.get(t, [])
            idx = ptr.get(t, 0)
            items = lst[idx] if idx < len(lst) else []
            ptr[t] = idx + 1
            if a_idx == 0 and html_bullets:
                items = html_bullets
            panels.append({"title": t, "items": items})
        seccion = {
            "id": sec.get("id") or "",
            "class": cls(sec),
            "row_class": cls(row[0]) if row else "",
            "badge": badge,
            "title": stitle,
            "accent": saccent,
            "lead": text(lead_el),
            "lead_class": cls(lead_el[0]) if lead_el else "",
            "media_class": cls(media_inner),
            "img_class": cls(img),
            "img": img.get("src") if img is not None else "",
            "alt": (img.get("alt") or "") if img is not None else "",
            "text_class": cls(text_outer),
            "panels": panels,
        }
        if sfirst:
            seccion["accent_first"] = True
        sections.append(seccion)

    return {
        "title": SEO[slug][0],
        "description": SEO[slug][1],
        "layout": "servicio",
        "hero": {
            "class": cls(hero_el),
            "video": vsrc[0] if vsrc else "",
            "poster": vposter[0] if vposter else "",
            "image": imgs[0] if imgs else "",
            "title": h1_title,
            "accent": h1_accent,
            "leads": leads,
            "ctas": ctas,
        },
        "sections": sections,
    }


# ------------------------------------------------- HTML heredado (resto)
DROP_TAGS = {"header", "footer"}

def clean_html(fragment):
    fragment = re.sub(r"\sdata-nimg=\"[^\"]*\"", "", fragment)
    fragment = re.sub(r"\sdata-ai-hint=\"[^\"]*\"", "", fragment)
    fragment = re.sub(r"\sdata-radix-collection-item=\"[^\"]*\"", "", fragment)
    fragment = re.sub(r"\sdata-orientation=\"[^\"]*\"", "", fragment)
    fragment = re.sub(r"\sid=\"radix-[^\"]*\"", "", fragment)
    fragment = re.sub(r"\saria-controls=\"radix-[^\"]*\"", "", fragment)
    fragment = fragment.replace("<!-- -->", "")
    fragment = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", fragment, flags=re.S)
    fragment = re.sub(r"\s(draggable|spellcheck)=\"[^\"]*\"", "", fragment)
    fragment = re.sub(r"\s{2,}", " ", fragment)
    return fragment.strip()


def legacy_page(slug):
    path = os.path.join(ROOT, slug if slug != "index" else "", "index.html")
    doc = LH.parse(path)
    main = doc.xpath("//main")[0]
    for el in main.xpath("./header|./footer|./a[contains(@class,'fixed')]"):
        el.getparent().remove(el)
    parts = [etree.tostring(c, encoding="unicode", method="html")
             for c in main if isinstance(c.tag, str)]
    html = "\n".join(parts)
    if slug == "index":
        # contadores animados del JS original: fijar valores finales
        html = re.sub(r"<span>0</span>(</span><span[^>]*>,000 KM)",
                      r"<span>24</span>\1", html)
        html = re.sub(r"<span>0</span>(</span><span[^>]*>POPS)",
                      r"<span>525</span>\1", html)
        html = re.sub(r"<span>0\.00</span>(</span><span[^>]*>% SLA)",
                      "<span>99.99</span>\\1", html)
    if slug == "test-de-velocidad":
        # el widget nPerf se cargaba por JS desde el componente React
        marker = '<div class="mt-8 pt-6 border-t border-brand-roseWhite w-full">'
        script = ('<script src="https://ws.nperf.com/partner/js?'
                  'k=b7a206b0-5678-45eb-a39b-1ddc465c91d5&amp;sp=9416" defer></script>')
        if marker in html and "ws.nperf.com" not in html:
            html = html.replace(marker, script + marker, 1)
    return clean_html(html)


def write_page(slug, body, is_home=False):
    title, desc = SEO["index" if is_home else slug]
    fm = ["---", f"title: {yaml_scalar(title)}"]
    if desc:
        fm.append(f"description: {yaml_scalar(desc)}")
    if slug == "404":
        fm.append("noindex: true")
    fm.append("---")
    if is_home:
        path = os.path.join(CONTENT, "_index.html")
    else:
        d = os.path.join(CONTENT, slug)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "index.html")
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(fm) + "\n" + body + "\n")
    return path


def write_404():
    body = '''<section class="relative pt-36 pb-24 bg-brand-midnight">
  <div class="container mx-auto px-4">
    <p class="text-brand-magenta font-black text-xs tracking-[0.35em] uppercase mb-3">Error 404</p>
    <h1 class="text-4xl md:text-5xl font-headline font-bold text-white mb-4 uppercase tracking-tight">Página no encontrada</h1>
    <div class="h-1.5 w-24 bg-brand-magenta rounded-full"></div>
  </div>
</section>
<section class="py-20">
  <div class="container mx-auto px-4 max-w-4xl">
    <p class="text-brand-purple/80 text-base leading-relaxed mb-8">La página que buscas cambió de dirección o ya no existe. Vuelve al inicio o consulta nuestros servicios.</p>
    <a href="/" class="inline-flex items-center justify-center w-56 h-12 rounded-md bg-brand-magenta text-white font-bold text-sm uppercase tracking-wider hover:bg-brand-magenta/90 transition-all">Volver al inicio</a>
  </div>
</section>'''
    d = os.path.join(CONTENT, "404")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "index.html")
    fm = ["---", f"title: {yaml_scalar(SEO['404'][0])}", "noindex: true", "---"]
    io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(fm) + "\n" + body + "\n")
    return p


def main():
    os.makedirs(CONTENT, exist_ok=True)
    written = []
    # home
    written.append(write_page("index", legacy_page("index"), is_home=True))
    # servicios
    for slug in SERVICES:
        data = parse_service(slug)
        d = os.path.join(CONTENT, slug)
        os.makedirs(d, exist_ok=True)
        fm = ["---", to_yaml(data), "---", ""]
        p = os.path.join(d, "_index.md")
        io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(fm))
        written.append(p)
    # resto
    for slug in SEO:
        if slug in SERVICES or slug in ("index",):
            continue
        if slug == "404":
            continue
        written.append(write_page(slug, legacy_page(slug)))
    for w in written:
        print("OK", w.replace(DEST, ""))

    # reporte de paneles vacios
    for slug in SERVICES:
        data = parse_service(slug)
        empties = [(s["id"], p["title"]) for s in data["sections"]
                   for p in s["panels"] if not p["items"]]
        print(f"paneles vacios {slug}: {empties}")


if __name__ == "__main__":
    main()
