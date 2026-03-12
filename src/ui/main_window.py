# Fenetre principale: selection fichier, initialisation, telechargement et progression.

import os
from pathlib import Path

from PyQt6.QtCore import QPoint, QThread, pyqtSignal, Qt, QUrl, QEvent
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from notifypy import Notify

from src.config_loader import load_config
from src.i18n import t
from src.core.download_manager import get_download_manager
from src.core.downloader import DownloadProgress
from src.core.url_parser import parse_urls_from_file
from src.core.url_validator import ValidationResult, validate_urls
from src.ui.history_window import HistoryWindow
from src.ui.icons import get_history_icon, get_open_file_icon
from src.ui.progress_window import ProgressWindow
from src.ui.rounded_tooltip import RoundedTooltip
from src.ui.styles import MAIN_STYLESHEET
from src.ui.title_bar import TitleBar


class ValidationWorker(QThread):
    """Thread pour valider les URLs sans bloquer l'interface."""

    finished = pyqtSignal(object)  # ValidationResult
    progress = pyqtSignal(int, int, str)

    def __init__(self, urls: list[str], parent: QWidget | None = None):
        super().__init__(parent)
        self._urls = urls

    def run(self) -> None:
        def on_progress(current: int, total: int, url: str) -> None:
            self.progress.emit(current, total, url)

        result = validate_urls(self._urls, progress_callback=on_progress)
        self.finished.emit(result)


