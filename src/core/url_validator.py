# Validation des URLs YouTube (acces et format) en batch parallele.

from dataclasses import dataclass
from typing import Callable

import yt_dlp
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.logger import get_logger

DEFAULT_VALIDATION_WORKERS = 6
_log = get_logger(__name__)


def _validate_one(url: str, opts: dict) -> tuple[str, bool]:
    """Valide une URL. Retourne (url, True si valide)."""
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.extract_info(url, download=False)
        return url, True
    except Exception:
        return url, False


@dataclass
class ValidationResult:
    """Resultat du scan: URLs valides et invalides."""

    valid: list[str]
    invalid: list[str]
    total: int

    @property
    def valid_count(self) -> int:
        return len(self.valid)

    @property
    def invalid_count(self) -> int:
        return len(self.invalid)


def validate_urls(
    urls: list[str],
    progress_callback: Callable[[int, int, str], None] | None = None,
    max_workers: int = DEFAULT_VALIDATION_WORKERS,
) -> ValidationResult:
    """
    Verifie les URLs en parallele (batch) avec yt-dlp (extract_info sans telecharger).
    progress_callback(current_done, total, url) est appele a chaque URL terminee.
    """
    valid: list[str] = []
    invalid: list[str] = []
    total = len(urls)
    done = 0

    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }

    max_workers = min(max_workers, max(1, total))
    _log.info("validation_start total=%s", total)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_validate_one, url, opts): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                _, ok = future.result()
                if ok:
                    valid.append(url)
                else:
                    invalid.append(url)
            except Exception:
                invalid.append(url)
            done += 1
            if progress_callback:
                progress_callback(done, total, url)

    _log.info("validation_finished valid=%s invalid=%s total=%s", len(valid), len(invalid), total)
    return ValidationResult(valid=valid, invalid=invalid, total=total)
