# Caché y compresión en el servidor

El sitio es estático: el build en `public/` se sube por FTP. Estas cabeceras **no** las controla Hugo;
hay que configurarlas en el hosting. Pregunta primero al proveedor qué servidor es (Apache, Nginx,
LiteSpeed o un CDN delante) antes de subir nada.

Sin esto, el navegador vuelve a descargar imágenes y videos en cada visita, y todo el trabajo de
optimización se desaprovecha.

---

## Reglas recomendadas

| Recurso | `Cache-Control` |
|---|---|
| HTML | `no-cache` (o `max-age=0, must-revalidate`) |
| `/assets/opt/*.webp`, `/assets/*.jpg`, `*.png`, `*.svg` | `public, max-age=31536000, immutable` |
| `/assets/*.mp4` | `public, max-age=31536000` |
| `/assets/css/*.css` | `public, max-age=31536000` |
| `sitemap.xml`, `robots.txt` | `public, max-age=3600` |

Compresión: **gzip** o, mejor, **brotli** para `text/html`, `text/css`, `application/javascript`,
`application/json`, `image/svg+xml`. No comprimir `.mp4`, `.webp`, `.jpg`, `.png` (ya están comprimidos).

> Nota: hoy los nombres de los assets no llevan hash (`site.css`, `foto.jpg`), así que un
> `immutable` a un año obliga a renombrar el archivo cuando cambie. Si prefieres no renombrar, usa
> `max-age=604800` (una semana) para imágenes y CSS.

---

## Apache (`.htaccess` en la raíz del sitio)

```apache
# --- Compresión ---
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml \
    application/javascript application/json image/svg+xml
</IfModule>

# --- Caché ---
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html                 "access plus 0 seconds"
  ExpiresByType text/css                  "access plus 1 year"
  ExpiresByType image/webp                "access plus 1 year"
  ExpiresByType image/jpeg                "access plus 1 year"
  ExpiresByType image/png                 "access plus 1 year"
  ExpiresByType image/svg+xml             "access plus 1 year"
  ExpiresByType video/mp4                 "access plus 1 year"
  ExpiresByType application/xml           "access plus 1 hour"
</IfModule>

# --- 404 propio ---
ErrorDocument 404 /404.html

# --- HTTPS + sin www (ajusta al dominio real) ---
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</IfModule>
```

---

## Nginx

```nginx
server {
    root /var/www/ctctelecom.mx;
    index index.html;

    gzip on;
    gzip_types text/html text/css application/javascript application/json image/svg+xml;
    gzip_min_length 1024;

    location /assets/ {
        add_header Cache-Control "public, max-age=31536000, immutable";
        try_files $uri =404;
    }

    location ~* \.html$ {
        add_header Cache-Control "no-cache";
    }

    location / {
        try_files $uri $uri/ $uri/index.html =404;
    }

    error_page 404 /404.html;
}
```

---

## Netlify / Cloudflare Pages

Archivo `_headers` en la raíz de `public/` (o en `static/_headers` si quieres versionarlo):

```
/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: no-cache
```

---

## Verificación (2 minutos, tras desplegar)

```bash
curl -I https://ctctelecom.mx/assets/opt/servicios-960.webp
curl -I -H "Accept-Encoding: gzip" https://ctctelecom.mx/
```

Deben aparecer `cache-control` con `max-age` largo y `content-encoding: gzip` (o `br`).
