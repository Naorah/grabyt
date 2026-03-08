# Genere assets/icon.ico a partir du SVG de l'application (pour l'exe).
# Lance avec: python scripts/build_icon.py
# Necessite: PyQt6, Pillow

import io
import sys
from pathlib import Path

# Ajouter la racine au path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtCore import QByteArray, QBuffer, QIODevice, QRectF
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QApplication

from src.ui.icons import SVG_APP


def main() -> None:
    app = QApplication(sys.argv)
    color = "#2c2c2c"
    colored = SVG_APP.replace(b"currentColor", color.encode())
    renderer = QSvgRenderer(QByteArray(colored))

    size = 256
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(0)
    painter = QPainter(image)
    renderer.render(painter, QRectF(0, 0, size, size))
    painter.end()

    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")
    buffer.close()

    from PIL import Image

    pil_img = Image.open(io.BytesIO(buffer.data().data())).convert("RGBA")

    out_dir = project_root / "assets"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "icon.ico"
    pil_img.save(
        out_path,
        format="ICO",
        sizes=[(256, 256), (48, 48), (32, 32), (16, 16)],
    )
    print(f"Icone generee: {out_path}")


if __name__ == "__main__":
    main()
