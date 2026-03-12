# Chargement de la configuration depuis config.yaml.

from pathlib import Path
from typing import Any

import yaml

from src.constants import (
    BUNDLED_CONFIG_FILE,
    CONFIG_FILE,
    DEFAULT_DOWNLOADS_DIR,
    DEFAULT_URLS_FILE,
    PROJECT_ROOT,
)


def _config_file_to_use() -> Path:
    """Fichier config a utiliser: a cote de l'exe si present, sinon config embarquee."""
    if CONFIG_FILE.exists():
        return CONFIG_FILE
    if BUNDLED_CONFIG_FILE and BUNDLED_CONFIG_FILE.exists():
        return BUNDLED_CONFIG_FILE
    return CONFIG_FILE


def load_config() -> dict[str, Any]:
    """
    Charge le fichier config.yaml et retourne un dictionnaire.
    En mode exe: utilise config a cote de l'exe si presente, sinon la config embarquee.
    Les chemins relatifs sont interpretes par rapport au repertoire du projet.
    """
    path = _config_file_to_use()
    if not path.exists():
        return _default_config()

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        return _default_config()

    # Resoudre les chemins relatifs
    app_name = data.get("app_name", "YT Grab")
    urls_file = data.get("default_urls_file", "urls.txt")
    downloads_dir = data.get("downloads_dir", "downloads")
    max_concurrent = int(data.get("max_concurrent_downloads", 3))
    language = (data.get("language") or "fr").strip().lower()[:2]
    if language not in ("fr", "en", "de", "es"):
        language = "fr"
    version_check_url = (data.get("version_check_url") or "").strip()
    log_level = (data.get("log_level") or "INFO").strip().upper()
    log_file = (data.get("log_file") or "").strip()

    if not Path(urls_file).is_absolute():
        urls_file = str(PROJECT_ROOT / urls_file)
    if not Path(downloads_dir).is_absolute():
        downloads_dir = str(PROJECT_ROOT / downloads_dir)
    if log_file and not Path(log_file).is_absolute():
        log_file = str(PROJECT_ROOT / log_file)

    return {
        "app_name": app_name,
        "default_urls_file": urls_file,
        "downloads_dir": downloads_dir,
        "max_concurrent_downloads": max(1, min(max_concurrent, 8)),
        "language": language,
        "version_check_url": version_check_url,
        "log_level": log_level,
        "log_file": log_file,
    }


def _default_config() -> dict[str, Any]:
    """Configuration par defaut si le fichier est absent."""
    return {
        "app_name": "YT Grab",
        "default_urls_file": str(DEFAULT_URLS_FILE),
        "downloads_dir": str(DEFAULT_DOWNLOADS_DIR),
        "max_concurrent_downloads": 3,
        "language": "fr",
        "version_check_url": "",
        "log_level": "INFO",
        "log_file": "",
    }
