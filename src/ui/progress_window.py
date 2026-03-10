# Fenetre secondaire affichant la progression du telechargement.
# Meme style que la fenetre principale (barre de titre custom, theme pastel et blanc).

from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.downloader import DownloadProgress
from src.ui.styles import MAIN_STYLESHEET
from src.ui.icons import get_app_icon
from src.ui.title_bar import TitleBar


class ProgressWindow(QWidget):
    """
    Fenetre dediee a l'affichage de la progression (piste en cours, %, compteurs, ETA).
    Meme apparence que la fenetre principale (barre de titre avec cercles pastels).
    A la fin: bouton "Vers les musiques" pour ouvrir le dossier.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        title: str = "Progression",
        downloads_dir: str = "",
    ) -> None:
        super().__init__(parent)
        self.setObjectName("progressWindow")
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setMinimumSize(420, 280)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        self._downloads_dir = downloads_dir
        _icon = get_app_icon()
        if not _icon.isNull():
            self.setWindowIcon(_icon)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._title_bar = TitleBar(self, title=title)
        main_layout.addWidget(self._title_bar)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(24, 24, 24, 24)

        process_group = QGroupBox("Process")
        process_group.setObjectName("processGroup")
        layout = QVBoxLayout(process_group)
        layout.setSpacing(16)

        layout.addWidget(QLabel("En cours"))
        self._current_track_label = QLabel("--")
        self._current_track_label.setObjectName("trackLabel")
        self._current_track_label.setWordWrap(True)
        self._current_track_label.setMaximumHeight(36)
        layout.addWidget(self._current_track_label)

        row_avancement = QHBoxLayout()
        row_avancement.setSpacing(8)
        row_avancement.addWidget(QLabel("Avancement"))
        self._current_percent_label = QLabel("0 %")
        self._current_percent_label.setMinimumWidth(40)
        row_avancement.addWidget(self._current_percent_label)
        row_avancement.addStretch()
        layout.addLayout(row_avancement)

        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        layout.addWidget(self._progress_bar)

        row_counts = QHBoxLayout()
        row_counts.setSpacing(20)
        self._dot_dl = QWidget()
        self._dot_dl.setObjectName("progressDotGreen")
        self._dot_dl.setFixedSize(12, 12)
        self._count_dl_label = QLabel("0")
        self._count_dl_label.setObjectName("secondaryLabel")
        self._dot_err = QWidget()
        self._dot_err.setObjectName("progressDotRed")
        self._dot_err.setFixedSize(12, 12)
        self._count_err_label = QLabel("0")
        self._count_err_label.setObjectName("secondaryLabel")
        self._dot_rest = QWidget()
        self._dot_rest.setObjectName("progressDotBlue")
        self._dot_rest.setFixedSize(12, 12)
        self._count_rest_label = QLabel("0")
        self._count_rest_label.setObjectName("secondaryLabel")
        for dot, lbl in (
            (self._dot_dl, self._count_dl_label),
            (self._dot_err, self._count_err_label),
            (self._dot_rest, self._count_rest_label),
        ):
            pair = QHBoxLayout()
            pair.setSpacing(4)
            pair.setContentsMargins(0, 0, 0, 0)
            pair.addWidget(dot)
            pair.addWidget(lbl)
            row_counts.addLayout(pair)
        row_counts.addStretch()
        layout.addLayout(row_counts)

        self._eta_label = QLabel("ETA: --")
        self._eta_label.setObjectName("secondaryLabel")
        layout.addWidget(self._eta_label)

        self._buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(self._buttons_widget)
        buttons_layout.setContentsMargins(0, 16, 0, 0)
        buttons_layout.setSpacing(12)
        buttons_layout.addStretch()
        self._open_folder_btn = QPushButton("Vers les musiques")
        self._open_folder_btn.setObjectName("startButton")
        self._open_folder_btn.setEnabled(False)
        self._open_folder_btn.clicked.connect(self._on_open_folder)
        buttons_layout.addWidget(self._open_folder_btn)
        layout.addWidget(self._buttons_widget)

        content_layout.addWidget(process_group)
        main_layout.addWidget(content)
        self.setStyleSheet(MAIN_STYLESHEET)

    def _on_open_folder(self) -> None:
        if self._downloads_dir:
            path = Path(self._downloads_dir).resolve()
            if path.exists():
                url = QUrl.fromLocalFile(str(path))
                QDesktopServices.openUrl(url)

    def update_progress(self, prog: DownloadProgress) -> None:
        """Met a jour l'affichage avec l'etat courant du telechargement."""
        title = prog.current_title or prog.current_url
        if len(title) > 60:
            title = title[:57] + "..."
        self._current_track_label.setText(title)
        self._current_percent_label.setText(f"{prog.current_percent:.0f} %")
        self._progress_bar.setValue(int(prog.current_percent))
        self._count_dl_label.setText(str(prog.downloaded_count))
        self._count_err_label.setText(str(prog.error_count))
        self._count_rest_label.setText(str(prog.remaining_count))
        if prog.eta_seconds is not None and prog.eta_seconds >= 0:
            eta_m = int(prog.eta_seconds // 60)
            eta_s = int(prog.eta_seconds % 60)
            self._eta_label.setText(f"ETA: {eta_m:02d}:{eta_s:02d}")
        else:
            self._eta_label.setText("ETA: --")

    def set_finished(self, downloaded: int, errors: int) -> None:
        """Affiche l'etat final et active le bouton Vers les musiques."""
        self._progress_bar.setValue(100)
        self._eta_label.setText("Termine.")
        self._count_dl_label.setText(str(downloaded))
        self._count_err_label.setText(str(errors))
        self._count_rest_label.setText("0")
        self._open_folder_btn.setEnabled(True)

    def reset(self) -> None:
        """Reinitialise les champs avant un nouveau telechargement."""
        self._current_track_label.setText("--")
        self._current_percent_label.setText("0 %")
        self._progress_bar.setValue(0)
        self._count_dl_label.setText("0")
        self._count_err_label.setText("0")
        self._count_rest_label.setText("0")
        self._eta_label.setText("ETA: --")
        self._open_folder_btn.setEnabled(False)
