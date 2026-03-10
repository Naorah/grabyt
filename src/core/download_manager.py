# Gestionnaire centralise des telechargements: file d'attente, N workers, retries, historique download.json.

from __future__ import annotations

import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import yt_dlp

from src.core.downloader import DownloadProgress

try:
    import imageio_ffmpeg
    _FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except (ImportError, RuntimeError):
    _FFMPEG_EXE = None

DOWNLOAD_JSON_FILENAME = "download.json"
MAX_RETRIES = 3


@dataclass
class HistoryEntry:
    """Une entree de l'historique (download.json)."""
    url: str
    filename: str
    date: str  # ISO
    size_bytes: int


def _load_history(path: Path) -> list[dict]:
    """Charge le fichier historique ou retourne une liste vide."""
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    if isinstance(data, list):
        return data
    return data.get("history", data.get("entries", []))


def get_history_entries(downloads_dir: str | Path) -> list[HistoryEntry]:
    """Retourne la liste des entrees d'historique (plus recent en premier)."""
    path = Path(downloads_dir) / DOWNLOAD_JSON_FILENAME
    raw = _load_history(path)
    entries = []
    for r in raw:
        if isinstance(r, dict) and r.get("url"):
            entries.append(HistoryEntry(
                url=r["url"],
                filename=r.get("filename", ""),
                date=r.get("date", ""),
                size_bytes=int(r.get("size_bytes", 0)),
            ))
    entries.reverse()
    return entries


def _append_history_entry(path: Path, entry: HistoryEntry, lock: threading.Lock) -> None:
    """Ajoute une entree a download.json (thread-safe)."""
    with lock:
        entries = _load_history(path)
        entries.append({
            "url": entry.url,
            "filename": entry.filename,
            "date": entry.date,
            "size_bytes": entry.size_bytes,
        })
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"history": entries}, f, ensure_ascii=False, indent=2)


def _download_one(
    url: str,
    output_dir: Path,
    ffmpeg_exe: str | None,
    progress_callback: Callable[[float, str, float | None], None],
    cancel_check: Callable[[], bool],
    last_file_ref: list[Path],
) -> tuple[bool, str | None, int]:
    """
    Telecharge une URL en MP3. Retourne (success, filename_or_none, size_bytes).
    Met a jour last_file_ref[0] avec le chemin du fichier en cas de succes (pour recuperer la taille).
    """
    out_tmpl = str(output_dir / "%(title).200s.%(ext)s")

    def progress_hook(d: dict) -> None:
        if cancel_check():
            raise yt_dlp.utils.DownloadCancelled()
        if d.get("status") == "downloading":
            percent = d.get("_percent_str", "0%").replace("%", "").strip()
            try:
                pct = float(percent)
            except ValueError:
                pct = 0.0
            progress_callback(pct, d.get("info_dict", {}).get("title", ""), d.get("eta"))
        elif d.get("status") == "finished":
            progress_callback(100.0, d.get("info_dict", {}).get("title", ""), None)
            if not last_file_ref:
                f = d.get("filename")
                if f:
                    last_file_ref.append(Path(f).with_suffix(".mp3"))

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
    }
    if ffmpeg_exe:
        opts["ffmpeg_location"] = ffmpeg_exe

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadCancelled:
        return False, None, 0
    except Exception:
        return False, None, 0

    final_path = last_file_ref[-1] if last_file_ref else None
    if final_path and final_path.exists():
        return True, final_path.name, final_path.stat().st_size
    # Fallback: dernier .mp3 du dossier par mtime
    mp3s = sorted(output_dir.glob("*.mp3"), key=lambda p: p.stat().st_mtime, reverse=True)
    if mp3s:
        p = mp3s[0]
        return True, p.name, p.stat().st_size
    return False, None, 0


