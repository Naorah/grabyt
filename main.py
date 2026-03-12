# Point d'entree de l'application.
# Lance l'interface Qt avec le nom et les options charges depuis config/config.yaml.

import os
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMessageBox

from src.config_loader import load_config
from src.i18n import get_default_urls_content, set_language, t
from src.logger import setup_logging
from src.ui.icons import get_app_icon
from src.ui.main_window import MainWindow
from src.version import CURRENT_VERSION, fetch_latest_version, is_newer


def _base_dir() -> str:
    """Repertoire de base pour les chemins relatifs (exe ou projet)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _ensure_default_urls_file(config: dict) -> None:
    """Cree le fichier URLs par defaut s'il n'existe pas, avec instructions commentees (selon la langue)."""
    urls_file = config.get("default_urls_file", "urls.txt")
    path = os.path.join(_base_dir(), urls_file) if not os.path.isabs(urls_file) else urls_file
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(get_default_urls_content())


def _check_new_version(window: MainWindow, version_url: str) -> None:
    """Verification asynchrone: affiche un message si une nouvelle version est disponible."""
    if not version_url:
        return
    latest = fetch_latest_version(version_url)
    if latest and is_newer(latest, CURRENT_VERSION):
        msg = t("new_version", version=latest)
        QMessageBox.information(window, window.windowTitle(), msg)


def main() -> None:
    config = load_config()
    set_language(config.get("language", "fr"))
    _ensure_default_urls_file(config)

    setup_logging(
        level=config.get("log_level", "INFO"),
        log_file=config.get("log_file") or None,
    )

    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 9)
    app.setFont(font)

    icon = get_app_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)

    window = MainWindow()
    window.setWindowTitle(config["app_name"])
    if not icon.isNull():
        window.setWindowIcon(icon)
    window.show()

    version_url = config.get("version_check_url", "").strip()
    if version_url:
        QTimer.singleShot(1500, lambda: _check_new_version(window, version_url))

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
