# main.py

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
import win32event
import win32api
import winerror
import ctypes

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from config import Config
from sound_manager import SoundManager
from audio_manager import AudioManager
from popup_manager import PopupManager
from keyboard_handler import KeyboardHandler
from keyboard_popup import KeyboardPopup
from keyboard_popup_cursor import KeyboardPopupCursor
from volume_popup import VolumePopup
from media_info_popup import MediaInfoPopup
from tray_manager import TrayManager
from settings_window import SettingsWindow
from utils import get_resource_path, get_windows_ui_language
from language_handler import LanguageHandler
import asyncio
import qasync
from translations import localizer as loc, translations as trans

APP_MUTEX_HANDLE = None

def is_already_running():
    global APP_MUTEX_HANDLE
    mutex_name = "Global\\PoppyMutex"
    mutex = win32event.CreateMutex(None, False, mutex_name)

    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        win32api.CloseHandle(mutex)
        return True

    APP_MUTEX_HANDLE = mutex
    return False

def show_already_running_message():
    ctypes.windll.user32.MessageBoxW(
        0,
        "Приложение Poppy уже работает в фоне.\nПроверьте системный трей.",
        "Уже запущено",
        0x30  # MB_ICONWARNING
    )

def cleanup_mutex():
    global APP_MUTEX_HANDLE
    if APP_MUTEX_HANDLE:
        try:
            win32api.CloseHandle(APP_MUTEX_HANDLE)
        except Exception:
            pass
        APP_MUTEX_HANDLE = None


class App(QObject):
    
    layout_update_requested = pyqtSignal()
    lock_update_requested = pyqtSignal(str)
    volume_update_requested = pyqtSignal(bool)
    media_update_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.layout_update_requested.connect(lambda: QTimer.singleShot(10, self.update_and_show_layout))
        self.lock_update_requested.connect(lambda lock_name: QTimer.singleShot(10, lambda: self.show_lock_popup(lock_name)))
        self.volume_update_requested.connect(self.show_volume_popup)
        self.media_update_requested.connect(self.show_media_popup)
        
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setQuitOnLastWindowClosed(False)
        
        # НОВОЕ: создаём qasync-совместимый event loop
        self.loop = qasync.QEventLoop(self.qt_app)
        asyncio.set_event_loop(self.loop)

        self.config = Config()
        
        lang = self.config.language if self.config.language else get_windows_ui_language()
        loc.set_language(lang)
        
        self.sound_manager = SoundManager(self.config)
        self.audio_manager = AudioManager(self.config)
        self.popup_manager = PopupManager(self.config)
        self.tray = TrayManager(self)
        
        self.keyboard_popup = KeyboardPopup(self, 180, 64, False, False, 2)
        self.volume_popup = VolumePopup(self, 300, 40, True, True, 0)
        self.media_popup = MediaInfoPopup(self, 300, 98, True, True, 1)

        self.keyboard_popup_cursor = KeyboardPopupCursor(self, 50, 30, False, False)

        self.language_handler = LanguageHandler()
        self.keyboard_handler = KeyboardHandler(
            self,
            self.trigger_layout_update,
            self.trigger_lock_update,
            self.trigger_volume_update,
            self.trigger_media_update
        )

        self._settings_window = SettingsWindow(self)
        
        self.current_layout = self.language_handler.get_layout_id()

        icon_path = get_resource_path('icon.ico')
        self.qt_app.setWindowIcon(QIcon(icon_path))

    def trigger_layout_update(self):
        self.layout_update_requested.emit()
        
    def trigger_lock_update(self, lock_name):
        self.lock_update_requested.emit(lock_name)
        
    def trigger_volume_update(self, device_changed):
        self.volume_update_requested.emit(device_changed)

    def trigger_media_update(self):
        self.media_update_requested.emit()

    def update_and_show_layout(self):
        new_layout = self.language_handler.get_layout_id()
        if new_layout == self.current_layout:
            return

        self.current_layout = new_layout
         
        if self.config.keyboard_window_show_language:
            if self.config.keyboard_window_show_cursor:
                self.keyboard_popup_cursor.show_popup(self.language_handler.get_code(new_layout))
            else:
                self.keyboard_popup.show_popup(loc.tr(trans.input_language), self.language_handler.get_name(new_layout))
                

    def show_lock_popup(self, lock_name):
        if not self.config.keyboard_window_show_modifiers:
            return

        status_text = f"{lock_name} "
        if lock_name == "Caps":
            status_text += loc.tr(trans.on if self.keyboard_handler.is_caps_lock_on() else trans.off)
        elif lock_name == "Scroll":
            status_text += loc.tr(trans.on if self.keyboard_handler.is_scroll_lock_on() else trans.off)
        elif lock_name == "Num":
            status_text += loc.tr(trans.on if self.keyboard_handler.is_num_lock_on() else trans.off)
        elif lock_name == "Insert":
            status_text = loc.tr(trans.replace if self.keyboard_handler.is_insert_on() else trans.insert)
        
        self.keyboard_popup.show_popup(loc.tr(trans.lock), status_text)
    
    def show_volume_popup(self, device_changed):
        self.volume_popup.show_popup(device_changed)

    def show_media_popup(self):
        self.media_popup.show_popup()

    def show_settings_window(self):
        if self._settings_window.isVisible():
            return
        
        self._settings_window.show()
        self._settings_window.raise_()
        self._settings_window.activateWindow()

    def run(self):
        # Запускаем мониторинг медиа-сессий после старта цикла
        self.loop.call_soon(self.media_popup.start_monitoring)
        
        # Запускаем qasync loop вместо qt_app.exec()
        try:
            with self.loop:
                self.loop.run_forever()
        finally:
            self.shutdown()

    def shutdown(self):
        self.cleanup()
        self.loop.stop()
        self.qt_app.exit()

    def cleanup(self):
        self.keyboard_handler.stop()


if __name__ == "__main__":
    if is_already_running():
        show_already_running_message()
        sys.exit(1)

    app = App()

    try:
        app.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
    finally:
        app.cleanup()
        cleanup_mutex()
        print("exit")
        import os
        os._exit(0)
