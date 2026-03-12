# Version courante et verification simple de mise a jour.

import json
import urllib.request
from typing import Any

CURRENT_VERSION = "0.3.0"


def _parse_version(s: str) -> tuple[int, ...]:
    """Transforme '1.2.3' en (1, 2, 3) pour comparaison."""
    parts = []
    for x in s.strip().split("."):
        try:
            parts.append(int(x))
        except ValueError:
            parts.append(0)
    return tuple(parts) if parts else (0,)


def is_newer(latest: str, current: str = CURRENT_VERSION) -> bool:
    """Retourne True si latest > current (semver simple)."""
    return _parse_version(latest) > _parse_version(current)


def fetch_latest_version(url: str, timeout_sec: float = 5.0) -> str | None:
    """
    Recupere la version depuis une URL renvoyant un JSON avec une cle 'version'.
    Retourne la chaine de version ou None en cas d'erreur.
    """
    if not url or not url.strip():
        return None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GrabYT/" + CURRENT_VERSION})
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            data: Any = json.loads(resp.read().decode())
            if isinstance(data, dict) and "version" in data:
                return str(data["version"]).strip()
            return None
    except Exception:
        return None
