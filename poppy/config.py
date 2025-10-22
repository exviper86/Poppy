# config.py

import json
import winreg

class Config:
    def __init__(self):
        self.keyboard_window_enable = self._load_keyboard_window_enable()
        self.keyboard_window_show_language = self._load_keyboard_window_show_language()
        self.keyboard_window_show_cursor = self._load_keyboard_window_show_cursor() 
        self.keyboard_window_show_modifiers = self._load_keyboard_window_show_modifiers()
        self.keyboard_window_position = self._load_keyboard_window_position()
        self.volume_window_enable = self._load_volume_window_enable()
        self.volume_window_position = self._load_volume_window_position()
        self.volume_window_show_media = self._load_volume_window_show_media()
        self.volume_window_step = self._load_volume_window_step()
        self.volume_window_show_name = self._load_volume_window_show_name()
        self.volume_window_full_name = self._load_volume_window_full_name()
        self.media_window_enable = self._load_media_window_enable()
        self.media_window_position = self._load_media_window_position()
        self.media_window_show_volume = self._load_media_window_show_volume()
        self.media_window_show_timeline = self._load_media_window_show_timeline()
        self.media_window_color_by_cover = self._load_media_window_color_by_cover()
        self.media_window_show_on_change = self._load_media_window_show_on_change()
        self.audio_switch_double_tap = self._load_audio_switch_double_tap()
        self.audio_switch_tray = self._load_audio_switch_tray()
        self.audio_switch_tray_full_name = self._load_audio_switch_tray_full_name()
        self.audio_switch_hotkey = self._load_audio_switch_hotkey()
        self.audio_switch_hotkey_value = self._load_audio_switch_hotkey_value()
        self.audio_switch_set_communication = self._load_audio_switch_set_communication()
        self.audio_switch_select = self._load_audio_switch_select()
        self.audio_switch_devices = self._load_audio_switch_devices()
        self.sound = self._load_sound()
        self.sound_type = self._load_sound_type()
        self.taskbar = self._load_taskbar()
        self.popup_duration = self._load_popup_duration()
        self.popup_transparency = self._load_popup_transparency()
        self.popup_show_duration = self._load_popup_show_duration()
        self.animation = self._load_animation()
        self.language = self._load_language()
        self.autostart = self._load_autostart()

    def _load_setting(self, key_name, default):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Poppy")
            value, _ = winreg.QueryValueEx(key, key_name)
            winreg.CloseKey(key)
            return value
        except:
            return default
    
    def _save_setting(self, key_name, value, reg_type=winreg.REG_DWORD):
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Poppy")
            winreg.SetValueEx(key, key_name, 0, reg_type, value)
            winreg.CloseKey(key)
        except:
            pass
    
    def _load_keyboard_window_enable(self):
        return self._load_setting("KeyboardWindowEnable", 1)
    
    def save_keyboard_window_enable(self, enabled):
        self.keyboard_window_enable = enabled
        self._save_setting("KeyboardWindowEnable", 1 if enabled else 0)

    def _load_keyboard_window_show_language(self):
        return self._load_setting("KeyboardWindowShowLanguage", 1)

    def save_keyboard_window_show_language(self, enabled):
        self.keyboard_window_show_language = enabled
        self._save_setting("KeyboardWindowShowLanguage", 1 if enabled else 0)

    def _load_keyboard_window_show_cursor(self):
        return self._load_setting("KeyboardWindowShowCursor", 0)

    def save_keyboard_window_show_cursor(self, enabled):
        self.keyboard_window_show_cursor = enabled
        self._save_setting("KeyboardWindowShowCursor", 1 if enabled else 0)

    def _load_keyboard_window_show_modifiers(self):
        return self._load_setting("KeyboardWindowShowModifiers", 1)

    def save_keyboard_window_show_modifiers(self, enabled):
        self.keyboard_window_show_modifiers = enabled
        self._save_setting("KeyboardWindowShowModifiers", 1 if enabled else 0)
    
    def _load_keyboard_window_position(self):
        return self._load_setting("KeyboardWindowPosition", "center")
    
    def save_keyboard_window_position(self, position):
        self.keyboard_window_position = position
        self._save_setting("KeyboardWindowPosition", position, winreg.REG_SZ)
    
    def _load_volume_window_enable(self):
        return self._load_setting("VolumeWindowEnable", 1)
    
    def save_volume_window_enable(self, enabled):
        self.volume_window_enable = enabled
        self._save_setting("VolumeWindowEnable", 1 if enabled else 0)
    
    def _load_volume_window_position(self):
        return self._load_setting("VolumeWindowPosition", "bottom")
    
    def save_volume_window_position(self, position):
        self.volume_window_position = position
        self._save_setting("VolumeWindowPosition", position, winreg.REG_SZ)
    
    def _load_volume_window_show_media(self):
        return self._load_setting("VolumeWindowShowMedia", 0)
    
    def save_volume_window_show_media(self, enabled):
        self.volume_window_show_media = enabled
        self._save_setting("VolumeWindowShowMedia", 1 if enabled else 0)

    def _load_volume_window_step(self):
        value = self._load_setting("VolumeWindowStep", 2)
        return value

    def save_volume_window_step(self, step):
        self.volume_window_step = step
        self._save_setting("VolumeWindowStep", step)

    def _load_volume_window_show_name(self):
        return self._load_setting("VolumeWindowShowName", 0)

    def save_volume_window_show_name(self, enabled):
        self.volume_window_show_name = enabled
        self._save_setting("VolumeWindowShowName", 1 if enabled else 0)

    def _load_volume_window_full_name(self):
        return self._load_setting("VolumeWindowFullName", 0)

    def save_volume_window_full_name(self, enabled):
        self.volume_window_full_name = enabled
        self._save_setting("VolumeWindowFullName", 1 if enabled else 0)
    
    def _load_media_window_enable(self):
        return self._load_setting("MediaWindowEnable", 1)
    
    def save_media_window_enable(self, enabled):
        self.media_window_enable = enabled
        self._save_setting("MediaWindowEnable", 1 if enabled else 0)
    
    def _load_media_window_position(self):
        return self._load_setting("MediaWindowPosition", "right-bottom")
    
    def save_media_window_position(self, position):
        self.media_window_position = position
        self._save_setting("MediaWindowPosition", position, winreg.REG_SZ)

    def _load_media_window_show_volume(self):
        return self._load_setting("MediaWindowShowVolume", 0)

    def save_media_window_show_volume(self, enabled):
        self.media_window_show_volume = enabled
        self._save_setting("MediaWindowShowVolume", 1 if enabled else 0)

    def _load_media_window_show_timeline(self):
        return bool(self._load_setting("MediaWindowShowTimeline", 1))

    def save_media_window_show_timeline(self, enabled):
        self.media_window_show_timeline = enabled
        self._save_setting("MediaWindowShowTimeline", 1 if enabled else 0)
            
    def _load_media_window_color_by_cover(self):
        return bool(self._load_setting("MediaWindowColorByCover", 0))
    
    def save_media_window_color_by_cover(self, enabled):
        self.media_window_color_by_cover = enabled
        self._save_setting("MediaWindowColorByCover", 1 if enabled else 0)
    
    def _load_media_window_show_on_change(self):
        return bool(self._load_setting("MediaWindowShowOnChange", 1))
    
    def save_media_window_show_on_change(self, enabled):
        self.media_window_show_on_change = enabled
        self._save_setting("MediaWindowShowOnChange", 1 if enabled else 0)
    
    def _load_audio_switch_double_tap(self):
        return bool(self._load_setting("AudioSwitchDoubleTap", 0))
    
    def save_audio_switch_double_tap(self, enabled):
        self.audio_switch_double_tap = enabled
        self._save_setting("AudioSwitchDoubleTap", 1 if enabled else 0)
    
    def _load_audio_switch_tray(self):
        return bool(self._load_setting("AudioSwitchTray", 0))
    
    def save_audio_switch_tray(self, enabled):
        self.audio_switch_tray = enabled
        self._save_setting("AudioSwitchTray", 1 if enabled else 0)
    
    def _load_audio_switch_tray_full_name(self):
        return bool(self._load_setting("AudioSwitchTrayFullName", 0))
    
    def save_audio_switch_tray_full_name(self, enabled):
        self.audio_switch_tray_full_name = enabled
        self._save_setting("AudioSwitchTrayFullName", 1 if enabled else 0)
    
    def _load_audio_switch_hotkey(self):
        return bool(self._load_setting("AudioSwitchHotkey", 0))
    
    def save_audio_switch_hotkey(self, enabled):
        self.audio_switch_hotkey = enabled
        self._save_setting("AudioSwitchHotkey", 1 if enabled else 0)
    
    def _load_audio_switch_hotkey_value(self):
        return self._load_setting("AudioSwitchHotkeyValue", "alt+a")
    
    def save_audio_switch_hotkey_value(self, value):
        self.audio_switch_hotkey_value = value
        self._save_setting("AudioSwitchHotkeyValue", value, winreg.REG_SZ)
    
    def _load_audio_switch_set_communication(self):
        return bool(self._load_setting("AudioSwitchSetCommunication", 0))
    
    def save_audio_switch_set_communication(self, enabled):
        self.audio_switch_set_communication = enabled
        self._save_setting("AudioSwitchSetCommunication", 1 if enabled else 0)
    
    def _load_audio_switch_select(self):
        return bool(self._load_setting("AudioSwitchSelect", 0))
    
    def save_audio_switch_select(self, enabled):
        self.audio_switch_select = enabled
        self._save_setting("AudioSwitchSelect", 1 if enabled else 0)
    
    def _load_audio_switch_devices(self):
        value = self._load_setting("AudioSwitchDevices", "")
        return self._deserialize_audio_switch_devices(value)
    
    def save_audio_switch_device(self, value):
        device_id = value["id"]
        is_enabled = value.get("on", False)
    
        # Если выключено — удаляем из списка (если есть)
        if not is_enabled:
            self.audio_switch_devices = [dev for dev in self.audio_switch_devices if dev["id"] != device_id]
        else:
            # Иначе — обновляем или добавляем
            for i, device in enumerate(self.audio_switch_devices):
                if device["id"] == device_id:
                    self.audio_switch_devices[i] = value  # полная замена
                    break
            else:
                self.audio_switch_devices.append(value)
        
        self._save_setting("AudioSwitchDevices", self._serialize_audio_switch_devices(self.audio_switch_devices), winreg.REG_SZ)
    
    def _load_sound(self):
        return bool(self._load_setting("SoundEnabled", 1))
    
    def save_sound(self, enabled):
        self.sound = enabled
        self._save_setting("SoundEnabled", 1 if enabled else 0)
    
    def _load_sound_type(self):
        return self._load_setting("SoundType", 5)
    
    def save_sound_type(self, sound_type):
        self.sound_type = sound_type
        self._save_setting("SoundType", sound_type)
    
    def _load_taskbar(self):
        return bool(self._load_setting("TaskbarOffset", 1))
    
    def save_taskbar(self, enabled):
        self.taskbar = enabled
        self._save_setting("TaskbarOffset", 1 if enabled else 0)
    
    def _load_popup_duration(self):
        value = self._load_setting("PopupDuration", 2500)
        return value
    
    def save_popup_duration(self, duration):
        self.popup_duration = duration
        self._save_setting("PopupDuration", duration)

    def _load_popup_transparency(self):
        return self._load_setting("PopupTransparency", 95)

    def save_popup_transparency(self, transparency):
        self.popup_transparency = transparency
        self._save_setting("PopupTransparency", transparency)

    def _load_popup_show_duration(self):
        return self._load_setting("PopupShowDuration", 80)

    def save_popup_show_duration(self, duration):
        self.popup_show_duration = duration
        self._save_setting("PopupShowDuration", duration)

    def _load_animation(self):
        return bool(self._load_setting("Animation", 1))

    def save_animation(self, enabled):
        self.animation = enabled
        self._save_setting("Animation", 1 if enabled else 0)
    
    def _load_language(self):
        return self._load_setting("Language", "")
    
    def save_language(self, language):
        self.language = language
        self._save_setting("Language", language, winreg.REG_SZ)
    
    def _load_autostart(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            try:
                value, _ = winreg.QueryValueEx(key, "Poppy")
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except:
            return False
    
    def save_autostart(self, enabled):
        try:
            self.autostart = enabled
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
            if enabled:
                exe_path = __import__('sys').executable
                winreg.SetValueEx(key, "Poppy", 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(key, "Poppy")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    def _serialize_audio_switch_devices(self, bindings: list) -> str:
        return json.dumps(bindings, ensure_ascii=False)

    def _deserialize_audio_switch_devices(self, bindings: str) -> list:
        if not bindings:
            return []
        try:
            return json.loads(bindings)
        except (json.JSONDecodeError, TypeError):
            return []