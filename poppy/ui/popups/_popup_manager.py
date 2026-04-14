# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt6.QtCore import QPoint
from poppy.animations import Animation
from poppy.config import config
from ._base_popup import BasePopup

class PopupManager:
    def __init__(self):
        self._popups = []
        
        self._PADDING = 20
        self._TASKBAR_PADDING = 45
        self._SLIDE_OFFSET = 50
        self._SPACE = 8
        
        self._block = False
        
    def add_popup(self, popup: BasePopup):
        self._popups.append(popup)
        
    def update_popups(self, popup: BasePopup):
        if self._block:
            return
        
        self._block = True
        for p in self._popups:
            if p != popup and p.is_active and p.screen_position == popup.screen_position:
                p.shift_popup(self._get_shift_animation(p))
        self._block = False
        
    def get_start_position(self, popup: BasePopup):
        if config.common.animation.value:
            return self._get_position(popup) + self._get_slide_offset(popup)
        else:
            return self._get_position(popup)
    
    def get_fadeIn_animation(self, popup: BasePopup):
        anim = Animation()
        anim.getStartValueOnRun = True
        anim.endValue = config.common.popup_transparency.value / 100
        anim.duration = config.common.popup_show_duration.value
        anim.getter = lambda: popup.windowOpacity()
        anim.setter = lambda v: popup.setWindowOpacity(v)
        return anim

    def get_in_animation(self, popup: BasePopup):
        anim = Animation()
        if config.common.animation.value and popup.screen_position:
            anim.getStartValueOnRun = True
            anim.endValue = self._get_position(popup)
            anim.duration = config.common.popup_show_duration.value
            anim.getter = lambda: popup.pos()
            anim.setter = lambda v: popup.move(v)
        return anim   
    
    def get_fadeOut_animation(self, popup: BasePopup):
        anim = Animation()
        anim.getStartValueOnRun = True
        anim.endValue = 0.0
        anim.duration = config.common.popup_show_duration.value * 2
        anim.getter = lambda: popup.windowOpacity()
        anim.setter = lambda v: popup.setWindowOpacity(v)
        return anim

    def get_out_animation(self, popup: BasePopup):
        anim = Animation()
        if config.common.animation.value and popup.screen_position:
            anim.getStartValueOnRun = True
            anim.endValue = popup.pos() + self._get_slide_offset(popup)
            anim.duration = config.common.popup_show_duration.value * 2
            anim.getter = lambda: popup.pos()
            anim.setter = lambda v: popup.move(v)
        return anim

    def _get_shift_animation(self, popup: BasePopup):
        anim = Animation()
        anim.getStartValueOnRun = True
        anim.endValue = self._get_position(popup)
        anim.duration = config.common.popup_show_duration.value
        anim.getter = lambda: popup.pos()
        anim.setter = lambda v: popup.move(v)
        return anim

    def _get_position(self, popup: BasePopup):
        if not popup.screen_position:
            return popup.pos()
        
        if popup.stay_on_hover and popup.is_mouse_over:
            return popup.pos()
        
        screen = popup.screen()
        if not screen:
            return QPoint(0, 0)

        screen_geo = screen.availableGeometry()
        w, h = popup.window_width, popup.window_height

        paddingX = self._PADDING
        paddingY = self._PADDING
        taskbar_padding = self._TASKBAR_PADDING if config.common.taskbar.value else 0

        if popup.screen_position == "left-top":
            popup_position = QPoint(paddingX, paddingY)
        elif popup.screen_position == "left":
            popup_position = QPoint(paddingX, (screen_geo.height() - h) // 2 - h)
        elif popup.screen_position == "top":
            popup_position = QPoint((screen_geo.width() - w) // 2, paddingY)
        elif popup.screen_position == "right-top":
            popup_position = QPoint(screen_geo.width() - w - paddingX, paddingY)
        elif popup.screen_position == "right":
            popup_position = QPoint(screen_geo.width() - w - paddingX, (screen_geo.height() - h) // 2 - h)
        elif popup.screen_position == "center":
            popup_position = QPoint((screen_geo.width() - w) // 2, (screen_geo.height() - h) // 2 - h)
        elif popup.screen_position == "left-bottom":
            popup_position = QPoint(paddingX, screen_geo.height() - h - paddingY - taskbar_padding)
        elif popup.screen_position == "bottom":
            popup_position = QPoint((screen_geo.width() - w) // 2, screen_geo.height() - h - paddingY - taskbar_padding)
        elif popup.screen_position == "right-bottom":
            popup_position = QPoint(screen_geo.width() - w - paddingX, screen_geo.height() - h - paddingY - taskbar_padding)
        else:
            popup_position = QPoint((screen_geo.width() - w) // 2, (screen_geo.height() - h) // 2)

        prev = self._find_nearest_lower_popup(popup)
        if prev:
            if "top" in popup.screen_position:
                popup_position.setY(self._get_position(prev).y() + prev.window_height + self._SPACE)
            else:
                popup_position.setY(self._get_position(prev).y() - h - self._SPACE)

        return popup_position

    def _get_slide_offset(self, popup: BasePopup):
        if not popup.screen_position:
            return QPoint(0, 0)

        if popup.screen_position.startswith("left"):
            offset = QPoint(-self._SLIDE_OFFSET, 0)
        elif popup.screen_position.startswith("right"):
            offset = QPoint(self._SLIDE_OFFSET, 0)
        elif popup.screen_position == "top":
            offset = QPoint(0, -self._SLIDE_OFFSET)
        else:
            offset = QPoint(0, self._SLIDE_OFFSET)
        return offset

    def _find_nearest_lower_popup(self, popup: BasePopup):
        prev_popup = None
        order = -1
    
        for p in self._popups:
            if p is popup or not p.isVisible() or p.screen_position != popup.screen_position:
                continue
    
            if order < p.order < popup.order:
                order = p.order
                prev_popup = p
    
        return prev_popup