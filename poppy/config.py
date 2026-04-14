from .config_options import (
    ConfigOptionBool as cBool,
    ConfigOptionInt as cInt,
    ConfigOptionStr as cStr,
    ConfigOptionAutostart as cAutoStart,
    ConfigOptionAudioDevices as cAudioDevices
)

class KeyboardWindowConfig:
    def __init__(self, name: str):
        self.enable: cBool = cBool(name + "Enable", True)
        self.show_language: cBool = cBool(name + "ShowLanguage", True)
        self.show_cursor: cBool = cBool(name + "ShowCursor", False)
        self.duration: cInt = cInt(name + "Duration", 2500)
        self.sound: cBool = cBool(name + "SoundEnabled", True)
        self.sound_type: cInt = cInt(name + "SoundType", 5)
        self.show_modifiers: cBool = cBool(name + "ShowModifiers", True)
        self.override_duration: cBool = cBool(name + "OverrideDuration", False)
        self.position: cStr = cStr(name + "Position", "center")

class VolumeWindowConfig:
    def __init__(self, name: str):
        self.enable: cBool = cBool(name + "Enable", True)
        self.show_media: cBool = cBool(name + "ShowMedia", False)
        self.step: cInt = cInt(name + "Step", 2)
        self.show_name: cBool = cBool(name + "ShowName", False)
        self.full_name: cBool = cBool(name + "FullName", False)
        self.override_duration: cBool = cBool(name + "OverrideDuration", False)
        self.duration: cInt = cInt(name + "Duration", 2500)
        self.position: cStr = cStr(name + "Position", "bottom")

class MediaWindowConfig:
    def __init__(self, name: str):
        self.enable: cBool = cBool(name + "Enable", True)
        self.show_volume: cBool = cBool(name + "ShowVolume", False)
        self.show_timeline: cBool = cBool(name + "ShowTimeline", True)
        self.color_by_cover: cBool = cBool(name + "ColorByCover", False)
        self.show_on_change: cBool = cBool(name + "ShowOnChange", True)
        self.override_duration = cBool(name + "OverrideDuration", False)
        self.duration: cInt = cInt(name + "Duration", 2500)
        self.position: cStr = cStr(name + "Position", "bottom")

class AudioSwitchConfig:
    def __init__(self, name: str):
        self.double_tap: cBool = cBool(name + "DoubleTap", False)
        self.tray: cBool = cBool(name + "Tray", False)
        self.tray_full_name: cBool = cBool(name + "TrayFullName", False)
        self.hotkey: cBool = cBool(name + "Hotkey", False)
        self.hotkey_value: cStr = cStr(name + "HotkeyValue", "alt+a")
        self.set_communication: cBool = cBool(name + "SetCommunication", False)
        self.select: cBool = cBool(name + "Select", False)
        self.devices: cAudioDevices = cAudioDevices(name + "Devices")

class LayoutSwitchConfig:
    def __init__(self, name: str):
        self.last: cBool = cBool(name + "Last", False)
        self.last_hotkey: cStr = cStr(name + "LastHotkey", "pause")
        self.no_last_switch: cBool = cBool(name + "NoLastSwitch", False)
        self.selected: cBool = cBool(name + "Selected", False)
        self.selected_hotkey: cStr = cStr(name + "SelectedHotkey", "shift+pause")
        self.case: cBool = cBool(name + "Case", False)
        self.case_hotkey: cStr = cStr(name + "CaseHotkey", "alt+pause")
        self.block_locks: cBool = cBool(name + "BlockLocks", False)

class CommonConfig:
    def __init__(self, name: str = ""):
        self.taskbar: cBool = cBool(name + "TaskbarOffset", True)
        self.popup_duration: cInt = cInt(name + "PopupDuration", 2500)
        self.popup_transparency: cInt = cInt(name + "PopupTransparency", 95)
        self.popup_show_duration: cInt = cInt(name + "PopupShowDuration", 80)
        self.animation: cBool = cBool(name + "Animation", True)
        self.language: cStr = cStr(name + "Language", "en")
        self.autostart: cAutoStart = cAutoStart(name + "Poppy")

class Config:
    def __init__(self):
        self.keyboard_window: KeyboardWindowConfig = KeyboardWindowConfig("KeyboardWindow")
        self.volume_window: VolumeWindowConfig = VolumeWindowConfig("VolumeWindow")
        self.media_window: MediaWindowConfig = MediaWindowConfig("MediaWindow")
        self.audio_switch: AudioSwitchConfig = AudioSwitchConfig("AudioSwitch")
        self.layout_switch: LayoutSwitchConfig = LayoutSwitchConfig("LayoutSwitch")
        self.common: CommonConfig = CommonConfig()
        
config: Config = Config()
        
