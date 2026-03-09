# Point d'entree de l'application.
# Lance l'interface Qt avec le nom et les options charges depuis config/config.yaml.

import os
import sys

from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication

from src.config_loader import load_config
from src.ui.main_window import MainWindow

# Contenu par defaut du fichier URLs (lignes # = commentaires, ignorees par le parser)
DEFAULT_URLS_CONTENT = """# Liste d'URLs YouTube (une par ligne).
# Les lignes commençant par # sont ignorées.
# Exemple :
# https://www.youtube.com/watch?v=xxxxx
"""


def _base_dir() -> str:
    """Repertoire de base pour les chemins relatifs (exe ou projet)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _ensure_default_urls_file(config: dict) -> None:
    """Cree le fichier URLs par defaut s'il n'existe pas, avec instructions commentees."""
    urls_file = config.get("default_urls_file", "urls.txt")
    path = os.path.join(_base_dir(), urls_file) if not os.path.isabs(urls_file) else urls_file
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(DEFAULT_URLS_CONTENT)


def _app_icon() -> QIcon:
    """Icône pour la fenêtre et la barre des tâches (Windows)."""
    if getattr(sys, "frozen", False):
        return QIcon(sys.executable)
    root = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root, "assets", "icon.ico")
    return QIcon(path) if os.path.isfile(path) else QIcon()


def main() -> None:
    config = load_config()
    _ensure_default_urls_file(config)
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 9)
    app.setFont(font)

    icon = _app_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)

    window = MainWindow()
    window.setWindowTitle(config["app_name"])
    if not icon.isNull():
        window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
