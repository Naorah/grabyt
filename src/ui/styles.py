# Theme global: pastel et blanc, moderne et cozy.
# Palette unifiee pour fenetre principale, fenetre progression et tous les composants.

MAIN_STYLESHEET = """
QWidget {
    background-color: #faf8f6;
    color: #2c2c2c;
    font-family: "Segoe UI", sans-serif;
}

QMainWindow {
    background-color: #faf8f6;
    border: 1px solid #e8e4e0;
}

QPushButton {
    background-color: #ffffff;
    color: #2c2c2c;
    border: 1px solid #e0ddd8;
    border-radius: 8px;
    padding: 10px 20px;
    min-height: 24px;
}

QPushButton:hover {
    background-color: #f0eeeb;
    border-color: #d8d5d0;
}

QPushButton:pressed {
    background-color: #e8e6e2;
}

QPushButton:disabled {
    background-color: #f0eeeb;
    color: #a8a6a2;
    border-color: #e8e4e0;
}

QPushButton#startButton {
    background-color: #8bc4b0;
    color: #ffffff;
    border: none;
    font-weight: bold;
    min-width: 180px;
}

QPushButton#startButton:hover {
    background-color: #7ab39f;
}

QPushButton#startButton:pressed {
    background-color: #6aa28e;
}

QPushButton#startButton:disabled {
    background-color: #c5e0d6;
    color: #ffffff;
}

QPushButton#openFileButton {
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
    border-radius: 20px;
    padding: 0;
}

QToolTip {
    background-color: #ffffff;
    color: #2c2c2c;
    border: 1px solid #e0ddd8;
    border-radius: 8px;
    padding: 8px 12px;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}

QLineEdit {
    background-color: #ffffff;
    color: #2c2c2c;
    border: 1px solid #e0ddd8;
    border-radius: 8px;
    padding: 10px 14px;
    selection-background-color: #c5e0d6;
}

QLineEdit:focus {
    border-color: #8bc4b0;
}

QLabel {
    color: #2c2c2c;
}

QLabel#titleLabel {
    color: #2c2c2c;
    font-size: 13px;
    background-color: #ffffff;
    padding: 0 6px 0 6px;
    border-bottom: 1px solid #e8e4e0;
}

QLabel#trackLabel {
    color: #6b6b6b;
    font-size: 12px;
}

QLabel#secondaryLabel {
    color: #7d7d7d;
}

QLabel#statsLabel {
    background-color: #ffffff;
    color: #2c2c2c;
    padding: 4px 0;
}

QProgressBar {
    background-color: #f0eeeb;
    border: 1px solid #e0ddd8;
    border-radius: 8px;
    text-align: center;
    color: #2c2c2c;
}

QProgressBar::chunk {
    background-color: #8bc4b0;
    border-radius: 6px;
}

QGroupBox {
    color: #2c2c2c;
    border: 1px solid #e8e4e0;
    border-radius: 10px;
    margin-top: 14px;
    padding: 18px 18px 18px 18px;
    padding-top: 46px;
    font-weight: normal;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: padding;
    subcontrol-position: top left;
    left: 18px;
    top: 14px;
    padding: 0;
    font-size: 15px;
    font-weight: 600;
    color: #2c2c2c;
    background-color: transparent;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QFrame#titleBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e8e4e0;
}

QWidget#progressWindow {
    border: 1px solid #e8e4e0;
}

QWidget#historyWindow {
    border: 1px solid #e8e4e0;
}

QFrame#historyCard {
    background-color: #ffffff;
    border: 1px solid #e8e4e0;
    border-radius: 10px;
    margin-bottom: 10px;
}

QFrame#historyCard:hover {
    border-color: #8bc4b0;
    background-color: #f8fcfb;
}

QFrame#historyCard QLabel,
QFrame#historyCard QLabel#historyCardUrl,
QFrame#historyCard QLabel#historyCardMeta {
    background-color: transparent;
}

QLabel#historyCardUrl {
    color: #2c7a6e;
    font-weight: 600;
    font-size: 13px;
}

QLabel#historyCardMeta {
    color: #7d7d7d;
    font-size: 12px;
}

QWidget#progressDotGreen {
    background-color: #4caf50;
    border-radius: 6px;
}

QWidget#progressDotRed {
    background-color: #e57373;
    border-radius: 6px;
}

QWidget#progressDotBlue {
    background-color: #64b5f6;
    border-radius: 6px;
}

QGroupBox#processGroup QLabel,
QGroupBox#processGroup QProgressBar,
QGroupBox#processGroup QWidget {
    background-color: transparent;
}

QGroupBox#processGroup QPushButton#startButton {
    background-color: #8bc4b0;
    color: #ffffff;
    border: none;
}

QGroupBox#processGroup QPushButton#startButton:hover {
    background-color: #7ab39f;
}

QGroupBox#processGroup QPushButton#startButton:pressed {
    background-color: #6aa28e;
}

QGroupBox#processGroup QPushButton#startButton:disabled {
    background-color: #c5e0d6;
    color: #ffffff;
}

QGroupBox#processGroup QWidget#progressDotGreen {
    background-color: #4caf50;
}

QGroupBox#processGroup QWidget#progressDotRed {
    background-color: #e57373;
}

QGroupBox#processGroup QWidget#progressDotBlue {
    background-color: #64b5f6;
}
"""

# Cercles de la barre de titre (pastels, meme palette)
TITLE_BAR_BUTTON_STYLE = """
QPushButton {
    border: none;
    min-width: 12px;
    max-width: 12px;
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
    padding: 0;
}

QPushButton#minButton {
    background-color: #8bc4b0;
}

QPushButton#minButton:hover {
    background-color: #5eb896;
}

QPushButton#restoreButton {
    background-color: #e8d48a;
}

QPushButton#restoreButton:hover {
    background-color: #d4b84a;
}

QPushButton#closeButton {
    background-color: #e8a89a;
}

QPushButton#closeButton:hover {
    background-color: #d97060;
}
"""

# Scrollbar flat pour la fenetre historique
HISTORY_SCROLLBAR_STYLE = """
QScrollArea#historyScrollArea {
    background-color: #faf8f6;
    border: none;
}

QScrollArea#historyScrollArea QScrollBar:vertical {
    background: #f0eeeb;
    width: 10px;
    margin: 0;
    border: none;
    border-radius: 5px;
}

QScrollArea#historyScrollArea QScrollBar::handle:vertical {
    background: #d0cec9;
    border-radius: 5px;
    min-height: 30px;
}

QScrollArea#historyScrollArea QScrollBar::handle:vertical:hover {
    background: #8bc4b0;
}

QScrollArea#historyScrollArea QScrollBar::add-line:vertical,
QScrollArea#historyScrollArea QScrollBar::sub-line:vertical {
    height: 0;
    border: none;
    background: none;
}

QScrollArea#historyScrollArea QScrollBar::add-page:vertical,
QScrollArea#historyScrollArea QScrollBar::sub-page:vertical {
    background: none;
}
"""
