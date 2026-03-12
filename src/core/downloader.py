# Telechargement YouTube vers MP3 via yt-dlp et ffmpeg.
# ffmpeg portable fourni par imageio-ffmpeg (aucune installation systeme requise).

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yt_dlp

try:
    import imageio_ffmpeg
    _FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except (ImportError, RuntimeError):
    _FFMPEG_EXE = None


@dataclass
class DownloadProgress:
    """Etat courant du telechargement pour l'interface."""

    current_url: str = ""
    current_title: str = ""
    current_percent: float = 0.0
    downloaded_count: int = 0
    error_count: int = 0
    remaining_count: int = 0
    total_count: int = 0
    eta_seconds: float | None = None
    is_running: bool = False


class Downloader:
    """
    Telecharge une liste d'URLs YouTube en MP3 dans un dossier donne.
    Utilise yt-dlp avec post-processeur ffmpeg pour l'extraction audio.
    """

    def __init__(
        self,
        output_dir: str | Path,
        progress_callback: Callable[[DownloadProgress], None] | None = None,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.progress_callback = progress_callback
        self._progress = DownloadProgress()
        self._cancelled = False

    def cancel(self) -> None:
        """Demande l'arret du telechargement en cours."""
        self._cancelled = True

    def download_all(self, urls: list[str]) -> tuple[int, int]:
        """
        Telecharge chaque URL en MP3. Retourne (nombre reussis, nombre en erreur).
        """
        self._cancelled = False
        total = len(urls)
        downloaded = 0
        errors = 0

        for i, url in enumerate(urls):
            if self._cancelled:
                break

            self._progress.current_url = url
            self._progress.current_title = ""
            self._progress.current_percent = 0.0
            self._progress.downloaded_count = downloaded
            self._progress.error_count = errors
            self._progress.remaining_count = total - i
            self._progress.total_count = total
            self._progress.is_running = True
            self._emit_progress()

            success = self._download_one(url, current_index=i + 1, total=total)
            if success:
                downloaded += 1
            else:
                errors += 1

        self._progress.is_running = False
        self._progress.remaining_count = 0
        self._emit_progress()
        return downloaded, errors

    def _download_one(self, url: str, current_index: int, total: int) -> bool:
        """Telecharge une URL en MP3. Retourne True si succes."""
        out_tmpl = str(self.output_dir / "%(title).200s.%(ext)s")

        def progress_hook(d: dict) -> None:
            if self._cancelled:
                raise yt_dlp.utils.DownloadCancelled()
            if d.get("status") == "downloading":
                percent = d.get("_percent_str", "0%").replace("%", "").strip()
                try:
                    self._progress.current_percent = float(percent)
                except ValueError:
                    self._progress.current_percent = 0.0
                self._progress.current_title = d.get("info_dict", {}).get("title", "")
                self._progress.eta_seconds = d.get("eta")
                self._emit_progress()
            elif d.get("status") == "finished":
                self._progress.current_percent = 100.0
                self._emit_progress()

        opts = {
            "format": "bestaudio/best",
            "outtmpl": out_tmpl,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "progress_hooks": [progress_hook],
            "quiet": True,
            "no_warnings": True,
        }
        if _FFMPEG_EXE:
            opts["ffmpeg_location"] = _FFMPEG_EXE

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return True
        except yt_dlp.utils.DownloadCancelled:
            return False
        except Exception:
            return False

    def _emit_progress(self) -> None:
        if self.progress_callback:
            self.progress_callback(self._progress)
