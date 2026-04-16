import json
import winreg
from abc import abstractmethod
from PyQt6.QtCore import pyqtSignal, QObject


class BaseConfigOption(QObject):
    valueChanged = pyqtSignal(object)
    
    def __init__(self, key_name: str):
        super().__init__()
        self._key_name = key_name
        self._default_value = None
        self._current_value = None

    @property
    def default_value(self):
        return self._default_value

    @property
    def value(self):
        return self._current_value

    @abstractmethod
    def save(self, value):
        self._current_value = value
        self.valueChanged.emit(value)

    def _load_setting(self, key_name: str, default):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Poppy") as key:
                value, _ = winreg.QueryValueEx(key, key_name)
                return value
        except (OSError, WindowsError):
            return default

    def _save_setting(self, key_name: str, value, reg_type=winreg.REG_DWORD):
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Poppy") as key:
                winreg.SetValueEx(key, key_name, 0, reg_type, value)
        except (OSError, FileNotFoundError, WindowsError):
            pass

class ConfigOptionInt(BaseConfigOption):
    valueChanged = pyqtSignal(int)
    
    def __init__(self, key_name: str, default: int = 0):
        super().__init__(key_name)
        self._default_value = default
        self._current_value = self._load(self._key_name, default)

    @property
    def value(self) -> int:
        return super().value

    @property
    def default_value(self) -> int:
        return super()._default_value

    def save(self, value: int):
        super().save(value)
        self._save_setting(self._key_name, str(value),  winreg.REG_SZ)
        
    def _load(self, key: str, default: int) -> int:
        return int(self._load_setting(key, default))

class ConfigOptionStr(BaseConfigOption):
    valueChanged = pyqtSignal(str)
    
    def __init__(self, key_name: str, default: str = ""):
        super().__init__(key_name)
        self._default_value = default
        self._current_value = self._load_setting(self._key_name, default)

    @property
    def value(self) -> str:
        return super().value

    @property
    def default_value(self) -> str:
        return super().default_value

    def save(self, value: str):
        super().save(value)
        self._save_setting(self._key_name, value, winreg.REG_SZ)

class ConfigOptionBool(BaseConfigOption):
    valueChanged = pyqtSignal(bool)
    
    def __init__(self, key_name: str, default: bool = False):
        super().__init__(key_name)
        self._default_value = default
        self._current_value = bool(self._load_setting(self._key_name, 1 if default else 0))

    @property
    def value(self) -> bool:
        return super().value

    @property
    def default_value(self) -> bool:
        return super().default_value

    def save(self, value: bool):
        super().save(value)
        self._save_setting(self._key_name, 1 if value else 0)
        
class ConfigOptionAutostart(ConfigOptionBool):
    def __init__(self, key_name: str):
        super().__init__(key_name)
        self._current_value = self._load_autostart()

    def save(self, value: bool):
        self._current_value = value
        self.valueChanged.emit(value)
        self._save_autostart(value)

    def _load_autostart(self) -> bool:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            try:
                value, _ = winreg.QueryValueEx(key, self._key_name)
                winreg.CloseKey(key)
                registry_path = value.strip('"')
                current_path = __import__('sys').executable
                return registry_path.lower() == current_path.lower()
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception as e:
            print("[Config] Error loading autostart:", e)
            return False

    def _save_autostart(self, enabled: bool):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
            if enabled:
                current_path = __import__('sys').executable
                winreg.SetValueEx(key, self._key_name, 0, winreg.REG_SZ, f'"{current_path}"')
            else:
                try:
                    winreg.DeleteValue(key, self._key_name)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print("[Config] Error saving autostart:", e)
            return False
        
class ConfigOptionAudioDevices(BaseConfigOption):
    valueChanged = pyqtSignal(list)
    
    def __init__(self, key_name: str):
        super().__init__(key_name)
        value = self._load_setting(self._key_name, "")
        self._current_value = self._deserialize_audio_switch_devices(value) 

    @property
    def value(self) -> list:
        return super().value

    def save(self, value: list):
        super().save(value)
        self._save_setting(self._key_name, self._serialize_audio_switch_devices(value), winreg.REG_SZ)
    
    def save_device(self, value: dict):
        device_id = value["id"]
        is_enabled = value.get("on", False)

        # Если выключено — удаляем из списка (если есть)
        if not is_enabled:
            self._current_value = [dev for dev in self._current_value if dev["id"] != device_id]
        else:
            # Иначе — обновляем или добавляем
            for i, device in enumerate(self._current_value):
                if device["id"] == device_id:
                    self._current_value[i] = value  # полная замена
                    break
            else:
                self._current_value.append(value)

        self.save(self._current_value)
    
    def _serialize_audio_switch_devices(self, bindings: list) -> str:
        return json.dumps(bindings, ensure_ascii=False)

    def _deserialize_audio_switch_devices(self, bindings: str) -> list:
        if not bindings:
            return []
        try:
            return json.loads(bindings)
        except (json.JSONDecodeError, TypeError):
            return []