class DownloadManager:
    """
    Gestionnaire unique des telechargements: file d'attente, N workers simultanes,
    retries automatiques (3x), ecriture de download.json pour l'historique.
    Thread-safe; les signaux peuvent etre emis depuis les workers (Qt les queue vers le main thread).
    """

    def __init__(self, max_workers: int = 3):
        self._max_workers = max(1, min(max_workers, 8))
        self._progress_callback: Callable[[DownloadProgress], None] | None = None
        self._lock = threading.Lock()
        self._downloaded_count = 0
        self._error_count = 0
        self._total_count = 0
        self._current_percent = 0.0
        self._current_title = ""
        self._eta_seconds: float | None = None
        self._cancelled = False
        self._history_path: Path | None = None
        self._history_lock = threading.Lock()

    def set_progress_callback(self, callback: Callable[[DownloadProgress], None] | None) -> None:
        self._progress_callback = callback

    def _emit_progress(self) -> None:
        if not self._progress_callback:
            return
        with self._lock:
            remaining = max(0, self._total_count - self._downloaded_count - self._error_count)
        self._progress_callback(DownloadProgress(
            current_url="",
            current_title=self._current_title,
            current_percent=self._current_percent,
            downloaded_count=self._downloaded_count,
            error_count=self._error_count,
            remaining_count=remaining,
            total_count=self._total_count,
            eta_seconds=self._eta_seconds,
            is_running=remaining > 0 or self._downloaded_count + self._error_count < self._total_count,
        ))

    def run_batch(self, urls: list[str], output_dir: str | Path) -> tuple[int, int]:
        """
        Lance le telechargement de toutes les URLs (file + N workers, 3 retries).
        Bloque jusqu'a la fin. Retourne (downloaded, errors).
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        self._history_path = output_dir / DOWNLOAD_JSON_FILENAME

        self._cancelled = False
        with self._lock:
            self._downloaded_count = 0
            self._error_count = 0
            self._total_count = len(urls)
        self._current_percent = 0.0
        self._current_title = ""
        self._eta_seconds = None
        self._emit_progress()

        def cancel_check() -> bool:
            return self._cancelled

        def one_progress(percent: float, title: str, eta) -> None:
            with self._lock:
                self._current_percent = percent
                self._current_title = title
                self._eta_seconds = float(eta) if eta is not None else None
            self._emit_progress()

        def do_one(url: str) -> tuple[bool, str | None, int]:
            last_file: list[Path] = []
            for attempt in range(MAX_RETRIES):
                ok, filename, size = _download_one(
                    url, output_dir, _FFMPEG_EXE, one_progress, cancel_check, last_file
                )
                if ok:
                    return True, filename, size
                if self._cancelled:
                    return False, None, 0
            return False, None, 0

        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = {executor.submit(do_one, url): url for url in urls}
            for future in as_completed(futures):
                if self._cancelled:
                    for f in futures:
                        f.cancel()
                    break
                url = futures[future]
                try:
                    ok, filename, size_bytes = future.result()
                except Exception:
                    ok, filename, size_bytes = False, None, 0
                with self._lock:
                    if ok:
                        self._downloaded_count += 1
                        if filename and self._history_path:
                            entry = HistoryEntry(
                                url=url,
                                filename=filename,
                                date=datetime.now(timezone.utc).isoformat(),
                                size_bytes=size_bytes or 0,
                            )
                            _append_history_entry(self._history_path, entry, self._history_lock)
                    else:
                        self._error_count += 1
                self._emit_progress()

        self._current_percent = 0.0
        self._current_title = ""
        self._eta_seconds = None
        self._emit_progress()
        with self._lock:
            return self._downloaded_count, self._error_count

    def cancel(self) -> None:
        self._cancelled = True


# Instance unique du gestionnaire (injectee ou recuperee via get_download_manager).
_manager: DownloadManager | None = None


def get_download_manager(max_workers: int = 3) -> DownloadManager:
    """Retourne le gestionnaire de telechargement unique (singleton)."""
    global _manager
    if _manager is None:
        _manager = DownloadManager(max_workers=max_workers)
    return _manager
