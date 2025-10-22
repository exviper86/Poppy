# tray_manager.py

# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from utils import get_resource_path, get_theme_colors, color_with_alpha, strip_audio_name
from translations import localizer as loc, translations as trans

class TrayManager:
    def __init__(self, app):
        self.app = app  # QApplication
        self.tray_icon = None
        
        self.create_tray_icon()
        
        self._update_text()
        loc.language_changed.connect(self._update_text)
    
    def create_tray_icon(self):
        icon_path = get_resource_path('icon.ico')
        tray_icon = QSystemTrayIcon(QIcon(icon_path), self.app)
        tray_icon.setToolTip("Poppy")

        # Создаём меню
        menu = QMenu()
        
        # Основной пункт: Настройки
        self.settings_action = menu.addAction("Настройки")
        self.settings_action.triggered.connect(self.app.show_settings_window)
        
        # Переключение устройства
        self.audio_menu = QMenu("Аудио устройство", menu)
        self.audio_menu_action = menu.addMenu(self.audio_menu)

        #menu.addSeparator()
        
        # Выход
        self.exit_action = menu.addAction("Выход")
        self.exit_action.triggered.connect(self.exit_app)

        # Применяем меню
        tray_icon.setContextMenu(menu)

        # Обработка кликов по иконке
        tray_icon.activated.connect(self.on_tray_activated)

        self.tray_icon = tray_icon
        self.tray_icon.show()
    
    def _update_audio_menu(self):
        # Сначала скроем/покажем само подменю в зависимости от настройки
        should_show = self.app.config.audio_switch_tray
        self.audio_menu_action.setVisible(should_show)
    
        if not should_show:
            return
    
        # Очищаем старые действия
        self.audio_menu.clear()
    
        # Получаем устройства и настройки
        devices = self.app.audio_manager.get_all_output_devices()
        switch_devices = self.app.config.audio_switch_devices

        switch_devices_enables = {dev["id"]: dev["on"] for dev in switch_devices}
    
        for device in devices:
            device_id = device["id"]
            
            if self.app.config.audio_switch_select and not switch_devices_enables.get(device_id, False):
                continue
    
            device_name = device["name"]
            if not self.app.config.audio_switch_tray_full_name:
                device_name = strip_audio_name(device_name)
            action = QAction(device_name, self.audio_menu)
            action.setCheckable(True)
            try:
                if self.app.audio_manager.get_device_name() == device["name"]:
                    action.setChecked(True)
            except Exception as e:
                print(f"Ошибка получения имени устройства: {e}")
    
            # Важно: захватываем device_id правильно
            action.triggered.connect(lambda checked, dev_id=device_id: self._on_audio_switch(dev_id))
    
            self.audio_menu.addAction(action)

        self.audio_menu_action.setVisible(len(self.audio_menu.actions()) > 0)

    def _on_audio_switch(self, device_id):
        try:
            self.app.audio_manager.switch_device(device_id)
        except Exception as e:
            print(f"Ошибка переключения устройства: {e}")
    
    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.app.show_settings_window()
            return 
        
        if reason != QSystemTrayIcon.ActivationReason.Context:
            return 
        
        self._update_audio_menu()
        
        colors = get_theme_colors()
        self.tray_icon.contextMenu().setStyleSheet(f"""
            QMenu {{
                border: 1px solid {colors['border']};
                background-color: {colors['bg']};
                border-radius: 4px;
            }}
            QMenu::item {{
                padding: 6px 20px 6px 20px;
                color: {colors['text']};
                border-radius: 4px;
                background-color: transparent;
            }}
            QMenu::item:selected {{
                border-radius: 4px;
                background-color: {color_with_alpha(colors['border'], 175)};
            }}
            QMenu::item:pressed {{
                border-radius: 4px;
                background-color: {color_with_alpha(colors['text'], 50)};
            }}
            QMenu::right-arrow {{
                right: 4px;
            }}
            QMenu::indicator {{
                left: 8px;
            }}
        """)

    def exit_app(self):
        self.tray_icon.hide()
        self.app.shutdown()

    def _update_text(self):
        self.settings_action.setText(loc.tr(trans.settings))
        self.audio_menu_action.setText(loc.tr(trans.audio_device))
        self.exit_action.setText(loc.tr(trans.exit))