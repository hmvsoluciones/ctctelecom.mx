# Análisis externo (HMV Soluciones, 24-11-2026) y estado en este repositorio

Documento de referencia: [`referencia/analisis-hmv-2026-11-24.html`](referencia/analisis-hmv-2026-11-24.html)
(auditoría pública del sitio anterior en Next.js: 12 páginas revisadas, 16 mejoras priorizadas).

Este archivo traduce esas 16 mejoras al estado real del proyecto Hugo, para no repetir trabajo y
para que el equipo sepa qué queda abierto.

Leyenda: ✅ hecho · 🟡 parcial · ⬜ pendiente · 🚫 fuera de alcance de esta entrega

| # | Mejora (informe HMV) | Prioridad | Estado | Dónde / nota |
|---|---|---|---|---|
| 1 | Unificar NAP (dirección, teléfonos, email) | P0 | 🟡 | Un solo juego de datos en `data/site.yaml` para header, footer y WhatsApp. **Falta** decidir con CTC: el cuerpo de `/contacto/` y el Aviso de Privacidad (texto legal) traen direcciones distintas de CDMX. Requiere validación de negocio. |
| 2 | CTA comercial en el hero de la home | P0 | ⬜ | El hero mantiene «Peering DB» y «Test de Velocidad». Cambiarlo es una decisión de contenido/comercial. |
| 3 | Crear `robots.txt` y `sitemap.xml` | P0 | ✅ | `static/robots.txt` + `layouts/sitemap.xml` (23 URLs, sin `noindex`). Enlazado desde `<head>`. |
| 4 | Formulario B2B que cualifique | P1 | ⬜ | Sigue siendo el formulario heredado (sin `action` ni `name`). Requiere definir destino (CRM / servicio de formularios). |
| 5 | Unificar la cifra de SLA y fijar contadores | P1 | 🟡 | Contadores ya son estáticos: **24,000 km**, **525 PoPs**, **99.99 %**. Queda un «99.999 %» en la tarjeta de la portada: es una decisión de negocio cuál cifra se publica. |
| 6 | PeeringDB a HTTPS y revisar teléfonos LATAM | P1 | 🟡 | Enlace corregido a `https://www.peeringdb.com/net/41652`. Teléfonos de Chile/Argentina/Brasil siguen como estaban: falta confirmación de CTC. |
| 7 | Verificador de cobertura / factibilidad | P1 | ⬜ | Requiere datos de cobertura por zona. |
| 8 | Optimizar imágenes y medir rendimiento | P1 | ✅ | Ver [`performance.md`](performance.md): `public/` 103 → 37 MB, portada 43.4 → 4.5 MB. |
| 9 | Página por subservicio clave | P1 | ⬜ | Sigue el modelo de 5 páginas con secciones + anclas. |
| 10 | Renombrar `/integracion/` → `/soluciones-empresariales/` | P1 | ⬜ | Se conservó la URL a propósito para no perder posicionamiento; requiere 301 y aprobación. |
| 11 | Meta descripciones y datos estructurados | P1 | ✅ | Descripción única por página, canonical, Open Graph, Twitter, `Organization`, `BreadcrumbList`, `Service`/`OfferCatalog`. Certificado y cabeceras del servidor: pendiente de verificar en hosting. |
| 12 | Reforzar `/soporte/` | P2 | ⬜ | Contenido heredado. |
| 13 | Mostrar el contenido de los acordeones + casos de éxito | P2 | 🟡 | Acordeones resueltos: los 98 paneles están en el HTML con `<details>` (Google los lee). Casos de éxito: pendientes de insumo. |
| 14 | Sección «por sector» | P2 | ⬜ | Requiere contenido nuevo. |
| 15 | Medición de conversiones (GA4/GTM) | P2 | ⬜ | No hay analítica instalada. |
| 16 | Rediseño mayor | P3 | 🚫 | Solo con métricas de conversión reales. |

## Lo que el informe daba por roto y ya no aplica

- **robots.txt / sitemap.xml respondían 404** → ahora existen y se generan en cada build.
- **Acordeones colapsados ocultaban contenido** → el contenido está en el HTML (98 paneles) y se
  abre sin JavaScript.
- **Imágenes que tardaban en cargar** → WebP + `srcset` + `width`/`height` + lazy loading.
- **Contadores animados con cifras inestables** → valores fijos en el HTML.
- **Sin metadatos SEO** → canonical, OG, Twitter y JSON-LD en las 23 páginas.
- **Enlace PeeringDB por HTTP** → HTTPS.

## Lo que sigue siendo cierto del informe

- El sitio **no tiene CTA comercial** en el hero ni cualificación de leads.
- **Datos de contacto inconsistentes** entre páginas y con el sitio residencial.
- **`/soporte/` es una página delgada** y no hay casos de éxito ni prueba social.
- **Sin analítica**: no se puede medir si los cambios anteriores mejoran algo.
- **Sin verificador de cobertura**, que es el lead magnet natural de un carrier.
