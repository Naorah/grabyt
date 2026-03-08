# Barre de titre personnalisee (sans bordure systeme): cercles type macOS (vert / orange / rouge).

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from src.ui.icons import get_app_icon_pixmap
from src.ui.styles import TITLE_BAR_BUTTON_STYLE


class TitleBar(QFrame):
    """
    Barre de titre custom pour une fenetre sans bordure native.
    Icone application a gauche du titre, puis trois cercles: vert / orange / rouge.
    Gere le double-clic pour restaurer/maximiser et le glisser pour deplacer.
    """

    def __init__(self, parent: QWidget | None = None, title: str = ""):
        super().__init__(parent)
        self.setObjectName("titleBar")
        self._window = parent
        self._drag_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(10)

        self._icon_label = QLabel()
        self._icon_label.setFixedSize(18, 18)
        self._icon_label.setPixmap(get_app_icon_pixmap(18))
        layout.addWidget(self._icon_label)

        self._title_label = QLabel(title)
        self._title_label.setObjectName("titleLabel")
        layout.addWidget(self._title_label)
        layout.addStretch()

        self._min_btn = QPushButton()
        self._min_btn.setObjectName("minButton")
        self._min_btn.setStyleSheet(TITLE_BAR_BUTTON_STYLE)
        self._min_btn.clicked.connect(self._on_minimize)
        self._min_btn.setFixedSize(12, 12)
        layout.addWidget(self._min_btn)

        self._restore_btn = QPushButton()
        self._restore_btn.setObjectName("restoreButton")
        self._restore_btn.setStyleSheet(TITLE_BAR_BUTTON_STYLE)
        self._restore_btn.clicked.connect(self._on_restore)
        self._restore_btn.setFixedSize(12, 12)
        layout.addWidget(self._restore_btn)

        self._close_btn = QPushButton()
        self._close_btn.setObjectName("closeButton")
        self._close_btn.setStyleSheet(TITLE_BAR_BUTTON_STYLE)
        self._close_btn.clicked.connect(self._on_close)
        self._close_btn.setFixedSize(12, 12)
        layout.addWidget(self._close_btn)

        self.setFixedHeight(34)

    def set_title(self, title: str) -> None:
        self._title_label.setText(title)

    def _on_minimize(self) -> None:
        if self._window:
            self._window.showMinimized()

    def _on_restore(self) -> None:
        if self._window:
            if self._window.isMaximized():
                self._window.showNormal()
            else:
                self._window.showMaximized()

    def _on_close(self) -> None:
        if self._window:
            self._window.close()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self._window:
            self._drag_pos = event.globalPosition().toPoint() - self._window.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos is not None and self._window:
            self._window.move(event.globalPosition().toPoint() - self._drag_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._on_restore()
        super().mouseDoubleClickEvent(event)
