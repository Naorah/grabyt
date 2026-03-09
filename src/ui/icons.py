# Icones SVG pour la barre de titre et l'application.

from PyQt6.QtCore import QByteArray, QRectF
from PyQt6.QtGui import QIcon, QImage, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer


def _pixmap_from_svg(svg_bytes: bytes, size: int, color: str) -> QPixmap:
    """Rend un SVG en QPixmap (remplace currentColor par color)."""
    colored = svg_bytes.replace(b"currentColor", color.encode())
    renderer = QSvgRenderer(QByteArray(colored))
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(0)
    painter = QPainter(image)
    renderer.render(painter, QRectF(0, 0, size, size))
    painter.end()
    return QPixmap.fromImage(image)


def _icon_from_svg(svg_bytes: bytes, size: int = 16, color: str = "#e6e6e6") -> QIcon:
    """Construit un QIcon a partir de donnees SVG (couleur pour fond sombre)."""
    return QIcon(_pixmap_from_svg(svg_bytes, size, color))


SVG_MINIMIZE = b"""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M7 21q-.425 0-.712-.288T6 20t.288-.712T7 19h10q.425 0 .713.288T18 20t-.288.713T17 21z"/></svg>"""

SVG_MAXIMIZE = b"""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M19 3H5c-1.11 0-2 .89-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2m0 2v14H5V5z"/></svg>"""

SVG_CLOSE = b"""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="m12 13.4l-4.9 4.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7l4.9-4.9l-4.9-4.9q-.275-.275-.275-.7t.275-.7t.7-.275t.7.275l4.9 4.9l4.9-4.9q.275-.275.7-.275t.7.275t.275.7t-.275.7L13.4 12l4.9 4.9q.275.275.275.7t-.275.7t-.7.275t-.7-.275z"/></svg>"""

ICON_SIZE = 12


# Icone de l'application (affichée a gauche du titre dans le header)
SVG_APP = b"""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10.803 9.997L9.75 7.69C9.48 7.032 9.12 6.6 8.4 6.6m0 0H5.25C3.711 6.6 3 7.05 3 8.85c.075 1.614.827 3.266 1.915 4.462M8.4 6.6c0-1.395.216-3.6-1.8-3.6c-1.8 0-2.25 2.029-2.25 3.676M14 13.21l2.311 1.04c.657.27 1.089.63 1.089 1.35m0 0v3.15c0 1.539-.45 2.25-2.25 2.25c-1.614-.076-3.264-.824-4.459-1.912M17.4 15.6c1.395 0 3.6-.216 3.6 1.8c0 1.8-2.029 2.25-3.676 2.25M5.34 13l5.211-2.89c1.701-.945 4.311 1.602 3.339 3.34l-2.898 5.228C9.12 22.044 1.911 14.908 5.34 13"/></svg>"""

# Icone "ouvrir le fichier texte" (bouton circulaire a cote du champ fichier URLs)
SVG_OPEN_FILE = b"""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path d="M14.186 2.753v3.596c0 .487.195.955.54 1.3a1.85 1.85 0 0 0 1.306.539h4.125"/><path d="M20.25 8.568v8.568a4.25 4.25 0 0 1-1.362 2.97a4.28 4.28 0 0 1-3.072 1.14h-7.59a4.3 4.3 0 0 1-3.1-1.124a4.26 4.26 0 0 1-1.376-2.986V6.862a4.25 4.25 0 0 1 1.362-2.97a4.28 4.28 0 0 1 3.072-1.14h5.714a3.5 3.5 0 0 1 2.361.905l2.96 2.722a2.97 2.97 0 0 1 1.031 2.189M7.647 7.647h3.265M7.647 12h8.706m-8.706 4.353h8.706"/></g></svg>"""

APP_ICON_SIZE = 20


def get_app_icon_pixmap(size: int = APP_ICON_SIZE, color: str = "#2c2c2c") -> QPixmap:
    """
    Retourne le pixmap de l'icone application pour le header.
    A appeler apres creation de QApplication.
    """
    return _pixmap_from_svg(SVG_APP, size, color)


def get_title_bar_icons() -> tuple[QIcon, QIcon, QIcon]:
    """
    Retourne les icones minimize, maximize, close.
    A appeler apres creation de QApplication (sinon QPixmap echoue).
    """
    return (
        _icon_from_svg(SVG_MINIMIZE, ICON_SIZE),
        _icon_from_svg(SVG_MAXIMIZE, ICON_SIZE),
        _icon_from_svg(SVG_CLOSE, ICON_SIZE),
    )


def get_open_file_icon(size: int = 20, color: str = "#2c2c2c") -> QIcon:
    """Icone pour le bouton 'ouvrir le fichier URLs' (bouton circulaire)."""
    return _icon_from_svg(SVG_OPEN_FILE, size, color)
