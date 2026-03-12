# Logs structures: niveau et fichier configurables (config.yaml).

import logging
import sys
from pathlib import Path
from typing import Any


def setup_logging(
    level: str = "INFO",
    log_file: str | None = None,
) -> None:
    """
    Configure le module logging (niveau, format, fichier optionnel).
    A appeler au demarrage avec les valeurs de config.
    """
    numeric = getattr(logging, level.upper(), logging.INFO)
    if not isinstance(numeric, int):
        numeric = logging.INFO

    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=datefmt)

    root = logging.getLogger()
    root.setLevel(numeric)
    for h in root.handlers[:]:
        root.removeHandler(h)

    handler_console = logging.StreamHandler(sys.stdout)
    handler_console.setFormatter(formatter)
    root.addHandler(handler_console)

    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            handler_file = logging.FileHandler(path, encoding="utf-8")
            handler_file.setFormatter(formatter)
            root.addHandler(handler_file)
        except OSError:
            root.warning("Impossible d'ouvrir le fichier de log: %s", log_file)


def get_logger(name: str) -> logging.Logger:
    """Retourne un logger nomme (ex: src.core.download_manager)."""
    return logging.getLogger(name)


def log_struct(logger: logging.Logger, level: int, msg: str, **kwargs: Any) -> None:
    """Ecrit un message avec champs additionnels (structure)."""
    extra = " | ".join(f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None)
    if extra:
        msg = f"{msg} | {extra}"
    logger.log(level, msg)
