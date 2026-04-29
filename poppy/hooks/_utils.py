from typing import Sequence

VK_NAMES = {
    # Стандартные
    0x03: "cancel",
    0x08: "backspace",
    0x09: "tab",
    0x0C: "clear",
    0x0D: "enter",
    0x13: "pause",
    0x14: "caps lock",
    0x15: "kana mode",          # или "hanguel mode"
    0x17: "junja mode",
    0x18: "final mode",
    0x19: "kanji mode",         # или "hanja mode"
    0x1B: "esc",
    0x1C: "convert",
    0x1D: "nonconvert",
    0x1E: "accept",
    0x1F: "mode change",
    0x20: "space",
    0x21: "page up",
    0x22: "page down",
    0x23: "end",
    0x24: "home",
    0x25: "left",
    0x26: "up",
    0x27: "right",
    0x28: "down",
    0x29: "select",
    0x2A: "print",
    0x2B: "execute",
    0x2C: "print screen",
    0x2D: "insert",
    0x2E: "delete",
    0x2F: "help",

    # Цифры 0-9 (верхний ряд) — остаются как есть
    **{0x30 + i: str(i) for i in range(10)},

    # Буквы a-z
    **{0x41 + i: chr(0x61 + i) for i in range(26)},  # 'a' to 'z'

    # win
    0x5B: "left win",
    0x5C: "right win",
    0x5D: "menu",
    
    # Numpad
    0x60: "numpad 0",
    0x61: "numpad 1",
    0x62: "numpad 2",
    0x63: "numpad 3",
    0x64: "numpad 4",
    0x65: "numpad 5",
    0x66: "numpad 6",
    0x67: "numpad 7",
    0x68: "numpad 8",
    0x69: "numpad 9",
    0x6A: "numpad multiply",
    0x6B: "numpad add",
    0x6C: "numpad separator",
    0x6D: "numpad subtract",
    0x6E: "numpad decimal",
    0x6F: "numpad divide",

    # F1–F24
    **{0x70 + i: f"f{i+1}" for i in range(24)},

    # Специальные
    0x90: "num lock",
    0x91: "scroll lock",
    0xA0: "left shift",
    0xA1: "right shift",
    0xA2: "left ctrl",
    0xA3: "right ctrl",
    0xA4: "left alt",
    0xA5: "right alt",
    0xA6: "browser back",
    0xA7: "browser forward",
    0xA8: "browser refresh",
    0xA9: "browser stop",
    0xAA: "browser search",
    0xAB: "browser favorites",
    0xAC: "browser home",
    0xAD: "volume mute",
    0xAE: "volume down",
    0xAF: "volume up",
    0xB0: "next track",
    0xB1: "previous track",
    0xB2: "stop",
    0xB3: "play pause",
    0xB4: "launch mail",
    0xB5: "launch media select",
    0xB6: "launch app 1",
    0xB7: "launch app 2",

    # OEM-клавиши (часто не используются в логике, но для полноты)
    0xBA: "semicolon",      # ; : 
    0xBB: "equal",          # = + 
    0xBC: "comma",          # , < 
    0xBD: "minus",          # - _ 
    0xBE: "period",         # . > 
    0xBF: "slash",          # / ? 
    0xC0: "backquote",      # ` ~ 
    0xDB: "left bracket",   # [ { 
    0xDC: "backslash",      # \ | 
    0xDD: "right bracket",  # ] } 
    0xDE: "quote",          # ' " 

    # Системные/редкие
    0xF6: "attn",
    0xF7: "crsel",
    0xF8: "exsel",
    0xF9: "ereof",
    0xFA: "play",
    0xFB: "zoom",
    0xFC: "no name",
    0xFD: "pa1",
    0xFE: "oem clear",
}
NAME_TO_VK = {name: vk for vk, name in VK_NAMES.items()}

MOUSE_NAMES = {
    0: "left",
    1: "right",
    2: "middle",
    3: "x1",
    4: "x2",
}

NAME_TO_MOUSE = {name: vk for vk, name in MOUSE_NAMES.items()}

def get_vk(name: str) -> int | None:
    if name in ('shift', 'ctrl', 'alt', 'win'):
        name = f"left {name}"
    if name.startswith("num "):
        name = name.replace("num", "numpad")
    return NAME_TO_VK.get(name.lower()) or None

def get_mouse(name: str) -> int | None:
    return NAME_TO_MOUSE.get(name.lower()) or None

def parse_hotkey_string(hotkey_str: str) -> Sequence[str]:
    parts = [part.strip().lower() for part in hotkey_str.split('+') if part.strip()]
    return parts