class DownloadWorker(QThread):
    """Thread qui delegue au DownloadManager central (file + N workers, retries)."""

    finished = pyqtSignal(int, int)  # downloaded, errors
    progress = pyqtSignal(object)  # DownloadProgress

    def __init__(
        self,
        urls: list[str],
        output_dir: str,
        max_workers: int,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self._urls = urls
        self._output_dir = output_dir
        self._max_workers = max_workers

    def run(self) -> None:
        manager = get_download_manager(self._max_workers)
        manager.set_progress_callback(lambda p: self.progress.emit(p))
        downloaded, errors = manager.run_batch(self._urls, self._output_dir)
        self.finished.emit(downloaded, errors)

    def cancel(self) -> None:
        get_download_manager().cancel()


class MainWindow(QMainWindow):
    """Fenetre principale avec barre de titre custom et contenu central."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window
        )
        self.setMinimumSize(520, 420)
        self.resize(560, 480)

        self._config = load_config()
        self._urls_file: str = self._config["default_urls_file"]
        self._urls: list[str] = []
        self._valid_urls: list[str] = []
        self._validation_worker: ValidationWorker | None = None
        self._download_worker: DownloadWorker | None = None
        self._progress_window: ProgressWindow | None = None

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._title_bar = TitleBar(self, title=self._config["app_name"])
        main_layout.addWidget(self._title_bar)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(24, 24, 24, 24)

        # Selection du fichier
        file_group = QGroupBox(t("file_group_title"))
        file_layout = QVBoxLayout(file_group)
        row_file = QHBoxLayout()
        self._file_edit = QLineEdit()
        self._file_edit.setPlaceholderText(t("file_placeholder"))
        self._file_edit.setText(self._urls_file)
        self._browse_btn = QPushButton(t("browse"))
        self._browse_btn.clicked.connect(self._on_browse)
        self._open_file_btn = QPushButton()
        self._open_file_btn.setObjectName("openFileButton")
        self._open_file_btn.setFixedSize(40, 40)
        self._open_file_btn.setIcon(get_open_file_icon(20))
        self._open_file_btn.clicked.connect(self._on_open_file)
        row_file.addWidget(self._file_edit)
        row_file.addWidget(self._browse_btn)
        row_file.addWidget(self._open_file_btn)
        file_layout.addLayout(row_file)
        content_layout.addWidget(file_group)

        # Initialisation: bouton unique (init puis demarrage) + historique a droite
        init_group = QGroupBox(t("init_group_title"))
        init_layout = QVBoxLayout(init_group)
        self._stats_label = QLabel(t("stats_none"))
        self._stats_label.setObjectName("statsLabel")
        self._stats_label.setWordWrap(True)
        init_layout.addWidget(self._stats_label)

        self._validation_progress = QProgressBar()
        self._validation_progress.setFixedHeight(8)
        self._validation_progress.setRange(0, 100)
        self._validation_progress.setValue(0)
        self._validation_progress.setTextVisible(False)
        self._validation_progress.hide()
        init_layout.addWidget(self._validation_progress)

        action_row = QHBoxLayout()
        self._action_btn = QPushButton(t("init_button"))
        self._action_btn.clicked.connect(self._on_action_clicked)
        action_row.addWidget(self._action_btn)

        self._history_btn = QPushButton()
        self._history_btn.setObjectName("openFileButton")
        self._history_btn.setFixedSize(40, 40)
        self._history_btn.setIcon(get_history_icon(20))
        self._history_btn.clicked.connect(self._on_open_history)
        action_row.addWidget(self._history_btn)
        init_layout.addLayout(action_row)
        content_layout.addWidget(init_group)

        main_layout.addWidget(content)
        self.setStyleSheet(MAIN_STYLESHEET)

        # Tooltips arrondis (fenêtre à masque) pour les boutons circulaires
        self._open_file_tooltip = RoundedTooltip(t("tooltip_open_file"))
        self._history_tooltip = RoundedTooltip(t("tooltip_history"))
        self._tooltip_map: dict[QWidget, RoundedTooltip] = {
            self._open_file_btn: self._open_file_tooltip,
            self._history_btn: self._history_tooltip,
        }
        self._open_file_btn.installEventFilter(self)
        self._history_btn.installEventFilter(self)

    def eventFilter(self, obj: QWidget, event: QEvent) -> bool:
        tip = self._tooltip_map.get(obj)
        if tip is None:
            return super().eventFilter(obj, event)
        if event.type() == QEvent.Type.Enter:
            # Position en coordonnées écran : juste sous le bouton, aligné à droite
            bottom_right = obj.mapToGlobal(obj.rect().bottomRight())
            x = bottom_right.x() - tip.width()
            y = bottom_right.y() + 6
            tip.move(x, y)
            tip.show()
        elif event.type() == QEvent.Type.Leave:
            tip.hide()
        return super().eventFilter(obj, event)

    def _on_open_history(self) -> None:
        out_dir = self._config.get("downloads_dir", "downloads")
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        win = HistoryWindow(out_dir, self)
        win.show()

    def _on_open_file(self) -> None:
        path = self._file_edit.text().strip()
        if not path:
            return
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        if not os.path.isfile(path):
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def _on_browse(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            t("browse_dialog_title"),
            str(Path(self._file_edit.text()).parent) if self._file_edit.text() else "",
            "Fichiers texte (*.txt);;Tous (*)",
        )
        if path:
            self._file_edit.setText(path)
            self._urls_file = path
            self._urls = []
            self._valid_urls = []
            self._stats_label.setText(t("stats_file_changed"))
            self._switch_action_to_init()

    def _switch_action_to_init(self) -> None:
        """Remet le bouton en mode Initialiser."""
        self._validation_progress.hide()
        self._action_btn.setText(t("init_button"))
        self._action_btn.setObjectName("")
        self._action_btn.style().unpolish(self._action_btn)
        self._action_btn.style().polish(self._action_btn)
        self._action_btn.setEnabled(True)

    def _switch_action_to_start(self) -> None:
        """Passe le bouton en mode Demarrer le telechargement."""
        self._action_btn.setText(t("start_button"))
        self._action_btn.setObjectName("startButton")
        self._action_btn.setEnabled(True)
        self._action_btn.style().unpolish(self._action_btn)
        self._action_btn.style().polish(self._action_btn)

    def _on_action_clicked(self) -> None:
        """Un seul bouton: init si pas encore valide, demarrage sinon."""
        if self._valid_urls:
            self._on_start_download()
        else:
            self._on_init()

    def _on_init(self) -> None:
        path = self._file_edit.text().strip()
        if not path:
            self._stats_label.setText(t("stats_select_file"))
            return
        if not Path(path).exists():
            self._stats_label.setText(t("stats_file_missing"))
            return

        self._urls = parse_urls_from_file(path)
        if not self._urls:
            self._stats_label.setText(t("stats_no_urls"))
            self._action_btn.setEnabled(True)
            return

        self._stats_label.setText(t("stats_validation"))
        self._action_btn.setEnabled(False)
        self._validation_progress.setRange(0, len(self._urls))
        self._validation_progress.setValue(0)
        self._validation_progress.show()
        self._validation_worker = ValidationWorker(self._urls, self)
        self._validation_worker.progress.connect(self._on_validation_progress)
        self._validation_worker.finished.connect(self._on_validation_finished)
        self._validation_worker.start()

    def _on_validation_progress(self, current: int, total: int, url: str) -> None:
        self._stats_label.setText(t("validation_progress", current=current, total=total))
        self._validation_progress.setValue(current)

    def _on_validation_finished(self, result: ValidationResult) -> None:
        self._validation_worker = None
        self._validation_progress.hide()
        self._valid_urls = result.valid
        self._stats_label.setText(
            t("stats_format", total=result.total, valid=result.valid_count, invalid=result.invalid_count)
        )
        if result.valid_count > 0:
            self._switch_action_to_start()
        else:
            self._action_btn.setEnabled(True)

    def _on_start_download(self) -> None:
        if not self._valid_urls:
            return
        out_dir = self._config["downloads_dir"]
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        self._action_btn.setEnabled(False)
        self._action_btn.setText(t("downloading"))

        self._progress_window = ProgressWindow(
            self, title=t("progress_window_title"), downloads_dir=out_dir
        )
        self._progress_window.reset()
        self._progress_window.show()

        self._download_worker = DownloadWorker(
            self._valid_urls,
            out_dir,
            self._config.get("max_concurrent_downloads", 3),
            self,
        )
        self._download_worker.progress.connect(self._progress_window.update_progress)
        self._download_worker.finished.connect(self._on_download_finished)
        self._download_worker.start()

    def _on_download_finished(self, downloaded: int, errors: int) -> None:
        self._download_worker = None
        self._action_btn.setEnabled(True)
        self._action_btn.setText(t("start_button"))
        total = len(self._valid_urls) if self._valid_urls else 0
        if self._progress_window:
            self._progress_window.set_finished(downloaded, errors, total=total)
            self._progress_window = None
        # Notification fin de batch via notification système
        if total > 0:
            pct = 100.0 * downloaded / total
            msg = t("termine_pct", pct=pct, ok=downloaded, total=total)
        else:
            msg = t("termine")
        notification = Notify()
        notification.title = self.windowTitle()
        notification.message = msg
        try:
            notification.send()
        except Exception:
            # On ignore les erreurs de notification pour ne pas interrompre le flux
            pass
