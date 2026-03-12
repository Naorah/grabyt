# Constantes et chemins par defaut du projet.

import sys
from pathlib import Path

# Repertoire racine: dossier de l'exe en mode PyInstaller, sinon parent de src/
if getattr(sys, "frozen", False):
    PROJECT_ROOT = Path(sys.executable).parent
    # Config embarquee (extractee par PyInstaller dans _MEIPASS)
    _MEIPASS = Path(getattr(sys, "_MEIPASS", PROJECT_ROOT))
    BUNDLED_CONFIG_FILE = _MEIPASS / "config" / "config.yaml"
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    BUNDLED_CONFIG_FILE = Path()

CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
DEFAULT_URLS_FILE = PROJECT_ROOT / "urls.txt"
DEFAULT_DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
