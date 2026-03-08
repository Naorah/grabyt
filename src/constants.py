# Constantes et chemins par defaut du projet.

import sys
from pathlib import Path

# Repertoire racine: dossier de l'exe en mode PyInstaller, sinon parent de src/
if getattr(sys, "frozen", False):
    PROJECT_ROOT = Path(sys.executable).parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
DEFAULT_URLS_FILE = PROJECT_ROOT / "urls.txt"
DEFAULT_DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
