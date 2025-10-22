# keyboard_handler.py

# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

import keyboard
import ctypes

user32 = ctypes.windll.user32

class KeyboardHandler:
    def __init__(self, app, on_layout_change_callback, on_lock_change_callback, on_volume_change_callback, on_media_change_callback):
        self.app = app
        
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.shift_pressed = False
        self.foreign_key_pressed = False
        self.on_layout_change = on_layout_change_callback
        self.on_lock_change = on_lock_change_callback
        self.on_volume_change = on_volume_change_callback
        self.on_media_change = on_media_change_callback
        self.switch_device_hotkey = None
        
        self.caps_pressed = False
        self.scroll_pressed = False
        self.num_pressed = False
        self.insert_pressed = False
        
        # Запускаем хуки
        self.setup_hooks()

    def setup_hooks(self):
        # --- Lock-клавиши ---
        keyboard.hook_key('caps lock', self.on_caps_lock)
        keyboard.hook_key('scroll lock', self.on_scroll_lock)
        keyboard.hook_key('num lock', self.on_num_lock)
        keyboard.hook_key('insert', self.on_insert)

        # --- Модификаторы ---
        keyboard.hook_key('ctrl', self.on_ctrl_event)
        keyboard.hook_key('right ctrl', self.on_ctrl_event)
        keyboard.hook_key('alt', self.on_alt_event)
        keyboard.hook_key('right alt', self.on_alt_event)
        keyboard.hook_key('shift', self.on_shift_event)
        keyboard.hook_key('right shift', self.on_shift_event)

        # --- Громкость ---
        keyboard.hook_key(-175, self.volume_buttons, suppress=True)  # Volume Up
        keyboard.hook_key(-174, self.volume_buttons, suppress=True)  # Volume Down
        keyboard.hook_key(-173, self.volume_buttons, suppress=True)  # Volume Mute

        # --- Мультимедиа ---
        keyboard.hook_key(-179, self.media_buttons)  # Play/Pause
        keyboard.hook_key(-176, self.media_buttons)  # Next Track
        keyboard.hook_key(-177, self.media_buttons)  # Previous Track

        # --- Переключение устройства ---
        self.set_switch_device_hotkey(self.app.config.audio_switch_hotkey_value)

        # --- Все остальные клавиши ---
        keyboard.hook(self.on_any_key)

    def set_switch_device_hotkey(self, hotkey: str):
        if self.switch_device_hotkey:
            keyboard.remove_hotkey(self.switch_device_hotkey)

        if self.app.config.audio_switch_hotkey and hotkey:
            keyboard.add_hotkey(hotkey, self.on_change_device, suppress=True, trigger_on_release=True)
            self.switch_device_hotkey = hotkey

    def volume_buttons(self, e):
        if not self.app.config.volume_window_enable:
            return True
        
        if e.event_type == keyboard.KEY_DOWN:
            if e.name == 'volume up':
                self.app.audio_manager.volume_up()
                self.on_volume_change(False)
            elif e.name == 'volume down':
                self.app.audio_manager.volume_down()
                self.on_volume_change(False)
            elif e.name == 'volume mute':
                self.app.audio_manager.toggle_mute()
                self.on_volume_change(False)

        return False  # Подавляем событие → системный попап не появится

    def media_buttons(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            self.on_media_change()
        return True

    # --- Обработчики Lock-клавиш ---
    def on_caps_lock(self, e):
        if e.name != "caps lock":
            return
        
        if e.event_type == keyboard.KEY_DOWN:
            if not self.caps_pressed:  # только если до этого не была нажата
                self.caps_pressed = True
                self.on_lock_change("Caps")
        elif e.event_type == keyboard.KEY_UP:
            self.caps_pressed = False
    
    def on_scroll_lock(self, e):
        if e.name != "scroll lock":
            return
        
        if e.event_type == keyboard.KEY_DOWN:
            if not self.scroll_pressed:  # только если до этого не была нажата
                self.scroll_pressed = True
                self.on_lock_change("Scroll")
        elif e.event_type == keyboard.KEY_UP:
            self.scroll_pressed = False

    def on_num_lock(self, e):
        if e.name != "num lock":
            return
        
        if e.event_type == keyboard.KEY_DOWN:
            if not self.num_pressed:  # только если до этого не была нажата
                self.num_pressed = True
                self.on_lock_change("Num")
        elif e.event_type == keyboard.KEY_UP:
            self.num_pressed = False

    def on_insert(self, e):
        if e.name != "insert":
            return 
        
        if e.event_type == keyboard.KEY_DOWN:
            if not self.insert_pressed:  # только если до этого не была нажата
                self.insert_pressed = True
                self.on_lock_change("Insert")
        elif e.event_type == keyboard.KEY_UP:
            self.insert_pressed = False
            

    # --- Обработчики модификаторов ---
    def on_ctrl_event(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            self.ctrl_pressed = True
        elif e.event_type == keyboard.KEY_UP:
            self.ctrl_pressed = False
            if self.shift_pressed and not self.foreign_key_pressed:
                self.on_layout_change()
            self.foreign_key_pressed = False

    def on_alt_event(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            self.alt_pressed = True
        elif e.event_type == keyboard.KEY_UP:
            self.alt_pressed = False
            if self.shift_pressed and not self.foreign_key_pressed:
                self.on_layout_change()
            self.foreign_key_pressed = False

    def on_shift_event(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            self.shift_pressed = True
        elif e.event_type == keyboard.KEY_UP:
            self.shift_pressed = False
            if (self.ctrl_pressed or self.alt_pressed) and not self.foreign_key_pressed:
                self.on_layout_change()
            self.foreign_key_pressed = False
    
    def on_change_device(self):
        self.app.audio_manager.switch_device()
        self.on_volume_change(True)
        return True

    # --- Обработчик любых клавиш ---
    def on_any_key(self, e):
        #print(e.name, e.scan_code)
        if e.name in ('ctrl', 'right ctrl', 'shift', 'right shift', 'alt', 'right alt', 'caps lock', 'num lock', 'scroll lock', 'insert'):
            return
        
        if e.event_type == keyboard.KEY_DOWN:
            if (self.ctrl_pressed or self.alt_pressed) and self.shift_pressed:
                self.foreign_key_pressed = True

    def stop(self):
        keyboard.unhook_all()
    
    def is_caps_lock_on(self):
        """Возвращает True, если Caps Lock включён."""
        state = user32.GetKeyState(VK_CAPS)
        return (state & 0x0001) != 0
    
    def is_num_lock_on(self):
        """Возвращает True, если Num Lock включён."""
        state = user32.GetKeyState(VK_NUM)
        return (state & 0x0001) != 0
    
    def is_scroll_lock_on(self):
        """Возвращает True, если Scroll Lock включён."""
        state = user32.GetKeyState(VK_SCROLL)
        return (state & 0x0001) != 0
    
    def is_insert_on(self):
        """Возвращает True, если Insert включён (режим вставки активен)."""
        state = user32.GetKeyState(VK_INSERT)
        return (state & 0x0001) != 0

# Virtual Key Codes
VK_CAPS = 0x14
VK_NUM = 0x90
VK_SCROLL  = 0x91
VK_INSERT = 0x2D