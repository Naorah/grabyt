# Icones SVG pour la barre de titre et l'application.
# L'icône de l'app est chargée depuis assets/favicon.svg en priorité, sinon assets/icon.ico.

import os
import sys

from PyQt6.QtCore import QByteArray, QRectF, QSize
from PyQt6.QtGui import QIcon, QImage, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer


def _assets_dir() -> str:
    """Répertoire assets (à la racine du projet ou dans le bundle PyInstaller si frozen)."""
    if getattr(sys, "frozen", False):
        # PyInstaller extrait les datas dans _MEIPASS (onefile) ou à côté de l'exe (onedir)
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        return os.path.join(base, "assets")
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(root, "assets")


def _app_icon_svg_path() -> str | None:
    """Chemin vers assets/favicon.svg si le fichier existe (prioritaire)."""
    path = os.path.join(_assets_dir(), "favicon.svg")
    return path if os.path.isfile(path) else None


def _app_icon_path() -> str | None:
    """Chemin vers assets/icon.ico si le fichier existe (fallback)."""
    path = os.path.join(_assets_dir(), "icon.ico")
    return path if os.path.isfile(path) else None


def _load_app_icon_svg_bytes() -> bytes | None:
    """Charge le contenu de assets/favicon.svg."""
    path = _app_icon_svg_path()
    if not path:
        return None
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        return None


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

# Icone historique (horloge) pour le bouton en haut a gauche
SVG_HISTORY = b"""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 21q-3.15 0-5.575-1.912T3.275 14.2q-.1-.375.15-.687t.675-.363q.4-.05.725.15t.45.6q.6 2.25 2.475 3.675T12 19q2.925 0 4.963-2.037T19 12t-2.037-4.962T12 5q-1.725 0-3.225.8T6.25 8H8q.425 0 .713.288T9 9t-.288.713T8 10H4q-.425 0-.712-.288T3 9V5q0-.425.288-.712T4 4t.713.288T5 5v1.35q1.275-1.6 3.113-2.475T12 3q1.875 0 3.513.713t2.85 1.924t1.925 2.85T21 12t-.712 3.513t-1.925 2.85t-2.85 1.925T12 21m1-9.4l2.5 2.5q.275.275.275.7t-.275.7t-.7.275t-.7-.275l-2.8-2.8q-.15-.15-.225-.337T11 11.975V8q0-.425.288-.712T12 7t.713.288T13 8z"/></svg>"""

APP_ICON_SIZE = 20


def get_app_icon() -> QIcon:
    """
    Retourne l'icône application pour setWindowIcon.
    Priorité: assets/favicon.svg, puis assets/icon.ico.
    """
    svg_bytes = _load_app_icon_svg_bytes()
    if svg_bytes:
        icon = QIcon()
        for s in (16, 32, 48, 64, 128, 256):
            pix = _pixmap_from_svg(svg_bytes, s, "#000")
            if not pix.isNull():
                icon.addPixmap(pix)
        if not icon.isNull():
            return icon
    path = _app_icon_path()
    return QIcon(path) if path else QIcon()


def get_app_icon_pixmap(size: int = APP_ICON_SIZE, color: str = "#2c2c2c") -> QPixmap:
    """
    Retourne le pixmap de l'icone application pour le header (barre de titre).
    Priorité: assets/favicon.svg, puis assets/icon.ico, sinon SVG embarqué.
    """
    svg_bytes = _load_app_icon_svg_bytes()
    if svg_bytes:
        pix = _pixmap_from_svg(svg_bytes, size, "#000")
        if not pix.isNull():
            return pix
    path = _app_icon_path()
    if path:
        icon = QIcon(path)
        if not icon.isNull():
            pix = icon.pixmap(QSize(size, size))
            if not pix.isNull():
                return pix
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


def get_history_icon(size: int = 20, color: str = "#2c2c2c") -> QIcon:
    """Icone pour le bouton historique (horloge) en haut a gauche."""
    return _icon_from_svg(SVG_HISTORY, size, color)
