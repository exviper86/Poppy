# keyboard_popup.py

# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QApplication
from base_popup import BasePopup

class KeyboardPopupCursor(BasePopup):
    def create_content(self, background_widget):
        content_layout = QVBoxLayout(background_widget)
        content_layout.setContentsMargins(0, 0, 0, 2)

        self.label_main = QLabel()
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_main.setFont(QFont("Segoe UI Variable", 12))
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.label_main)

        self.timer = QTimer()
        self.timer.timeout.connect(self._move_to_cursor)

    def apply_theme_content(self, colors):
        self.label_main.setStyleSheet(f"color: {colors['accent']};")

    def show_popup(self, main_text):
        if not self.app.config.keyboard_window_enable:
            return
        
        self.label_main.setText(main_text)

        if self.app.config.keyboard_window_show_cursor:
            self.app.sound_manager.play_sound()
        
        self._show_popup()
        
        #self._move_to_cursor()
        screen = QApplication.primaryScreen()
        framerate = screen.refreshRate() if screen else 60
        interval_ms = max(1, int(1000 / framerate))
        self.timer.setInterval(interval_ms)
        self.timer.start()
    
    def hideEvent(self, a0):
        super().hideEvent(a0)
        self.timer.stop()
    
    def _move_to_cursor(self):
        cursor_pos = QCursor.pos()  # глобальная позиция курсора
        screen = self.screen().availableGeometry()
    
        popup_width = self.width()
        popup_height = self.height()
    
        # Смещение, чтобы popup не закрывал курсор
        offset_x = 10
        offset_y = 23
    
        x = cursor_pos.x() + offset_x
        y = cursor_pos.y() + offset_y
    
        # Убедимся, что popup не вылезает за границы экрана
        if x + popup_width > screen.right():
            x = screen.right() - popup_width
        if y + popup_height > screen.bottom():
            y = screen.bottom() - popup_height
        if x < screen.left():
            x = screen.left()
        if y < screen.top():
            y = screen.top()
    
        self.move(x, y)

    def _get_duration(self):
        return self.app.config.keyboard_window_duration if self.app.config.keyboard_window_override_duration else self.app.config.popup_duration
