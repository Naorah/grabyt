# Point d'entree de l'application.
# Lance l'interface Qt avec le nom et les options charges depuis config/config.yaml.

import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from src.config_loader import load_config
from src.ui.main_window import MainWindow


def main() -> None:
    config = load_config()
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 9)
    app.setFont(font)

    window = MainWindow()
    window.setWindowTitle(config["app_name"])
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
