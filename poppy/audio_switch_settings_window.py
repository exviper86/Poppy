# audio_switch_settings_window.py

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QCheckBox, QHBoxLayout,
    QLineEdit, QToolButton, QWidget, QComboBox, QGroupBox, QScrollArea, QFrame
)
from translations import localizer as loc, translations as trans

class HotkeyEdit(QLineEdit):
    """Поле для ввода горячей клавиши в формате, совместимом с библиотекой 'keyboard'."""
    hotkeyChanged = pyqtSignal(str)  # Сигнал: строка вида "ctrl+alt+a"

    def __init__(self, placeholder: str, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self._hotkey_str = ""  # строка в формате keyboard
        self._placeholder = placeholder
        self.setPlaceholderText(self._placeholder)
    
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()

        # Игнорируем Tab и неизвестные клавиши
        if key in (Qt.Key.Key_Tab, Qt.Key.Key_unknown):
            return

        # Игнорируем нажатие только модификаторов
        if key in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            return

        # Сброс по Esc
        if key == Qt.Key.Key_Escape:
            self.clear()
            return

        # Собираем части сочетания
        parts = []

        # Модификаторы (в порядке: ctrl, alt, shift, windows)
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            parts.append("ctrl")
        if modifiers & Qt.KeyboardModifier.AltModifier:
            parts.append("alt")
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            parts.append("shift")
        if modifiers & Qt.KeyboardModifier.MetaModifier:
            parts.append("windows")

        # Основная клавиша
        key_name = self._key_to_keyboard_name(key)
        if key_name:
            parts.append(key_name)

        # Формируем итоговую строку
        if parts:
            self._hotkey_str = "+".join(parts)
            self.setText(self._hotkey_str)
            self.hotkeyChanged.emit(self._hotkey_str)
        else:
            self.clear()

    def _key_to_keyboard_name(self, key: int) -> str:
        """Преобразует Qt.Key в имя клавиши для библиотеки 'keyboard'."""
        # Буквы A-Z
        if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
            return chr(ord('a') + (key - Qt.Key.Key_A))
    
        # Цифры 0-9 (верхний ряд)
        if Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            return chr(ord('0') + (key - Qt.Key.Key_0))
    
        # Специальные клавиши
        key_map = {
            Qt.Key.Key_Enter: "enter",
            Qt.Key.Key_Return: "enter",
            Qt.Key.Key_Escape: "esc",
            Qt.Key.Key_Backspace: "backspace",
            Qt.Key.Key_Tab: "tab",
            Qt.Key.Key_Space: "space",
            Qt.Key.Key_Delete: "delete",
            Qt.Key.Key_Home: "home",
            Qt.Key.Key_End: "end",
            Qt.Key.Key_Insert: "insert",
            Qt.Key.Key_PageUp: "page up",
            Qt.Key.Key_PageDown: "page down",
            Qt.Key.Key_Up: "up",
            Qt.Key.Key_Down: "down",
            Qt.Key.Key_Left: "left",
            Qt.Key.Key_Right: "right",
            Qt.Key.Key_CapsLock: "caps lock",
            Qt.Key.Key_NumLock: "num lock",
            Qt.Key.Key_ScrollLock: "scroll lock",
            Qt.Key.Key_Comma: "comma",
            Qt.Key.Key_Period: "period",
            Qt.Key.Key_Slash: "slash",
            Qt.Key.Key_Semicolon: "semicolon",
            Qt.Key.Key_Apostrophe: "quote",
            Qt.Key.Key_BracketLeft: "left bracket",
            Qt.Key.Key_BraceRight: "right bracket",
            Qt.Key.Key_Backslash: "backslash",
            Qt.Key.Key_Minus: "minus",
            Qt.Key.Key_Equal: "equal",
            Qt.Key.Key_QuoteLeft: "grave",
        }
    
        # F1-F24
        if Qt.Key.Key_F1 <= key <= Qt.Key.Key_F24:
            return f"f{key - Qt.Key.Key_F1 + 1}"
    
        return key_map.get(key, "")

    def clear(self):
        self._hotkey_str = ""
        self.setText("")
        self.setPlaceholderText(self._placeholder)
        self.hotkeyChanged.emit("")

    def hotkey(self) -> str:
        """Возвращает строку в формате 'keyboard' (например, 'ctrl+alt+a')."""
        return self._hotkey_str

    def setHotkey(self, hotkey: str):
        """Устанавливает горячую клавишу из строки формата 'keyboard'."""
        if not hotkey:
            self.clear()
            return
        self._hotkey_str = hotkey
        self.setText(hotkey)
        self.setPlaceholderText("")
        self.hotkeyChanged.emit(hotkey)

class AudioDeviceSelector(QGroupBox):
    deviceChanged = pyqtSignal(dict)
    
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)

        main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.layout = QVBoxLayout()
        
        main_layout.addWidget(self.scroll_area)
        

    def setDevices(self, output_devices, input_devices, settings):
        old_widget = self.scroll_area.widget()
        if old_widget:
            old_widget.deleteLater()
        
        scroll_content = QWidget()
        self.layout = QVBoxLayout(scroll_content)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(scroll_content)
        
        # Создаём словарь для быстрого поиска по device_id
        bindings_dict = {item["id"]: item for item in settings}
    
        input_device_names = [d["name"] for d in input_devices]
        input_device_ids = [d["id"] for d in input_devices]
    
        for device in output_devices:
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(6)
    
            check_box = QCheckBox(device["name"])
            combo_box = QComboBox()
            combo_box.addItem("не менять микрофон")
            combo_box.addItems(input_device_names)
    
            # Настройка состояния чекбокса
            binding = bindings_dict.get(device["id"])
            if binding is not None:
                check_box.setChecked(bool(binding.get("on", False)))
    
                # Настройка комбобокса: выбираем привязанный микрофон
                mic_id = binding.get("mic")
                if mic_id is not None:
                    try:
                        # Находим индекс микрофона по его ID
                        mic_index = input_device_ids.index(mic_id)
                        combo_box.setCurrentIndex(mic_index + 1)  # +1 из-за "не менять микрофон"
                    except ValueError:
                        # Микрофон не найден в списке — оставляем "не менять"
                        combo_box.setCurrentIndex(0)
                else:
                    combo_box.setCurrentIndex(0)
            else:
                check_box.setChecked(False)
                combo_box.setCurrentIndex(0)
    
            item_layout.addWidget(check_box)
            item_layout.addWidget(combo_box)
            self.layout.addLayout(item_layout)

            # noinspection PyDefaultArgument
            def on_change(value, checkbox=check_box, combobox=combo_box, device_id=device["id"], input_ids=input_device_ids):
                is_enabled = checkbox.isChecked()
                m_id = None
                if is_enabled:
                    idx = combobox.currentIndex()
                    if idx > 0:  # не "не менять микрофон"
                        m_id = input_ids[idx - 1]
                self.deviceChanged.emit({"id": device_id, "on": is_enabled, "mic": m_id})

            # Подключаем оба события
            check_box.toggled.connect(on_change)
            combo_box.currentIndexChanged.connect(on_change)
    
        self.layout.addStretch()

