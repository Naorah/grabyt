# Lecture et extraction des URLs depuis un fichier texte.

import re
from pathlib import Path


# Pattern pour les URLs YouTube (watch, shorts, embed, etc.)
YOUTUBE_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)[\w\-]+"
)


def parse_urls_from_file(filepath: str | Path) -> list[str]:
    """
    Lit un fichier et en extrait toutes les URLs YouTube (une par ligne ou inline).
    Retourne une liste d'URLs normalisees, sans doublons, dans l'ordre d'apparition.
    """
    path = Path(filepath)
    if not path.exists():
        return []

    urls: list[str] = []
    seen: set[str] = set()

    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for match in YOUTUBE_URL_PATTERN.finditer(line):
                url = _normalize_url(match.group(0))
                if url and url not in seen:
                    seen.add(url)
                    urls.append(url)

    return urls


def _normalize_url(url: str) -> str:
    """Normalise une URL YouTube (supprime parametres inutiles pour unicite)."""
    url = url.strip()
    if "youtu.be/" in url:
        return url
    if "watch?v=" in url:
        base = url.split("watch?v=")[0] + "watch?v="
        rest = url.split("watch?v=")[1]
        vid_id = rest.split("&")[0].split("#")[0]
        return base + vid_id
    if "shorts/" in url:
        base = url.split("shorts/")[0] + "shorts/"
        rest = url.split("shorts/")[1]
        vid_id = rest.split("?")[0].split("#")[0]
        return base + vid_id
    if "embed/" in url:
        base = url.split("embed/")[0] + "embed/"
        rest = url.split("embed/")[1]
        vid_id = rest.split("?")[0].split("#")[0]
        return base + vid_id
    return url
