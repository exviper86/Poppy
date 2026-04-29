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

from poppy.utils import Utils
from poppy.animations import Animation
from poppy.config import config

class BasePopup(QWidget):
    def __init__(self, width: int, height: int, is_hide_animation: bool, stay_on_hover: bool, order: int = -1):
        super().__init__()

        from poppy.app import App
        self._app = App.instance()
        
        self._window_width = width
        self._window_height = height
        self._origin_width = width
        self._origin_height = height
        self._is_hide_animation = is_hide_animation
        self._stay_on_hover = stay_on_hover

        self._screen_position = "center"

        self._last_theme = None
        self._last_accent_color = None

        self._setup_window()

        self._is_active = False
        self._is_mouse_over = False

        self._order = order

        self._fadeIn_anim = Animation()
        self._fadeOut_anim = Animation()
        self._in_anim = Animation()
        self._out_anim = Animation()
        self._shift_anim = Animation()
        
        self._hide_timer = QTimer()
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._hide_animation)

        self.hide()

        self._app.popup_manager.add_popup(self)

    @property
    def window_width(self) -> int:
        return self._window_width

    @property
    def window_height(self) -> int:
        return self._window_height
    
    @property
    def order(self) -> int:
        return self._order
    
    @property
    def is_mouse_over(self) -> bool:
        return self._is_mouse_over
    
    @property
    def stay_on_hover(self) -> bool:
        return self._stay_on_hover
    
    @property
    def screen_position(self) -> str:
        return self._screen_position

    @property
    def is_active(self) -> bool:
        return self._is_active

    def _setup_window(self):
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
        self.setFixedSize(self._window_width, self._window_height)
        self._create_widgets()
    
    def _create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        background_widget = QWidget()
        background_widget.setObjectName("backgroundWidget")
        #background_widget.setFixedSize(self.window_width, self.window_height)
        layout.addWidget(background_widget)
        
        self._create_content(background_widget)

    @abstractmethod
    def _create_content(self, background_widget: QWidget):
        pass

    def _apply_theme(self):
        theme = Utils.get_windows_theme()
        colors = Utils.get_theme_colors()

        accent = colors["accent"]
        
        if self._last_theme == theme and self._last_accent_color == accent:
            return
        
        self._last_theme = theme
        self._last_accent_color = accent
        
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

        self._apply_theme_content(colors)

    @abstractmethod
    def _apply_theme_content(self, colors):
        pass

    @abstractmethod
    def _update_screen_position(self):
        pass

    def shift_popup(self, shift_animation):
        if not self.isVisible():
            return

        self._shift_anim.stop()
        
        self._shift_anim = shift_animation
        self._shift_anim.run()
        
        self._show_popup()
    
    def _show_popup(self):
        self._apply_theme()
        
        if not self.isVisible():
            self._update_screen_position()
            self.move(self._app.popup_manager.get_start_position(self))
            self.show()
        
        if self._order > -1:
            self._app.popup_manager.update_popups(self)

        self._show_animation()
        
    def _show_animation(self):
        self._fadeOut_anim.stop()
        self._out_anim.stop()
        
        if not self._fadeIn_anim.is_running:
            self._hide_timer.stop()
            self._fadeIn_anim = self._app.popup_manager.get_fadeIn_animation(self)
            self._fadeIn_anim.onFinished = self._on_show_animation_end
            self._fadeIn_anim.run()
        if not self._in_anim.is_running:
            self._in_anim = self._app.popup_manager.get_in_animation(self)
            self._in_anim.run()
    
    def _on_show_animation_end(self):
        self._is_active = True
        self._hide_timer.start(self._get_duration())
            
    def _hide_animation(self):
        is_hovered = self._stay_on_hover and self._is_mouse_over
        if is_hovered:
            return 
        
        self._is_active = False
    
        self._fadeOut_anim = self._app.popup_manager.get_fadeOut_animation(self)
        self._fadeOut_anim.onFinished = self.hide
        self._fadeOut_anim.run()

        self._out_anim = self._app.popup_manager.get_out_animation(self)
        if self._is_hide_animation:
            self._out_anim.run()

    def enterEvent(self, event):
        super().enterEvent(event)
        if self._is_active and self._stay_on_hover:
            self._hide_timer.stop()
        self._is_mouse_over = True
        
    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self._is_active and self._stay_on_hover:
            self._hide_timer.start(self._get_duration())
        self._is_mouse_over = False
        
    def _get_duration(self) -> int:
        return config.common.popup_duration.value
    