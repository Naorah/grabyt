#!/usr/bin/env bash
# Genere les exe FULL et SLIM puis cree pour chaque langue (fr, en, de, es)
# un dossier dist/full-{lang} et dist/slim-{lang} avec l'exe et config/config.yaml.
# Usage: scripts/packaging/build-all.sh

set -e
cd "$(dirname "$0")/../.."

if [ ! -f "venv/bin/activate" ] && [ ! -f ".venv/bin/activate" ]; then
    echo "Creez un venv puis: pip install pyinstaller pillow"
    exit 1
fi

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    source .venv/bin/activate
fi

pip install pyinstaller pillow -q

echo "Generation de l'icone..."
python scripts/build/build_icon.py
if [ ! -f "assets/icon.ico" ]; then
    echo "Attention: assets/icon.ico absent (optionnel sur Linux/Mac)."
fi

echo ""
echo "=== Build FULL ==="
pip install imageio-ffmpeg -q
pyinstaller scripts/build/build_full.spec --noconfirm

echo ""
echo "=== Build SLIM ==="
pyinstaller scripts/build/build_slim.spec --noconfirm

echo ""
echo "=== Packs par langue (fr, en, de, es) ==="
python scripts/packaging/prepare_lang_builds.py

echo ""
echo "Termine: dist/GrabYT-full, dist/GrabYT-slim"
echo "Packs: dist/full-fr, dist/full-en, dist/full-de, dist/full-es"
echo "      dist/slim-fr, dist/slim-en, dist/slim-de, dist/slim-es"

