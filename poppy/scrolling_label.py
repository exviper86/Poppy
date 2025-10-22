# scrolling_label.py

from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QFontMetrics

class ScrollingLabel(QLabel):
    def __init__(self, step = 0.33, parent=None):
        super().__init__(parent)
        self._scroll_enabled = False
        self._scroll_offset = 0.0
        self._scroll_step = step

        screen = QApplication.primaryScreen()
        framerate = screen.refreshRate() if screen else 60
        interval_ms = max(1, int(1000 / framerate))
        
        self._scroll_timer = QTimer(self)
        self._scroll_timer.timeout.connect(self._update_scroll)
        self._scroll_timer.setInterval(interval_ms)
        self.setText("")

    def setText(self, text):
        super().setText(text)
        self._reset_scroll()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reset_scroll()

    def _reset_scroll(self):
        if not self.text():
            self._scroll_enabled = False
            self._scroll_timer.stop()
            return

        fm = QFontMetrics(self.font())
        self._text_width = fm.horizontalAdvance(self.text())
        self._label_width = self.width()
    
        if self._text_width <= self._label_width:
            self._scroll_enabled = False
            self._scroll_timer.stop()
            self.update()
        else:
            self._scroll_enabled = True
            self._scroll_offset = 0.0
            if not self._scroll_timer.isActive():
                self._scroll_timer.start()
    
    def paintEvent(self, event):
        if not self._scroll_enabled:
            super().paintEvent(event)
            return
    
        painter = self._get_painter()
        # Рисуем два экземпляра текста подряд
        text = self.text()
        total_width = self._text_width * 2 + 20  # +20 для небольшого пробела между повторами
    
        # Первый экземпляр
        rect1 = QRectF(-self._scroll_offset, 0, self._text_width, self.height())
        painter.drawText(rect1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)
    
        # Второй экземпляр (справа от первого)
        rect2 = QRectF(-self._scroll_offset + self._text_width + 20, 0, self._text_width, self.height())
        painter.drawText(rect2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)
    
    def _update_scroll(self):
        if not self._scroll_enabled:
            return
    
        # Сбрасываем смещение, когда первый текст полностью ушёл влево
        if self._scroll_offset > self._text_width + 20:
            self._scroll_offset -= (self._text_width + 20)
        else:
            self._scroll_offset += self._scroll_step
    
        self.update()

    def _get_painter(self):
        from PyQt6.QtGui import QPainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        return painter