# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt6.QtCore import QTimer
from .hooks import *
import ctypes
from .config import config

user32 = ctypes.windll.user32

class KeyboardHandler:
    def __init__(self):
        from .app import App
        self._app = App.instance()
        
        self._ctrl_pressed = False
        self._alt_pressed = False
        self._shift_pressed = False
        self._foreign_key_pressed = False
        self._switch_device_hotkey_id: int | None = None
        
        self._setup_hooks()

    def _setup_hooks(self):
        # --- Lock-клавиши ---
        keyboard.hook_hotkey([keys.caps_lock], lambda: self._on_lock_key("Caps"))
        keyboard.hook_hotkey([keys.scroll_lock], lambda: self._on_lock_key("Scroll"))
        keyboard.hook_hotkey([keys.num_lock], lambda: self._on_lock_key("Num"))
        keyboard.hook_hotkey([keys.insert], lambda: self._on_lock_key("Insert"))

        # --- Модификаторы ---
        keyboard.hook_key(keys.left_ctrl, self._on_ctrl_event)
        keyboard.hook_key(keys.right_ctrl, self._on_ctrl_event)
        keyboard.hook_key(keys.left_alt, self._on_alt_event)
        keyboard.hook_key(keys.right_alt, self._on_alt_event)
        keyboard.hook_key(keys.left_shift, self._on_shift_event)
        keyboard.hook_key(keys.right_shift, self._on_shift_event)

        # --- Громкость ---
        keyboard.hook_key(keys.volume_up, self._volume_buttons)
        keyboard.hook_key(keys.volume_down, self._volume_buttons)
        keyboard.hook_key(keys.volume_mute, self._volume_buttons)
        
        # --- Мультимедиа ---
        keyboard.hook_key(keys.play_pause, self._media_buttons)
        keyboard.hook_key(keys.next_track, self._media_buttons)
        keyboard.hook_key(keys.previous_track, self._media_buttons)

        # --- Переключение устройства ---
        self._set_switch_device_hotkey(config.audio_switch.hotkey_value.value)
        config.audio_switch.hotkey_value.valueChanged.connect(self._set_switch_device_hotkey)

        # --- Все остальные клавиши ---
        keyboard.hook(self._on_any_key)

    def start(self):
        if not keyboard.is_running:
            keyboard.start()

    def stop(self):
        if keyboard.is_running:
            keyboard.stop()
    
    def _on_lock_key(self, lock_name: str):
        self._app.call_soon_threadsafe(lambda: QTimer.singleShot(20, lambda: self._app.show_lock_popup(lock_name)))

    def _show_layout(self):
        self._app.call_soon_threadsafe(lambda: QTimer.singleShot(20, self._app.show_layout))

    def _show_volume(self, callback: callable, device_changed: bool = False):
        self._app.call_soon_threadsafe(callback)
        self._app.call_soon_threadsafe(self._app.show_volume_popup, device_changed)
    
    def _set_switch_device_hotkey(self, hotkey: str):
        if self._switch_device_hotkey_id:
            keyboard.unhook_hotkey(self._switch_device_hotkey_id)
            self._switch_device_hotkey_id = None
        if hotkey:
            self._switch_device_hotkey_id = keyboard.hook_hotkey(hotkey, self._on_change_device)
    
    def _volume_buttons(self, e: KeyEvent):
        if not config.volume_window.enable.value:
            return True
        
        if e.event_type == KeyEventType.PRESS:
            if e.key == keys.volume_up:
                self._show_volume(self._app.audio_manager.volume_up)
            elif e.key == keys.volume_down:
                self._show_volume(self._app.audio_manager.volume_down)
            elif e.key == keys.volume_mute:
                self._show_volume(self._app.audio_manager.toggle_mute)

        return False  # Подавляем событие → системный попап не появится

    def _media_buttons(self, e: KeyEvent):
        if e.event_type == KeyEventType.PRESS:
            self._app.call_soon_threadsafe(self._app.show_media_popup)
    
    # --- Обработчики модификаторов ---
    def _on_ctrl_event(self, e: KeyEvent):
        if e.event_type == KeyEventType.PRESS:
            self._ctrl_pressed = True
        elif e.event_type == KeyEventType.RELEASE:
            if not self._ctrl_pressed:
                return 
            self._ctrl_pressed = False
            if self._shift_pressed and not self._foreign_key_pressed:
                self._show_layout()
            self._foreign_key_pressed = False

    def _on_alt_event(self, e: KeyEvent):
        if e.event_type == KeyEventType.PRESS:
            self._alt_pressed = True
        elif e.event_type == KeyEventType.RELEASE:
            if not self._alt_pressed:
                return
            self._alt_pressed = False
            if self._shift_pressed and not self._foreign_key_pressed:
                self._show_layout()
            self._foreign_key_pressed = False

    def _on_shift_event(self, e: KeyEvent):
        if e.event_type == KeyEventType.PRESS:
            self._shift_pressed = True
        elif e.event_type == KeyEventType.RELEASE:
            if not self._shift_pressed:
                return
            self._shift_pressed = False
            if (self._ctrl_pressed or self._alt_pressed) and not self._foreign_key_pressed:
                self._show_layout()
            self._foreign_key_pressed = False
    
    def _on_change_device(self):
        if not config.audio_switch.hotkey.value:
            return

        self._show_volume(self._app.audio_manager.switch_device, True)

    # --- Обработчик любых клавиш ---
    def _on_any_key(self, e: KeyEvent):
        if e.key.name in ('ctrl', 'right ctrl', 'shift', 'right shift', 'alt', 'right alt', 'caps lock', 'num lock', 'scroll lock', 'insert'):
            return
        
        if e.event_type == KeyEventType.PRESS:
            if (self._ctrl_pressed or self._alt_pressed) and self._shift_pressed:
                self._foreign_key_pressed = True