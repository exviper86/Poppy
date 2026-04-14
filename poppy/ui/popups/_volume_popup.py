# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

from ._base_popup import BasePopup
from PyQt6.QtWidgets import QSlider, QHBoxLayout, QLabel, QToolButton, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from poppy.utils import Utils
from poppy.config import config

class VolumePopup(BasePopup):
    def _create_content(self, background_widget):
        main_layout = QVBoxLayout(background_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # отступы по краям
        main_layout.setSpacing(0)  # отступы между элементами
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)  # отступы по краям
        content_layout.setSpacing(0)  # отступы между элементами
        
        # Иконка громкости слева
        self._icon_label = QToolButton()
        self._icon_label.setFixedSize(QSize(40, 40))
        self._icon_label.setIconSize(QSize(25, 25))
        self._icon_label.clicked.connect(self._on_icon_click)

        # Слайдер по центру
        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setRange(0, 100)
        self._slider.valueChanged.connect(self._on_slider_change)

        # Текст громкости справа
        self._volume_label = QLabel("0")
        self._volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._volume_label.setFont(QFont("Segoe UI Variable", 14))
        self._volume_label.setFixedWidth(40)
        self._volume_label.setContentsMargins(0, 0, 3, 3)

        # Добавляем в layout
        content_layout.addWidget(self._icon_label, stretch=0)      # ← фиксированная ширина
        content_layout.addWidget(self._slider, stretch=1)          # ← растягивается
        content_layout.addWidget(self._volume_label, stretch=0)
        
        self._device_label = QLabel()
        self._device_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self._device_label.setFont(QFont("Segoe UI Variable", 10, QFont.Weight.Medium))
        main_layout.addWidget(self._device_label)
        main_layout.addLayout(content_layout)
        
        self._origin_height = self.window_height
        
    def _apply_theme_content(self, colors):
        self._icon_label.setStyleSheet(f"""
                QToolButton {{
                    background-color: transparent;
                    border: none;
                    border-radius: 8px;
                }}
                QToolButton:hover {{
                    background-color: {Utils.color_with_alpha(colors['border'], 175)};
                }}
                QToolButton:pressed {{
                    background-color: {Utils.color_with_alpha(colors['text'], 50)};
                }}
            """)

        self._device_label.setStyleSheet(f"color: {Utils.color_with_alpha(colors['text'], 175)};")

    def _update_screen_position(self):
        self._screen_position = config.volume_window.position.value
    
    def _update_icon_by_volume(self, volume, mute):
        """Обновляет иконку в зависимости от громкости."""
        if volume == 0 or mute:
            icon_path = f"icons/{Utils.get_windows_theme()}/volume_mute.png"
        elif volume < 33:
            icon_path = f"icons/{Utils.get_windows_theme()}/volume_low.png"
        elif volume < 66:
            icon_path = f"icons/{Utils.get_windows_theme()}/volume_medium.png"
        else:
            icon_path = f"icons/{Utils.get_windows_theme()}/volume_high.png"
    
        self._icon_label.setIcon(QIcon(Utils.get_resource_path(icon_path)))
    
    def _on_icon_click(self):
        mute = self._app.audio_manager.toggle_mute()
        self._update_icon_by_volume(self._slider.value(), mute)
    
    def _on_slider_change(self, value):
        self._app.audio_manager.set_volume(value)
        self._volume_label.setText(str(value))
        self._update_icon_by_volume(value, False)
    
    def show_popup(self, device_changed: bool = False):
        if not config.volume_window.enable.value:
            return
        
        volume = self._app.audio_manager.get_volume()

        show_name = config.volume_window.show_name.value or device_changed
        if not self.isVisible() or device_changed:
            self._window_height = (self._origin_height + 20) if show_name else self._origin_height
            self.setFixedHeight(self.window_height)
            self._update_device_name()
            self._device_label.setVisible(show_name)
        
        self._slider.blockSignals(True)
        self._slider.setValue(volume)
        self._slider.blockSignals(False)
        
        self._volume_label.setText(f"{volume}")
        self._update_icon_by_volume(volume, self._app.audio_manager.get_mute())

        self._show_popup()

        if config.volume_window.show_media.value and (not self._app.media_popup.isVisible() or not self._app.media_popup.is_active):
            self._app.media_popup.show_popup()
            
    def _get_duration(self):
        return config.volume_window.duration.value \
            if config.volume_window.override_duration.value else config.common.popup_duration.value
            
    def mouseDoubleClickEvent(self, a0):
        if config.audio_switch.double_tap.value:
            self._app.audio_manager.switch_device()
            self._update_device_name()

    def _update_device_name(self):
        name = self._app.audio_manager.get_device_name()
        if not config.volume_window.full_name.value:
            name = Utils.strip_audio_name(name)
        self._device_label.setText(name)