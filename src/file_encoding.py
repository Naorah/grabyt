# Detection d'encodage pour les fichiers texte (UTF-8, UTF-8 BOM, CP1252).

from pathlib import Path


ENCODINGS = ["utf-8-sig", "utf-8", "cp1252"]


def detect_file_encoding(filepath: str | Path) -> str:
    """
    Detecte l'encodage d'un fichier en essayant UTF-8 BOM, UTF-8, puis CP1252.
    Retourne le premier encodage qui decode sans erreur.
    """
    path = Path(filepath)
    if not path.exists():
        return "utf-8"
    raw = path.read_bytes()
    for encoding in ENCODINGS:
        try:
            raw.decode(encoding)
            return encoding
        except (UnicodeDecodeError, LookupError):
            continue
    return "utf-8"


def read_text_auto_encoding(filepath: str | Path) -> tuple[str, str]:
    """
    Lit le contenu d'un fichier en detectant l'encodage.
    Retourne (contenu, encodage_utilise).
    """
    path = Path(filepath)
    if not path.exists():
        return "", "utf-8"
    encoding = detect_file_encoding(path)
    return path.read_text(encoding=encoding), encoding
