# Tooltip personnalisé avec bords arrondis (fenêtre à masque arrondi).

from PyQt6.QtCore import QRect, QRectF, QSize, Qt
from PyQt6.QtGui import QPainter, QPainterPath, QPen, QColor, QRegion
from PyQt6.QtWidgets import QWidget


def _rounded_region(rect: QRect, radius: int) -> QRegion:
    """Région en rectangle arrondi pour setMask (fenêtre vraiment arrondie)."""
    region = QRegion()
    r = rect
    # Bande horizontale centrale
    region = region.united(QRegion(r.adjusted(radius, 0, -radius, 0)))
    # Bande verticale centrale
    region = region.united(QRegion(r.adjusted(0, radius, 0, -radius)))
    # Quatre coins (ellipses)
    corner = QRect(r.topLeft(), QSize(radius * 2, radius * 2))
    region = region.united(QRegion(corner, QRegion.RegionType.Ellipse))
    corner.moveTopRight(r.topRight())
    region = region.united(QRegion(corner, QRegion.RegionType.Ellipse))
    corner.moveBottomLeft(r.bottomLeft())
    region = region.united(QRegion(corner, QRegion.RegionType.Ellipse))
    corner.moveBottomRight(r.bottomRight())
    region = region.united(QRegion(corner, QRegion.RegionType.Ellipse))
    return region


class RoundedTooltip(QWidget):
    """Fenêtre tooltip avec forme arrondie (masque) pour rester rounded quand coupé par l'écran."""

    RADIUS = 8
    PADDING_H = 12
    PADDING_V = 8
    BORDER_COLOR = "#e0ddd8"
    BG_COLOR = "#ffffff"
    TEXT_COLOR = "#2c2c2c"

    def __init__(self, text: str, parent: QWidget | None = None):
        super().__init__(parent)
        self._text = text
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        font = self.font()
        font.setPointSize(10)
        font.setFamily("Segoe UI")
        self.setFont(font)
        fm = self.fontMetrics()
        tw = fm.horizontalAdvance(text)
        th = fm.height()
        w = tw + self.PADDING_H * 2
        h = th + self.PADDING_V * 2
        self.setFixedSize(w, h)

    def setText(self, text: str) -> None:
        self._text = text
        fm = self.fontMetrics()
        tw = fm.horizontalAdvance(text)
        th = fm.height()
        self.setFixedSize(tw + self.PADDING_H * 2, th + self.PADDING_V * 2)
        self.setMask(_rounded_region(self.rect(), self.RADIUS))
        self.update()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.setMask(_rounded_region(self.rect(), self.RADIUS))

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.setMask(_rounded_region(self.rect(), self.RADIUS))

    def paintEvent(self, event) -> None:
        r = self.rect()
        path = QPainterPath()
        path.addRoundedRect(QRectF(r), float(self.RADIUS), float(self.RADIUS))
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.fillPath(path, QColor(self.BG_COLOR))
        painter.setPen(QPen(QColor(self.BORDER_COLOR), 1))
        painter.drawPath(path)
        painter.setPen(QColor(self.TEXT_COLOR))
        painter.drawText(
            r.adjusted(self.PADDING_H, self.PADDING_V, -self.PADDING_H, -self.PADDING_V),
            Qt.AlignmentFlag.AlignCenter,
            self._text,
        )
