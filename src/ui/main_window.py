# Fenetre principale: selection fichier, initialisation, telechargement et progression.

from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.config_loader import load_config
from src.core.downloader import Downloader, DownloadProgress
from src.core.url_parser import parse_urls_from_file
from src.core.url_validator import ValidationResult, validate_urls
from src.ui.progress_window import ProgressWindow
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
    """Thread pour lancer le telechargement."""

    finished = pyqtSignal(int, int)  # downloaded, errors
    progress = pyqtSignal(object)  # DownloadProgress

    def __init__(
        self,
        urls: list[str],
        output_dir: str,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self._urls = urls
        self._output_dir = output_dir
        self._downloader: Downloader | None = None

    def run(self) -> None:
        def on_progress(prog: DownloadProgress) -> None:
            self.progress.emit(prog)

        self._downloader = Downloader(self._output_dir, progress_callback=on_progress)
        downloaded, errors = self._downloader.download_all(self._urls)
        self.finished.emit(downloaded, errors)

    def cancel(self) -> None:
        if self._downloader:
            self._downloader.cancel()


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
        file_group = QGroupBox("Fichier de liens")
        file_layout = QHBoxLayout(file_group)
        self._file_edit = QLineEdit()
        self._file_edit.setPlaceholderText("Chemin vers le fichier URLs...")
        self._file_edit.setText(self._urls_file)
        self._browse_btn = QPushButton("Parcourir")
        self._browse_btn.clicked.connect(self._on_browse)
        file_layout.addWidget(self._file_edit)
        file_layout.addWidget(self._browse_btn)
        content_layout.addWidget(file_group)

        # Initialisation: bouton et resultats
        init_group = QGroupBox("Initialisation")
        init_layout = QVBoxLayout(init_group)
        self._init_btn = QPushButton("Initialiser (nombre de musiques, liens valides / non valides)")
        self._init_btn.clicked.connect(self._on_init)
        init_layout.addWidget(self._init_btn)

        self._stats_label = QLabel("Aucune initialisation effectuee.")
        self._stats_label.setObjectName("statsLabel")
        self._stats_label.setWordWrap(True)
        init_layout.addWidget(self._stats_label)
        content_layout.addWidget(init_group)

        # Bouton central de telechargement
        self._start_btn = QPushButton("Demarrer le telechargement")
        self._start_btn.setObjectName("startButton")
        self._start_btn.clicked.connect(self._on_start_download)
        self._start_btn.setEnabled(False)
        content_layout.addWidget(self._start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(content)
        self.setStyleSheet(MAIN_STYLESHEET)

    def _on_browse(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir le fichier de liens",
            str(Path(self._file_edit.text()).parent) if self._file_edit.text() else "",
            "Fichiers texte (*.txt);;Tous (*)",
        )
        if path:
            self._file_edit.setText(path)
            self._urls_file = path
            self._urls = []
            self._valid_urls = []
            self._stats_label.setText("Fichier modifie. Reinitialiser pour mettre a jour les statistiques.")
            self._start_btn.setEnabled(False)

    def _on_init(self) -> None:
        path = self._file_edit.text().strip()
        if not path:
            self._stats_label.setText("Veuillez selectionner un fichier.")
            return
        if not Path(path).exists():
            self._stats_label.setText("Le fichier specifie n'existe pas.")
            return

        self._urls = parse_urls_from_file(path)
        if not self._urls:
            self._stats_label.setText("Aucune URL YouTube trouvee dans le fichier.")
            self._start_btn.setEnabled(False)
            return

        self._stats_label.setText("Validation des liens en cours...")
        self._init_btn.setEnabled(False)
        self._validation_worker = ValidationWorker(self._urls, self)
        self._validation_worker.progress.connect(self._on_validation_progress)
        self._validation_worker.finished.connect(self._on_validation_finished)
        self._validation_worker.start()

    def _on_validation_progress(self, current: int, total: int, url: str) -> None:
        self._stats_label.setText(f"Validation: {current} / {total} liens...")

    def _on_validation_finished(self, result: ValidationResult) -> None:
        self._validation_worker = None
        self._init_btn.setEnabled(True)
        self._valid_urls = result.valid
        self._stats_label.setText(
            f"Total: {result.total} | Valides: {result.valid_count} | Invalides: {result.invalid_count}"
        )
        self._start_btn.setEnabled(result.valid_count > 0)

    def _on_start_download(self) -> None:
        if not self._valid_urls:
            return
        out_dir = self._config["downloads_dir"]
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        self._start_btn.setEnabled(False)
        self._start_btn.setText("Telechargement en cours...")

        progress_title = f"{self._config['app_name']} - Progression"
        self._progress_window = ProgressWindow(
            self, title=progress_title, downloads_dir=out_dir
        )
        self._progress_window.reset()
        self._progress_window.show()

        self._download_worker = DownloadWorker(
            self._valid_urls,
            out_dir,
            self,
        )
        self._download_worker.progress.connect(self._progress_window.update_progress)
        self._download_worker.finished.connect(self._on_download_finished)
        self._download_worker.start()

    def _on_download_finished(self, downloaded: int, errors: int) -> None:
        self._download_worker = None
        self._start_btn.setEnabled(True)
        self._start_btn.setText("Demarrer le telechargement")
        if self._progress_window:
            self._progress_window.set_finished(downloaded, errors)
            self._progress_window = None
