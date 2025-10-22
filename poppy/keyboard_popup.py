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

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel
from base_popup import BasePopup

class KeyboardPopup(BasePopup):
    def create_content(self, background_widget):
        content_layout = QVBoxLayout(background_widget)
        content_layout.setContentsMargins(8, 4, 8, 8)
        content_layout.setSpacing(0)

        self.label_title = QLabel()
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setFont(QFont("Segoe UI Variable", 10))
        #self.label_title.setFixedHeight(18)
        content_layout.addWidget(self.label_title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.label_main = QLabel()
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_main.setFont(QFont("Segoe UI Variable", 16))
        content_layout.addWidget(self.label_main, alignment=Qt.AlignmentFlag.AlignCenter)

    def apply_theme_content(self, colors):
        self.label_title.setStyleSheet(f"color: {colors['text']};")
        self.label_main.setStyleSheet(f"color: {colors['accent']};")

    def update_screen_position(self):
        self.screen_position = self.app.config.keyboard_window_position

    def show_popup(self, title_text, main_text):
        if not self.app.config.keyboard_window_enable:
            return
        
        self.label_title.setText(title_text)
        self.label_main.setText(main_text)
        
        if not self.app.config.keyboard_window_show_cursor:
            self.app.sound_manager.play_sound()
        
        self._show_popup()
