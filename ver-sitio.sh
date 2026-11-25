#!/usr/bin/env sh
# Vista local del sitio CTC Telecom (macOS / Linux)
#
#   ./ver-sitio.sh            abre el navegador en http://localhost:8080
#   ./ver-sitio.sh 9000       usa otro puerto
#   NO_OPEN=1 ./ver-sitio.sh  no abre el navegador
#
# Si el archivo no tiene permiso de ejecución:  chmod +x ver-sitio.sh
set -e
cd "$(dirname "$0")"

PORT="${1:-8080}"

abrir() {
  if command -v open >/dev/null 2>&1; then
    open "$1"              # macOS
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$1"          # Linux
  fi
}

echo ""
echo "============================================"
echo "  CTC Telecom - vista local del sitio"
echo "============================================"
echo ""

echo "Sirviendo en http://localhost:$PORT/"
if [ -z "${NO_OPEN:-}" ]; then
  (sleep 2; abrir "http://localhost:$PORT/") &
fi

if command -v hugo >/dev/null 2>&1; then
  exec hugo server --port "$PORT" --disableFastRender
fi

if command -v python3 >/dev/null 2>&1; then
  exec python3 -m http.server "$PORT" --directory public
fi

if command -v python >/dev/null 2>&1; then
  exec python -m http.server "$PORT" --directory public
fi

echo "No se encontro Hugo ni Python."
echo "Instala Hugo (https://gohugo.io/installation/) o Python y vuelve a ejecutar este archivo."
exit 1
