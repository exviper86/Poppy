# volume_popup.py

# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

from base_popup import BasePopup
from PyQt6.QtWidgets import QSlider, QHBoxLayout, QLabel, QToolButton, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QMouseEvent
from utils import get_windows_theme, get_resource_path, color_with_alpha, strip_audio_name

class VolumePopup(BasePopup):
    def create_content(self, background_widget):
        main_layout = QVBoxLayout(background_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # отступы по краям
        main_layout.setSpacing(0)  # отступы между элементами
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)  # отступы по краям
        content_layout.setSpacing(0)  # отступы между элементами
        
        # Иконка громкости слева
        self.icon_label = QToolButton()
        self.icon_label.setFixedSize(QSize(40, 40))
        self.icon_label.setIconSize(QSize(25, 25))
        self.icon_label.clicked.connect(self._on_icon_click)

        # Слайдер по центру
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self._on_slider_change)

        # Текст громкости справа
        self.volume_label = QLabel("0")
        self.volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.volume_label.setFont(QFont("Segoe UI Variable", 14))
        self.volume_label.setFixedWidth(36)
        self.volume_label.setContentsMargins(0, 0, 3, 3)

        # Добавляем в layout
        content_layout.addWidget(self.icon_label, stretch=0)      # ← фиксированная ширина
        content_layout.addWidget(self.slider, stretch=1)          # ← растягивается
        content_layout.addWidget(self.volume_label, stretch=0)
        
        self.device_label = QLabel()
        self.device_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.device_label.setFont(QFont("Segoe UI Variable", 10, QFont.Weight.Medium))
        main_layout.addWidget(self.device_label)
        main_layout.addLayout(content_layout)
        
        self.origin_height = self.window_height
        
    def apply_theme_content(self, colors):
        self.icon_label.setStyleSheet(f"""
                QToolButton {{
                    background-color: transparent;
                    border: none;
                    border-radius: 8px;
                }}
                QToolButton:hover {{
                    background-color: {color_with_alpha(colors['border'], 175)};
                }}
                QToolButton:pressed {{
                    background-color: {color_with_alpha(colors['text'], 50)};
                }}
            """)

        self.device_label.setStyleSheet(f"color: {color_with_alpha(colors['text'], 175)};")

    def update_screen_position(self):
        self.screen_position = self.app.config.volume_window_position
    
    def _update_icon_by_volume(self, volume, mute):
        """Обновляет иконку в зависимости от громкости."""
        if volume == 0 or mute:
            icon_path = f"icons/{get_windows_theme()}/volume_mute.png"
        elif volume < 33:
            icon_path = f"icons/{get_windows_theme()}/volume_low.png"
        elif volume < 66:
            icon_path = f"icons/{get_windows_theme()}/volume_medium.png"
        else:
            icon_path = f"icons/{get_windows_theme()}/volume_high.png"
    
        self.icon_label.setIcon(QIcon(get_resource_path(icon_path)))
    
    def _on_icon_click(self):
        mute = self.app.audio_manager.toggle_mute()
        self._update_icon_by_volume(self.slider.value(), mute)
    
    def _on_slider_change(self, value):
        self.app.audio_manager.set_volume(value)
        self.volume_label.setText(str(value))
        self._update_icon_by_volume(value, False)
    
    def show_popup(self, device_changed = False):
        if not self.app.config.volume_window_enable:
            return
        
        volume = self.app.audio_manager.get_volume()

        show_name = self.app.config.volume_window_show_name or device_changed
        if not self.isVisible() or device_changed:
            self.window_height = (self.origin_height + 20) if show_name else self.origin_height
            self.setFixedHeight(self.window_height)
            self._update_device_name()
            self.device_label.setVisible(show_name)
        
        self.slider.blockSignals(True)
        self.slider.setValue(volume)
        self.slider.blockSignals(False)
        
        self.volume_label.setText(f"{volume}")
        self._update_icon_by_volume(volume, self.app.audio_manager.get_mute())

        self._show_popup()

        if self.app.config.volume_window_show_media and (not self.app.media_popup.isVisible() or not self.app.media_popup.is_active):
            self.app.media_popup.show_popup()
            
    def mouseDoubleClickEvent(self, a0):
        if self.app.config.audio_switch_double_tap:
            self.app.audio_manager.switch_device()
            self._update_device_name()
            
    def _update_device_name(self):
        name = self.app.audio_manager.get_device_name()
        if not self.app.config.volume_window_full_name:
            name = strip_audio_name(name)
        self.device_label.setText(name)