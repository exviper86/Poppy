from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen
from ._toggle import Toggle

class Switch(Toggle):
    def __init__(self):
        super().__init__()
        self.setFixedSize(41, 21)
        
    def _paint(self, painter: QPainter, bd_color: QColor, bg_color: QColor, fg_color: QColor):
        radius = self.height() / 2
        circle_radius = radius - 4.5 + self._hover_progress
        padding = 4.5 - self._hover_progress

        # Рисуем фон (скругленный прямоугольник)
        pen = QPen(bd_color, 1)
        painter.setPen(pen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(1, 1, self.width()-2, self.height()-2, radius, radius)

        # Рисуем круг (кнопку)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(fg_color)

        # Вычисляем позицию круга на основе прогресса
        start_x = padding
        end_x = self.width() - (circle_radius * 2) - padding

        current_x = start_x + (end_x - start_x) * self._progress

        painter.drawEllipse(QRectF(current_x, radius - circle_radius, circle_radius * 2, circle_radius * 2))