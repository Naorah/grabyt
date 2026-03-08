#!/usr/bin/env bash
# Genere l'executable Linux dans dist/
# Usage: ./build.sh [--build full|slim]
#   full = avec imageio-ffmpeg (binaire plus lourd, portable)
#   slim = sans ffmpeg inclus (binaire leger, ffmpeg requis sur le systeme)
# Defaut: full

set -e

BUILD=full
for i in "$@"; do
  if [ "$i" = "--build" ]; then
    next_build=1
  elif [ -n "$next_build" ]; then
    BUILD="$i"
    next_build=
  fi
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
  echo "Activation du venv..."
  # shellcheck source=venv/bin/activate
  . venv/bin/activate
fi

echo "Installation des dependances de build..."
pip install pyinstaller pillow -q

echo "Generation de l'icone..."
if python3 scripts/build_icon.py 2>/dev/null || true; then
  : # ok
else
  echo "Attention: assets/icon.ico absent (optionnel)."
fi

if [ "$BUILD" = "slim" ]; then
  echo "Build SLIM: sans imageio-ffmpeg. ffmpeg doit etre installe sur le systeme."
  pyinstaller build_slim.spec --noconfirm
else
  echo "Build FULL: avec imageio-ffmpeg."
  pip install imageio-ffmpeg -q
  pyinstaller build_full.spec --noconfirm
fi

echo ""
if [ -f "dist/GrabYT" ]; then
  chmod +x dist/GrabYT
  echo "Executable genere: dist/GrabYT"
else
  echo "Echec du build."
  exit 1
fi
