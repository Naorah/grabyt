# Validation des URLs YouTube (acces et format).

from dataclasses import dataclass
from typing import Callable

import yt_dlp


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
) -> ValidationResult:
    """
    Verifie chaque URL avec yt-dlp (extract_info sans telecharger).
    progress_callback(current_index, total, url) est appele pour chaque URL testee.
    """
    valid: list[str] = []
    invalid: list[str] = []
    total = len(urls)

    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }

    for i, url in enumerate(urls):
        if progress_callback:
            progress_callback(i + 1, total, url)
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.extract_info(url, download=False)
            valid.append(url)
        except Exception:
            invalid.append(url)

    return ValidationResult(valid=valid, invalid=invalid, total=total)
