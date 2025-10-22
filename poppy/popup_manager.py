# popup_manager.py

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
from animations import Animation

class PopupManager:
    def __init__(self, config):
        self.config = config
        
        self.popups = []
        
        self.PADDING = 20
        self.TASKBAR_PADDING = 45
        self.SLIDE_OFFSET = 50
        self.SPACE = 8
        
        self.block = False
        
    def add_popup(self, popup):
        self.popups.append(popup)
        
    def update_popups(self, popup):
        if self.block:
            return
        
        self.block = True
        for p in self.popups:
            if p != popup and p.is_active and p.screen_position == popup.screen_position:
                p.shift_popup(self._get_shift_animation(p))
        self.block = False
        
    def get_start_position(self, popup):
        if self.config.animation:
            return self._get_position(popup) + self._get_slide_offset(popup)
        else:
            return self._get_position(popup)
    
    def get_fadeIn_animation(self, popup):
        anim = Animation()
        anim.getStartValueOnRun = True
        anim.endValue = self.config.popup_transparency / 100
        anim.duration = self.config.popup_show_duration
        anim.getter = lambda: popup.windowOpacity()
        anim.setter = lambda v: popup.setWindowOpacity(v)
        return anim

    def get_in_animation(self, popup):
        anim = Animation()
        if self.config.animation and popup.screen_position:
            anim.getStartValueOnRun = True
            anim.endValue = self._get_position(popup)
            anim.duration = self.config.popup_show_duration
            anim.getter = lambda: popup.pos()
            anim.setter = lambda v: popup.move(v)
        return anim   
    
    def get_fadeOut_animation(self, popup):
        anim = Animation()
        anim.getStartValueOnRun = True
        anim.endValue = 0.0
        anim.duration = self.config.popup_show_duration * 2
        anim.getter = lambda: popup.windowOpacity()
        anim.setter = lambda v: popup.setWindowOpacity(v)
        return anim

    def get_out_animation(self, popup):
        anim = Animation()
        if self.config.animation and popup.screen_position:
            anim.getStartValueOnRun = True
            anim.endValue = popup.pos() + self._get_slide_offset(popup)
            anim.duration = self.config.popup_show_duration * 2
            anim.getter = lambda: popup.pos()
            anim.setter = lambda v: popup.move(v)
        return anim

    def _get_shift_animation(self, popup):
        anim = Animation()
        anim.getStartValueOnRun = True
        anim.endValue = self._get_position(popup)
        anim.duration = self.config.popup_show_duration
        anim.getter = lambda: popup.pos()
        anim.setter = lambda v: popup.move(v)
        return anim

    def _get_position(self, popup):
        if not popup.screen_position:
            return popup.pos()
        
        if popup.stay_on_hover and popup.is_mouse_over:
            return popup.pos()
        
        screen = popup.screen()
        if not screen:
            return QPoint(0, 0)

        screen_geo = screen.availableGeometry()
        w, h = popup.window_width, popup.window_height

        paddingX = self.PADDING
        paddingY = self.PADDING
        taskbar_padding = self.TASKBAR_PADDING if self.config.taskbar else 0

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
                popup_position.setY(self._get_position(prev).y() + prev.window_height + self.SPACE)
            else:
                popup_position.setY(self._get_position(prev).y() - h - self.SPACE)

        return popup_position

    def _get_slide_offset(self, popup):
        if not popup.screen_position:
            return QPoint(0, 0)

        if popup.screen_position.startswith("left"):
            offset = QPoint(-self.SLIDE_OFFSET, 0)
        elif popup.screen_position.startswith("right"):
            offset = QPoint(self.SLIDE_OFFSET, 0)
        elif popup.screen_position == "top":
            offset = QPoint(0, -self.SLIDE_OFFSET)
        else:
            offset = QPoint(0, self.SLIDE_OFFSET)
        return offset

    def _find_nearest_lower_popup(self, popup):
        prev_popup = None
        order = -1
    
        for p in self.popups:
            if p is popup or not p.isVisible() or p.screen_position != popup.screen_position:
                continue
    
            if order < p.order < popup.order:
                order = p.order
                prev_popup = p
    
        return prev_popup