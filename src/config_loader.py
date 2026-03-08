# Chargement de la configuration depuis config.yaml.

from pathlib import Path
from typing import Any

import yaml

from src.constants import CONFIG_FILE, DEFAULT_DOWNLOADS_DIR, DEFAULT_URLS_FILE, PROJECT_ROOT


def load_config() -> dict[str, Any]:
    """
    Charge le fichier config.yaml et retourne un dictionnaire.
    Les chemins relatifs sont interpretes par rapport au repertoire du projet.
    """
    if not CONFIG_FILE.exists():
        return _default_config()

    with open(CONFIG_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        return _default_config()

    # Resoudre les chemins relatifs
    app_name = data.get("app_name", "YT Grab")
    urls_file = data.get("default_urls_file", "urls.txt")
    downloads_dir = data.get("downloads_dir", "downloads")

    if not Path(urls_file).is_absolute():
        urls_file = str(PROJECT_ROOT / urls_file)
    if not Path(downloads_dir).is_absolute():
        downloads_dir = str(PROJECT_ROOT / downloads_dir)

    return {
        "app_name": app_name,
        "default_urls_file": urls_file,
        "downloads_dir": downloads_dir,
    }


def _default_config() -> dict[str, Any]:
    """Configuration par defaut si le fichier est absent."""
    return {
        "app_name": "YT Grab",
        "default_urls_file": str(DEFAULT_URLS_FILE),
        "downloads_dir": str(DEFAULT_DOWNLOADS_DIR),
    }
