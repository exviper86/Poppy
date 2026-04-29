from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QLineEdit

class HotkeyEdit(QLineEdit):
    """Поле для ввода горячей клавиши в формате, совместимом с библиотекой 'keyboard'."""
    hotkeyChanged = pyqtSignal(str)  # Сигнал: строка вида "ctrl+alt+a"

    def __init__(self, placeholder: str, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self._hotkey_str = ""  # строка в формате keyboard
        self._placeholder = placeholder
        self.setPlaceholderText(self._placeholder)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        modifiers = event.modifiers()
        
        # Игнорируем неизвестные клавиши
        if key == Qt.Key.Key_unknown:
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
        key_name = self._key_to_keyboard_name(key, True if modifiers & Qt.KeyboardModifier.KeypadModifier else False)
        if key_name:
            parts.append(key_name)
        else:
            parts.clear()
            return 

        # Формируем итоговую строку
        if parts:
            self._hotkey_str = "+".join(parts)
            self.setText(self._hotkey_str)
            self.hotkeyChanged.emit(self._hotkey_str)
        else:
            self.clear()

    def _key_to_keyboard_name(self, key: int, num: bool) -> str:
        """Преобразует Qt.Key в имя клавиши для библиотеки 'keyboard'."""
        # Буквы A-Z
        if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
            return chr(ord('a') + (key - Qt.Key.Key_A))

        # Цифры 0-9 (верхний ряд)
        if Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
            return ("num " if num else "") + chr(ord('0') + (key - Qt.Key.Key_0))

        # F1-F24
        if Qt.Key.Key_F1 <= key <= Qt.Key.Key_F24:
            return f"f{key - Qt.Key.Key_F1 + 1}"

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
            Qt.Key.Key_Pause: "pause",
            Qt.Key.Key_Up: "up",
            Qt.Key.Key_Down: "down",
            Qt.Key.Key_Left: "left",
            Qt.Key.Key_Right: "right",
            Qt.Key.Key_CapsLock: "caps lock",
            Qt.Key.Key_NumLock: "num lock",
            Qt.Key.Key_ScrollLock: "scroll lock",
            Qt.Key.Key_Comma: "comma",
            Qt.Key.Key_Period: "period",
            Qt.Key.Key_Slash: "slash" if not num else "num divide",
            Qt.Key.Key_Semicolon: "semicolon",
            Qt.Key.Key_Apostrophe: "quote",
            Qt.Key.Key_BracketLeft: "left bracket",
            Qt.Key.Key_BraceRight: "right bracket",
            Qt.Key.Key_Backslash: "backslash",
            Qt.Key.Key_Plus: "num add",
            Qt.Key.Key_Minus: "minus" if not num else "num subtract",
            Qt.Key.Key_Asterisk: "num multiply",
            Qt.Key.Key_Equal: "equal",
            Qt.Key.Key_QuoteLeft: "backquote",
        }
        
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