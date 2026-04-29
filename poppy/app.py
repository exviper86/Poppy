# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject
import asyncio
import qasync
from .config import config
from .hooks import keyboard
from .sound_manager import SoundManager
from .audio_manager import AudioManager
from .keyboard_handler import KeyboardHandler
from .ui.popups import PopupManager, KeyboardPopup, VolumePopup, MediaInfoPopup, KeyboardPopupCursor
from .ui import MainWindow
from .tray_manager import TrayManager
from .language_handler import LanguageHandler
from .layout_switcher import LayoutSwitcher
from .utils import Utils
from .translations import localizer as loc, translations as trans

class App(QObject):    
    @staticmethod
    def instance():
        return _instance
    
    def __init__(self):
        super().__init__()

        global _instance
        _instance = self
                
        # import os
        # os.environ["QT_SCALE_FACTOR"] = "1.1"
        
        self._qt_app: QApplication = QApplication(sys.argv)
        self._qt_app.setQuitOnLastWindowClosed(False)

        # НОВОЕ: создаём qasync-совместимый event loop
        self._loop = qasync.QEventLoop(self._qt_app)
        asyncio.set_event_loop(self._loop)

        lang = config.common.language.value if config.common.language.value else Utils.get_windows_ui_language()
        loc.set_language(lang)
        
        self._sound_manager: SoundManager = SoundManager()
        self._audio_manager: AudioManager = AudioManager()
        self._popup_manager: PopupManager = PopupManager()
        
        self._tray: TrayManager = TrayManager()

        self._keyboard_popup: KeyboardPopup = KeyboardPopup(180, 64, False, False, 2)
        self._volume_popup: VolumePopup = VolumePopup(300, 40, True, True, 0)
        self._media_popup: MediaInfoPopup = MediaInfoPopup(300, 98, True, True, 1)
        self._keyboard_popup_cursor: KeyboardPopupCursor = KeyboardPopupCursor(50, 30, False, False)

        self._language_handler: LanguageHandler = LanguageHandler()
        self._keyboard_handler: KeyboardHandler = KeyboardHandler()
        self._layout_switcher: LayoutSwitcher = LayoutSwitcher()

        self._current_layout = self._language_handler.get_layout()

        icon_path = Utils.get_resource_path('icon.ico')
        self._qt_app.setWindowIcon(QIcon(icon_path))

        self._main_window: MainWindow = MainWindow()
                    
    @property
    def sound_manager(self) -> SoundManager:
        return self._sound_manager

    @property
    def audio_manager(self) -> AudioManager:
        return self._audio_manager
    
    @property
    def popup_manager(self) -> PopupManager:
        return self._popup_manager
    
    @property
    def keyboard_popup(self) -> KeyboardPopup:
        return self._keyboard_popup
    
    @property
    def volume_popup(self) -> VolumePopup:
        return self._volume_popup
    
    @property
    def media_popup(self) -> MediaInfoPopup:
        return self._media_popup
    
    @property
    def keyboard_handler(self) -> KeyboardHandler:
        return self._keyboard_handler

    @property
    def language_handler(self) -> LanguageHandler:
        return self._language_handler

    @property
    def layout_switcher(self) -> LayoutSwitcher:
        return self._layout_switcher
    
    def call_soon(self, callback, *args):
        self._loop.call_soon(callback, *args)

    def call_soon_threadsafe(self, callback, *args):
        self._loop.call_soon_threadsafe(callback, *args)

    def show_layout(self, layout: int | None = None):
        if layout is None:
            layout = self._language_handler.get_layout()
        
        if layout == self._current_layout:
            return

        self._current_layout = layout

        if config.keyboard_window.show_language.value:
            if config.keyboard_window.show_cursor.value:
                self._keyboard_popup_cursor.show_popup(self._language_handler.get_layout_code(layout))
            else:
                self._keyboard_popup.show_popup(loc.tr(trans.input_language), self._language_handler.get_layout_name(layout))
    
    def show_lock_popup(self, lock_name: str):
        if not config.keyboard_window.show_modifiers.value:
            return

        status_text = f"{lock_name} "
        if lock_name == "Caps":
            status_text += loc.tr(trans.on.lower() if keyboard.get_caps_lock() else trans.off.lower())
        elif lock_name == "Scroll":
            status_text += loc.tr(trans.on.lower() if keyboard.get_scroll_lock() else trans.off.lower())
        elif lock_name == "Num":
            status_text += loc.tr(trans.on.lower() if keyboard.get_num_lock() else trans.off.lower())
        elif lock_name == "Insert":
            status_text = loc.tr(trans.replace if keyboard.get_insert() else trans.insert)

        self._keyboard_popup.show_popup(loc.tr(trans.lock), status_text)

    def show_volume_popup(self, device_changed: bool = False):
        self._volume_popup.show_popup(device_changed)
        
        if device_changed:
            return 
        
        if config.volume_window.show_media.value and (not self.media_popup.isVisible() or not self.media_popup.is_active):
            self.media_popup.show_popup()

    def show_media_popup(self):
        self._media_popup.show_popup()

        if config.media_window.show_volume.value and (not self.volume_popup.isVisible() or not self.volume_popup.is_active):
            self.volume_popup.show_popup()

    def show_settings_window(self):
        if self._main_window.isVisible():
            return

        self._main_window.show()
        self._main_window.raise_()
        self._main_window.activateWindow()

    def run(self):
        # Запускаем мониторинг медиа-сессий после старта цикла
        self._loop.call_soon(self._media_popup.start)
        self._loop.call_soon(self._keyboard_handler.start)
        self._loop.call_soon(self._layout_switcher.start)
        
        # Запускаем qasync loop вместо qt_app.exec()
        try:
            with self._loop:
                self._loop.run_forever()
        finally:
            self.shutdown()

    def shutdown(self):
        self.cleanup()
        self._loop.stop()
        self._qt_app.exit()

    def cleanup(self):
        self._keyboard_handler.stop()
        self._layout_switcher.stop()

_instance: App | None = None