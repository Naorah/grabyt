# Cree des dossiers full-{lang} et slim-{lang} dans dist/ avec l'exe et un config.yaml (language: lang).
# A lancer apres build full et build slim. Supporte Windows (.exe) et Unix (sans extension).

import shutil
import sys
from pathlib import Path

LANGS = ("fr", "en", "de", "es")
DIST = Path(__file__).resolve().parent.parent.parent / "dist"
FULL_NAME = "GrabYT-full"
SLIM_NAME = "GrabYT-slim"
EXE_SUFFIX = ".exe" if sys.platform == "win32" else ""

CONFIG_TEMPLATE = """# Configuration par defaut pour la langue {language}.
app_name: "GRABYT"
default_urls_file: "urls.txt"
downloads_dir: "downloads"
max_concurrent_downloads: 3
language: "{language}"
version_check_url: ""
log_level: "INFO"
log_file: ""
"""


def main() -> None:
    full_exe = DIST / f"{FULL_NAME}{EXE_SUFFIX}"
    slim_exe = DIST / f"{SLIM_NAME}{EXE_SUFFIX}"
    if not full_exe.exists():
        print(f"Manquant: {full_exe}. Lancez d'abord le build full.")
        sys.exit(1)
    if not slim_exe.exists():
        print(f"Manquant: {slim_exe}. Lancez d'abord le build slim.")
        sys.exit(1)

    for lang in LANGS:
        for kind, exe_path in (("full", full_exe), ("slim", slim_exe)):
            out_dir = DIST / f"{kind}-{lang}"
            out_dir.mkdir(parents=True, exist_ok=True)
            dest_exe = out_dir / exe_path.name
            shutil.copy2(exe_path, dest_exe)
            config_dir = out_dir / "config"
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / "config.yaml"
            config_file.write_text(
                CONFIG_TEMPLATE.format(language=lang),
                encoding="utf-8",
            )
            print(f"  {out_dir.relative_to(DIST)}/ ({exe_path.name} + config language={lang})")

    print(f"Builds par langue crees dans {DIST}.")


if __name__ == "__main__":
    main()

