# base_popup.py

# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from abc import abstractmethod
from utils import get_theme_colors, get_windows_theme
from animations import Animation


class BasePopup(QWidget):
    def __init__(self, app, width, height, is_hide_animation, stay_on_hover, order = -1):
        super().__init__()

        self.app = app
        
        self.window_width = width
        self.window_height = height
        self.is_hide_animation = is_hide_animation
        self.stay_on_hover = stay_on_hover

        self.screen_position = None

        self.last_theme = None
        self.last_accent_color = None

        self.setup_window()

        self.is_active = False
        self.is_mouse_over = False

        self.order = order

        self.fadeIn_anim = Animation()
        self.fadeOut_anim = Animation()
        self.in_anim = Animation()
        self.out_anim = Animation()
        self.shift_anim = Animation()
        
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_animation)

        self.hide()
        
        self.app.popup_manager.add_popup(self)

    def setup_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.ToolTip |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)

        # self.effect = QGraphicsOpacityEffect(self)
        # self.setGraphicsEffect(self.effect)
        # self.effect.setOpacity(0.0)
        self.setWindowOpacity(0.0)

        #self.resize(self.window_width, self.window_height)
        self.setFixedSize(self.window_width, self.window_height)
        self.create_widgets()
    
    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        background_widget = QWidget()
        background_widget.setObjectName("backgroundWidget")
        #background_widget.setFixedSize(self.window_width, self.window_height)
        layout.addWidget(background_widget)

        self.create_content(background_widget)

    @abstractmethod
    def create_content(self, background_widget):
        pass

    def apply_theme(self):
        theme = get_windows_theme()
        colors = get_theme_colors()

        accent = colors["accent"]
        
        if self.last_theme == theme and self.last_accent_color == accent:
            return
        
        self.last_theme = theme
        self.last_accent_color = accent
        
        bg = colors["bg"]
        border = colors["border"]

        # self.setStyleSheet(f"""
        #     #backgroundWidget {{
        #         background-color: {bg};
        #         border: 1px solid {border};
        #         border-radius: 8px;
        #     }}
        #     QWidget {{ 
        #         border: None;
        #         background-color: transparent; 
        #     }}
        # """)
        self.setStyleSheet(f"""
            #backgroundWidget {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 8px;
            }}
        """)

        self.apply_theme_content(colors)

    @abstractmethod
    def apply_theme_content(self, colors):
        pass

    @abstractmethod
    def update_screen_position(self):
        pass

    def shift_popup(self, shift_animation):
        if not self.isVisible():
            return

        self.shift_anim.stop()
        
        self.shift_anim = shift_animation
        self.shift_anim.run()
        
        self._show_popup()
    
    def _show_popup(self):
        self.apply_theme()
        
        if not self.isVisible():
            self.update_screen_position()
            self.move(self.app.popup_manager.get_start_position(self))
            self.show()
            
        self.app.popup_manager.update_popups(self)
            
        self.show_animation()
        
    def show_animation(self):
        self.fadeOut_anim.stop()
        self.out_anim.stop()
        
        if not self.fadeIn_anim.is_running:
            self.hide_timer.stop()
            self.fadeIn_anim = self.app.popup_manager.get_fadeIn_animation(self)
            self.fadeIn_anim.onFinished = self._on_show_animation_end
            self.fadeIn_anim.run()
        if not self.in_anim.is_running:
            self.in_anim = self.app.popup_manager.get_in_animation(self)
            self.in_anim.run()
    
    def _on_show_animation_end(self):
        self.is_active = True
        self.hide_timer.start(self.app.config.popup_duration)
            
    def hide_animation(self):
        is_hovered = self.stay_on_hover and self.is_mouse_over
        if is_hovered:
            return 
        
        self.is_active = False
    
        self.fadeOut_anim = self.app.popup_manager.get_fadeOut_animation(self)
        self.fadeOut_anim.onFinished = self.hide
        self.fadeOut_anim.run()

        self.out_anim = self.app.popup_manager.get_out_animation(self)
        if self.is_hide_animation:
            self.out_anim.run()

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.is_active and self.stay_on_hover:
            self.hide_timer.stop()
        self.is_mouse_over = True
        
    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.is_active and self.stay_on_hover:
            self.hide_timer.start(self.app.config.popup_duration)
        self.is_mouse_over = False