class AudioSwitchSettingsWindow(QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("Настройки переключения аудио устройств")
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setMinimumWidth(500)

        self._init_ui()

        self._update_text()
        loc.language_changed.connect(self._update_text)
    
    def showEvent(self, a0):
        super().showEvent(a0)
        self.hotkey_edit.clearFocus()
        self.double_click_cb.setEnabled(self.app.config.volume_window_enable)
        self.audio_selector.setDevices(
            self.app.audio_manager.get_all_output_devices(),
            self.app.audio_manager.get_all_input_devices(),
            self.app.config.audio_switch_devices
        )
    
    def _init_ui(self):
        layout = QVBoxLayout()

        self.double_click_cb = QCheckBox("По двойному клику на окне громкости")
        self.tray_cb = QCheckBox("В системном трее")
        self.tray_full_name_cb = QCheckBox("Полное имя устройства в системном трее")

        hotkey_layout = QHBoxLayout()

        self.hotkey_cb = QCheckBox("Cочетанием клавиш:")
        hotkey_layout.addWidget(self.hotkey_cb)

        self.hotkey_edit = HotkeyEdit("нажмите сочетание...")
        self.hotkey_edit.setFixedWidth(150)
        hotkey_layout.addWidget(self.hotkey_edit)

        self.clear_btn = QToolButton()
        self.clear_btn.setText("Сбросить")
        self.clear_btn.clicked.connect(self.hotkey_edit.clear)
        hotkey_layout.addWidget(self.clear_btn)
        hotkey_layout.addStretch()
        
        self.set_communication_cb = QCheckBox("Установливать и как устройство связи")
        self.select_audio_cb = QCheckBox("Только среди выбранных устройств")
        
        self.audio_selector = AudioDeviceSelector("Выбор устройств для переключения")
        self.audio_selector.setFixedHeight(200)
        
        layout.addWidget(self.double_click_cb)
        layout.addWidget(self.tray_cb)
        layout.addWidget(self.tray_full_name_cb)
        layout.addLayout(hotkey_layout)
        layout.addWidget(self.set_communication_cb)
        layout.addWidget(self.select_audio_cb)
        layout.addWidget(self.audio_selector)
        self.setLayout(layout)

        # Подключаем сигналы
        config = self.app.config
        
        self.double_click_cb.toggled.connect(config.save_audio_switch_double_tap)
        self.tray_cb.toggled.connect(config.save_audio_switch_tray)
        self.tray_cb.toggled.connect(self.tray_full_name_cb.setEnabled)
        self.tray_full_name_cb.toggled.connect(config.save_audio_switch_tray_full_name)
        self.hotkey_cb.toggled.connect(self._on_hotkey_cb_toggled)
        self.hotkey_edit.hotkeyChanged.connect(self._on_hotkey_edit_changed)
        self.set_communication_cb.toggled.connect(config.save_audio_switch_set_communication)
        self.select_audio_cb.toggled.connect(config.save_audio_switch_select)
        self.audio_selector.deviceChanged.connect(config.save_audio_switch_device)

        self._load_settings()

        self.select_audio_cb.toggled.connect(lambda checked: self.audio_selector.setEnabled(checked))
        
    def _load_settings(self):
        config = self.app.config
        
        self.double_click_cb.setChecked(config.audio_switch_double_tap)
        self.tray_cb.setChecked(config.audio_switch_tray)
        self.tray_full_name_cb.setChecked(config.audio_switch_tray_full_name)
        self.hotkey_cb.setChecked(config.audio_switch_hotkey)
        self.hotkey_edit.setHotkey(config.audio_switch_hotkey_value)
        self.set_communication_cb.setChecked(config.audio_switch_set_communication)
        self.select_audio_cb.setChecked(config.audio_switch_select)
        
        self._on_hotkey_cb_toggled(config.audio_switch_hotkey)
        self.audio_selector.setEnabled(config.audio_switch_select)

    def _on_hotkey_cb_toggled(self, enabled):
        self.app.config.save_audio_switch_hotkey(enabled)
        self.app.keyboard_handler.set_switch_device_hotkey(self.hotkey_edit.hotkey())
        self.hotkey_edit.setEnabled(enabled)
        self.clear_btn.setEnabled(enabled)
        
    def _on_hotkey_edit_changed(self, hotkey):
        self.app.config.save_audio_switch_hotkey_value(hotkey)
        self.app.keyboard_handler.set_switch_device_hotkey(hotkey)

    def _update_text(self):
        self.setWindowTitle(loc.tr(trans.audio_switch_title))

        self.double_click_cb.setText(loc.tr(trans.audio_switch_double_click))
        self.tray_cb.setText(loc.tr(trans.audio_switch_tray))
        self.tray_full_name_cb.setText(loc.tr(trans.audio_switch_tray_full_name))
        self.hotkey_cb.setText(loc.tr(trans.audio_switch_hotkey))
        self.hotkey_edit.setPlaceholderText(loc.tr(trans.audio_switch_hotkey_placeholder))
        self.clear_btn.setText(loc.tr(trans.audio_switch_clear_btn))
        self.set_communication_cb.setText(loc.tr(trans.audio_switch_set_communication))
        self.select_audio_cb.setText(loc.tr(trans.audio_switch_select_audio))
        self.audio_selector.setTitle(loc.tr(trans.audio_switch_devices_group))