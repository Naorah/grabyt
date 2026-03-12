# Fenetre historique des telechargements (lecture de download.json).

from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QMouseEvent
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.download_manager import get_history_entries, HistoryEntry
from src.i18n import t
from src.ui.icons import get_app_icon
from src.ui.styles import MAIN_STYLESHEET, HISTORY_SCROLLBAR_STYLE
from src.ui.title_bar import TitleBar


def _format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} o"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} Ko"
    return f"{size_bytes / (1024 * 1024):.1f} Mo"


def _format_date(iso_date: str) -> str:
    if not iso_date:
        return "--"
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return iso_date[:16] if len(iso_date) > 16 else iso_date


def _short_url(url: str, max_len: int = 70) -> str:
    s = url.strip()
    return s[:max_len] + "..." if len(s) > max_len else s


class HistoryCard(QFrame):
    """Carte cliquable vers le lien YouTube: clic ouvre l'URL."""

    def __init__(self, entry: HistoryEntry, parent: QWidget | None = None):
        super().__init__(parent)
        self.entry = entry
        self.setObjectName("historyCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        url_label = QLabel(_short_url(entry.url))
        url_label.setObjectName("historyCardUrl")
        url_label.setWordWrap(True)
        url_label.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(url_label)

        meta = QLabel(f"{entry.filename}  ·  {_format_date(entry.date)}  ·  {_format_size(entry.size_bytes)}")
        meta.setObjectName("historyCardMeta")
        layout.addWidget(meta)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.entry.url:
            QDesktopServices.openUrl(QUrl(self.entry.url))
        super().mousePressEvent(event)


class HistoryWindow(QWidget):
    """Fenetre affichant la liste scrollable des telechargements (download.json)."""

    def __init__(self, downloads_dir: str | Path, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("historyWindow")
        self.setWindowTitle(t("history_title"))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setMinimumSize(500, 400)
        self.resize(560, 480)
        _icon = get_app_icon()
        if not _icon.isNull():
            self.setWindowIcon(_icon)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._title_bar = TitleBar(self, title=t("history_title"))
        main_layout.addWidget(self._title_bar)

        scroll = QScrollArea()
        scroll.setObjectName("historyScrollArea")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        container = QWidget()
        self._list_layout = QVBoxLayout(container)
        self._list_layout.setContentsMargins(24, 16, 24, 16)
        self._list_layout.setSpacing(10)
        self._list_layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        self.setStyleSheet(MAIN_STYLESHEET + HISTORY_SCROLLBAR_STYLE)
        self._downloads_dir = Path(downloads_dir)
        self._container = container
        self._refresh()

    def _refresh(self) -> None:
        while self._list_layout.count() > 1:
            item = self._list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        entries = get_history_entries(self._downloads_dir)
        for e in entries:
            card = HistoryCard(e)
            self._list_layout.insertWidget(self._list_layout.count() - 1, card)
        if not entries:
            empty = QLabel(t("history_empty"))
            empty.setObjectName("secondaryLabel")
            self._list_layout.insertWidget(0, empty)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._refresh()
