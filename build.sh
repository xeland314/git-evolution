#!/usr/bin/env bash
# Compila git-evolution como un binario único usando uv + PyInstaller.
# Uso: ./build.sh
set -euo pipefail

cd "$(dirname "$0")"

echo "==> Creando entorno de build con uv..."
uv venv .venv-build --quiet

echo "==> Instalando dependencias (plotly + pyinstaller)..."
uv pip install --python .venv-build plotly pyinstaller --quiet

echo "==> Compilando binario (onefile)..."
.venv-build/bin/pyinstaller \
    --onefile \
    --name git-evolution \
    --add-data "template.html:." \
    --collect-submodules plotly \
    --noconfirm \
    --clean \
    main.py

echo ""
echo "Listo. Binario disponible en: dist/git-evolution"
