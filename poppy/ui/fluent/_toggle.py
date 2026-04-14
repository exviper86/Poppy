from abc import abstractmethod

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QRectF, pyqtSignal, QPoint, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QStaticText, QFont


class Toggle(QWidget):
    toggled = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()

        self.setFixedSize(21, 21)

        self._check_font = QFont("Roboto", 10)

        # Состояние
        self._checked = False
        self._progress = 0.0 
        self._hover_progress = 0.0

        # Цвета
        self._bg_color_light = QColor("#F5F5F5")
        self._circle_color_light = QColor("#5D5D5D")
        self._border_color_light = QColor("#8A8A8A")
        self._bg_color_dark = QColor("#272727")
        self._circle_color_dark = QColor("#CECECE")
        self._border_color_dark = QColor("#9E9E9E")
        
        # Настройка анимации
        self._animation = QPropertyAnimation(self, b"_qp_progress")
        self._animation.setDuration(150)  # ms
        self._animation.setEasingCurve(QEasingCurve.Type.Linear)

        self._hover_animation = QPropertyAnimation(self, b"_qp_hover_progress")
        self._hover_animation.setDuration(150)  # ms
        self._hover_animation.setEasingCurve(QEasingCurve.Type.Linear)

    # --- Свойство для анимации ---
    def _get_progress(self):
        return self._progress

    def _set_progress(self, value):
        self._progress = value
        self.update()

    def _get_hover_progress(self):
        return self._hover_progress

    def _set_hover_progress(self, value):
        self._hover_progress = value
        self.update()

    _qp_progress = pyqtProperty(float, _get_progress, _set_progress)
    _qp_hover_progress = pyqtProperty(float, _get_hover_progress, _set_hover_progress)
    # -----------------------------

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        if self._checked == checked:
            return

        self._checked = checked
        self._animation.stop()
        
        # Запуск анимации
        if self._checked:
            self._animation.setStartValue(0.0)
            self._animation.setEndValue(1.0)
        else:
            self._animation.setStartValue(1.0)
            self._animation.setEndValue(0.0)

        self._animation.start()
        
        self.toggled.emit(self._checked) 

    def toggle(self):
        self.setChecked(not self._checked)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle()
        super().mousePressEvent(event)
    
    def enterEvent(self, event):
        self._hover_animation.stop()
        self._hover_animation.setStartValue(0.0)
        self._hover_animation.setEndValue(1.0)
        self._hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_animation.stop()
        self._hover_animation.setStartValue(1.0)
        self._hover_animation.setEndValue(0.0)
        self._hover_animation.start()
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Цвета
        palette = self.palette()
        dark_theme = palette.text().color().lightness() > 128
        
        bg = self._bg_color_dark if dark_theme else self._bg_color_light
        border = self._border_color_dark if dark_theme else self._border_color_light
        circle = self._circle_color_dark if dark_theme else self._circle_color_light
        accent = palette.accent().color()

        if dark_theme:
            bg = bg.lighter(100 + int(self._hover_progress * 30))
        else:
            bg = bg.darker(100 + int(self._hover_progress * 4))
        
        bg_color = self._lerp_color(bg, accent, self._progress)
        bd_color = self._lerp_color(border, accent, self._progress)
        fg_color = self._lerp_color(circle, QColor("black" if dark_theme else "white"), self._progress)
        
        if not self.isEnabled():
            bg_color.setAlpha(128)
            bd_color.setAlpha(128)
            fg_color.setAlpha(128)

        self._paint(painter,bd_color, bg_color, fg_color)

        painter.end()
    
    @abstractmethod
    def _paint(self, painter: QPainter, bd_color: QColor, bg_color: QColor, fg_color: QColor):
        radius = 4
        circle_radius = 2
        padding = 5 - self._hover_progress
        
        # Рисуем фон
        pen = QPen(bd_color, 1)
        painter.setPen(pen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(1, 1, self.width()-2, self.height()-2, radius, radius)

        # Рисуем checkmark
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(fg_color)
        painter.translate(self.width()/2.0, self.height()/2.0)
        painter.scale(self._progress, self._progress)
        painter.drawRoundedRect(QRectF(padding-self.width()/2.0, padding-self.height()/2.0, self.width() - padding*2, self.width() - padding*2),
                                circle_radius, circle_radius)
        painter.translate(-self.width()/2.0, -self.height()/2.0)
    
    @staticmethod
    def _lerp_color(color1, color2, factor):
        
        # Получаем компоненты (0-255)
        r1, g1, b1, a1 = color1.getRgb()
        r2, g2, b2, a2 = color2.getRgb()

        # Интерполяция
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        a = int(a1 + (a2 - a1) * factor)

        return QColor(r, g, b, a)