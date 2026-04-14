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
from ._base_popup import BasePopup
from poppy.config import config

class KeyboardPopup(BasePopup):
    def _create_content(self, background_widget):
        content_layout = QVBoxLayout(background_widget)
        content_layout.setContentsMargins(8, 4, 8, 8)
        content_layout.setSpacing(0)

        self._label_title = QLabel()
        self._label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label_title.setFont(QFont("Segoe UI Variable", 10))
        #self._label_title.setFixedHeight(18)
        content_layout.addWidget(self._label_title, alignment=Qt.AlignmentFlag.AlignCenter)

        self._label_main = QLabel()
        self._label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label_main.setFont(QFont("Segoe UI Variable", 16))
        content_layout.addWidget(self._label_main, alignment=Qt.AlignmentFlag.AlignCenter)

    def _apply_theme_content(self, colors):
        self._label_title.setStyleSheet(f"color: {colors['text']};")
        self._label_main.setStyleSheet(f"color: {colors['accent']};")

    def _update_screen_position(self):
        self._screen_position = config.keyboard_window.position.value

    def show_popup(self, title_text: str, main_text: str):
        if not config.keyboard_window.enable.value:
            return
        
        self._label_title.setText(title_text)
        self._label_main.setText(main_text)
        
        self._app.sound_manager.play_sound()
        
        self._show_popup()
        
    def _get_duration(self):
        return config.keyboard_window.duration.value \
            if config.keyboard_window.override_duration.value else config.common.popup_duration.value
