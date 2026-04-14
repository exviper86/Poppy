# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

import ctypes
from ctypes import wintypes
import threading
from typing import Callable, Sequence, Union, Optional
from contextlib import contextmanager
from ._key import Key, KeyEvent, KeyEventType, HotkeyType, KeyStroke
from ._keys import keys
from ._utils import get_vk, parse_hotkey_string
from ._callbacks import Callbacks, ValuableCallbacks

# === Добавляем недостающие типы ===
if not hasattr(wintypes, 'LRESULT'):
    wintypes.LRESULT = ctypes.c_ssize_t
if not hasattr(wintypes, 'HHOOK'):
    wintypes.HHOOK = wintypes.HANDLE
if not hasattr(wintypes, 'LPMSG'):
    wintypes.LPMSG = ctypes.POINTER(wintypes.MSG)
if not hasattr(wintypes, 'HKL'):
    wintypes.HKL = wintypes.HANDLE

# === WinAPI ===
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# === Константы ===
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
INPUT_SIZE = 40 if ctypes.sizeof(ctypes.c_void_p) == 8 else 28

# === Структуры для SendInput ===
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("ki", KEYBDINPUT),
    ]

# === Типы ===
# noinspection PyUnresolvedReferences
HOOKPROC = ctypes.WINFUNCTYPE(wintypes.LRESULT, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)

user32.SetWindowsHookExW.argtypes = (wintypes.INT, HOOKPROC, wintypes.HINSTANCE, wintypes.DWORD)
user32.SetWindowsHookExW.restype = wintypes.HHOOK

user32.CallNextHookEx.argtypes = (wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
# noinspection PyUnresolvedReferences
user32.CallNextHookEx.restype = wintypes.LRESULT

user32.UnhookWindowsHookEx.argtypes = (wintypes.HHOOK,)
user32.UnhookWindowsHookEx.restype = wintypes.BOOL

user32.GetMessageW.argtypes = (wintypes.LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT)
user32.GetMessageW.restype = wintypes.BOOL

user32.TranslateMessage.argtypes = (wintypes.LPMSG,)
user32.DispatchMessageW.argtypes = (wintypes.LPMSG,)

user32.PostThreadMessageW.argtypes = (wintypes.DWORD, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
user32.PostThreadMessageW.restype = wintypes.BOOL

kernel32.GetLastError.argtypes = ()
kernel32.GetLastError.restype = wintypes.DWORD

user32.GetKeyState.argtypes = (wintypes.INT,)
user32.GetKeyState.restype = wintypes.SHORT

user32.VkKeyScanExW.argtypes = (wintypes.WORD, wintypes.HKL)
user32.VkKeyScanExW.restype = wintypes.SHORT

user32.ToUnicodeEx.argtypes = (
    wintypes.UINT,
    wintypes.UINT,
    ctypes.POINTER(wintypes.BYTE * 256),
    wintypes.LPWSTR,
    ctypes.c_int,
    wintypes.UINT,
    wintypes.HKL
)
user32.ToUnicodeEx.restype = ctypes.c_int


KeyEventCallback = Callable[[KeyEvent], Optional[bool]]
HotkeyCallback = Callable[[], None]
KeyParameter = Union[Key, str, int]
HotkeyParameter = Union[Sequence[KeyParameter], str]

class Keyboard:
    def __init__(self):
        self._thread: threading.Thread | None = None
        self._hook_proc: HOOKPROC | None = None
        self._hook_handle: wintypes.HHOOK | None = None
        
        self._pressed_keys: set[int] = set()
        
        self._any_key_callbacks = Callbacks[KeyEventCallback]()
        self._key_callbacks = ValuableCallbacks[int, KeyEventCallback]()
        self._hotkeys_on_press_callbacks = ValuableCallbacks[frozenset[int], HotkeyCallback]()
        self._hotkeys_on_press_once_callbacks = ValuableCallbacks[frozenset[int], HotkeyCallback]()
        self._hotkeys_on_release_callbacks = ValuableCallbacks[frozenset[int], HotkeyCallback]()
        self._active_once_hotkeys: set[frozenset[int]] = set()
        
    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self):
        if self.is_running:
            print("[!] Keyboard hook is already running")
            return
        
        self._thread = threading.Thread(target=self._message_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        if self.is_running:
            user32.PostThreadMessageW(wintypes.DWORD(self._thread.native_id), 0x0012, 0, 0)     # WM_QUIT
            self._thread.join(timeout=1)

            if self._thread.is_alive():
                print("[!] Keyboard thread did not terminate cleanly, forcing unhook")
                if self._hook_handle:
                    user32.UnhookWindowsHookEx(self._hook_handle)
                    self._hook_handle = None
                    self._hook_proc = None

        self._thread = None
        self._pressed_keys.clear()
    
    def hook(self, callback: KeyEventCallback) -> int:
        return self._any_key_callbacks.add(callback)
        
    def unhook(self, callback_id: int):
        self._any_key_callbacks.remove(callback_id)
            
    def unhook_global(self):
        self._any_key_callbacks.clear()
    
    def hook_key(self, key: KeyParameter, callback: KeyEventCallback) -> Optional[int]:
        vk = self._get_vk_form_key(key)
        if vk is None:
            return None
        
        return self._key_callbacks.add(vk, callback)

    def unhook_key(self, callback_id: int):
        self._key_callbacks.remove(callback_id)

    def unhook_key_global(self, key: KeyParameter):
        vk = self._get_vk_form_key(key)
        if vk is not None:
            self._key_callbacks.remove_by_value(vk)
    
    def unhook_all_keys(self):
        self._key_callbacks.clear()

    def hook_hotkey(self, hotkey: HotkeyParameter, callback: HotkeyCallback, hotkey_type: HotkeyType = HotkeyType.ON_PRESS_ONCE) -> Optional[int]:
        key_list = self._get_hotkey_list(hotkey)
        vks = (self._get_vk_form_key(k) for k in key_list)
        vk_set = frozenset(vk for vk in vks if vk is not None)
        if not vk_set:
            print(f"[!] Invalid keyboard hotkey: {hotkey}")
            return None
        
        if hotkey_type == HotkeyType.ON_PRESS:
            return self._hotkeys_on_press_callbacks.add(vk_set, callback)
        if hotkey_type == HotkeyType.ON_PRESS_ONCE:
            return self._hotkeys_on_press_once_callbacks.add(vk_set, callback)
        if hotkey_type == HotkeyType.ON_RELEASE:
            return self._hotkeys_on_release_callbacks.add(vk_set, callback)
        
        return None
    
    def unhook_hotkey(self, callback_id: int):
        callback = self._hotkeys_on_press_once_callbacks.remove(callback_id)
        if callback:
            self._active_once_hotkeys.discard(callback.value)
            return 
            
        if self._hotkeys_on_release_callbacks.remove(callback_id):
            return
        
        self._hotkeys_on_press_callbacks.remove(callback_id)
    
    def unhook_hotkey_global(self, hotkey: HotkeyParameter, hotkey_type: HotkeyType | None = None):
        key_list = self._get_hotkey_list(hotkey)
        vks = (self._get_vk_form_key(k) for k in key_list)
        vk_set = frozenset(vk for vk in vks if vk is not None)
        if not vk_set:
            print(f"[!] Invalid keyboard hotkey: {hotkey}")
            return
    
        if hotkey_type is None:
            self._hotkeys_on_press_callbacks.remove_by_value(vk_set)
            self._hotkeys_on_press_once_callbacks.remove_by_value(vk_set)
            self._hotkeys_on_release_callbacks.remove_by_value(vk_set)
            self._active_once_hotkeys.discard(vk_set)
        else:
            if hotkey_type == HotkeyType.ON_PRESS:
                self._hotkeys_on_press_callbacks.remove_by_value(vk_set)
            elif hotkey_type == HotkeyType.ON_PRESS_ONCE:
                self._hotkeys_on_press_once_callbacks.remove_by_value(vk_set)
                self._active_once_hotkeys.discard(vk_set)
            elif hotkey_type == HotkeyType.ON_RELEASE:
                self._hotkeys_on_release_callbacks.remove_by_value(vk_set)

    def unhook_all_hotkeys(self):
        self._hotkeys_on_press_callbacks.clear()
        self._hotkeys_on_press_once_callbacks.clear()
        self._hotkeys_on_release_callbacks.clear()
        self._active_once_hotkeys.clear()
    
    def unhook_all(self):
        self.unhook_global()
        self.unhook_all_keys()
        self.unhook_all_hotkeys()
    
    def press_key(self, key: KeyParameter):
        self.send_key(key, press=True)
    
    def release_key(self, key: KeyParameter):
        self.send_key(key, release=True)
        
    def click_key(self, key: KeyParameter):
        self.send_key(key, press=True, release=True)

    def send_key(self, key: KeyParameter, press: bool = False, release: bool = False):
        if not press and not release:
            return

        vk = self._get_vk_form_key(key)
        if vk is None:
            raise ValueError(f"Invalid keyboard key: {key}")

        if press:
            self._send_input(self._create_input(vk, key_down=True), "keyboard key press")
        if release:
            self._send_input(self._create_input(vk, key_down=False), "keyboard key release")

    def click_hotkey(self, hotkey: HotkeyParameter):
        key_list = self._get_hotkey_list(hotkey)
        vks = []
        for k in key_list:
            vk = self._get_vk_form_key(k)
            if vk is None:
                raise ValueError(f"Invalid keyboard key in hotkey: {k}")
            vks.append(vk)

        if not vks:
            return

        for vk in vks:
            self._send_input(self._create_input(vk, key_down=True), "keyboard hotkey press")
        for vk in reversed(vks):
            self._send_input(self._create_input(vk, key_down=False), "keyboard hotkey release")

    @contextmanager
    def hold(self, *hold_keys: KeyParameter):
        successfully_pressed = []
        try:
            for key in hold_keys:
                try:
                    self.send_key(key, press=True)
                    successfully_pressed.append(key)
                except Exception as e:
                    print(f"[!] Failed to press {key} in hold: {e}")
            yield
        finally:
            for key in reversed(successfully_pressed):
                try:
                    self.send_key(key, release=True)
                except Exception as e:
                    print(f"[!] Failed to release {key} in hold: {e}")

    def type(self, text: str):
        if not text:
            return
    
        for char in text:
            # Нажатие и отпускание Unicode-символа
            self._send_input(self._create_unicode_input(char, key_down=True), "keyboard type press")
            self._send_input(self._create_unicode_input(char, key_down=False), "keyboard type release")
        
    def is_key_pressed(self, key: KeyParameter) -> bool:
        return self._get_vk_form_key(key) in self._pressed_keys

    def is_win_pressed(self) -> bool:
        return keys.left_win.vk in self._pressed_keys or keys.right_win.vk in self._pressed_keys

    def is_shift_pressed(self) -> bool:
        return keys.left_shift.vk in self._pressed_keys or keys.right_shift.vk in self._pressed_keys

    def is_ctrl_pressed(self) -> bool:
        return keys.left_ctrl.vk in self._pressed_keys or keys.right_ctrl.vk in self._pressed_keys

    def is_alt_pressed(self) -> bool:
        return keys.left_alt.vk in self._pressed_keys or keys.right_alt.vk in self._pressed_keys
    
    def vk_to_char(
            self,
            vk: int,
            layout: int,
            shift: bool = False,
            ctrl: bool = False,
            alt: bool = False,
            caps_lock: bool = False,
            num_lock: bool = False,
            scroll_lock: bool = False,
    ) -> str | None:
        keyboard_state = (wintypes.BYTE * 256)()
        
        # Только модификаторы
        # for v in (0x10, 0x11, 0x12, 0x14, 0x90, 0x91):
        #     keyboard_state[v] = user32.GetKeyState(v) & 0xFF
        
        keyboard_state[0x10] = 0x80 if shift else 0x00      # VK_SHIFT
        keyboard_state[0x11] = 0x80 if ctrl else 0x00       # VK_CONTROL
        keyboard_state[0x12] = 0x80 if alt else 0x00        # VK_MENU (Alt)
        keyboard_state[0x14] = 0x01 if caps_lock else 0x00  # VK_CAPITAL
        keyboard_state[0x90] = 0x01 if num_lock else 0x00   # VK_NUMLOCK
        keyboard_state[0x91] = 0x01 if scroll_lock else 0x00  # VK_SCROLL

        #scan_code = user32.MapVirtualKeyW(vk, 0)
        
        buffer = ctypes.create_unicode_buffer(4)
        result = user32.ToUnicodeEx(vk, 0, keyboard_state, buffer, len(buffer), 0, layout)
    
        if result > 0:
            return buffer.value[:result]
        return None
    
    def keystroke_to_char(self, keystroke: KeyStroke, layout: int)-> str | None:
        if keystroke.vk is None:
            return None
        return self.vk_to_char(keystroke.vk, layout, shift=keystroke.shift, ctrl=keystroke.ctrl, alt=keystroke.alt)

    def char_to_keystroke(self, char: str, layout: int) -> Optional[KeyStroke]:
        if len(char) != 1:
            return None
    
        res = user32.VkKeyScanExW(ord(char), layout)
        if res == -1:
            return None
    
        vk = res & 0xFF
        modifiers = (res >> 8) & 0xFF
    
        return KeyStroke(
            vk=vk,
            shift=bool(modifiers & 0x02),
            ctrl=bool(modifiers & 0x04),
            alt=bool(modifiers & 0x08)
        )
    
    def click_keystroke(self, keystroke: KeyStroke):
        if keystroke.vk is None:
            return 
        
        if keystroke.ctrl:
            self.press_key(keys.left_ctrl)
        if keystroke.alt:
            self.press_key(keys.left_alt)
        if keystroke.shift:
            self.press_key(keys.left_shift)
    
        self.click_key(keystroke.vk)
    
        if keystroke.shift:
            self.release_key(keys.left_shift)
        if keystroke.alt:
            self.release_key(keys.left_alt)
        if keystroke.ctrl:
            self.release_key(keys.left_ctrl)
    
    def get_caps_lock(self) -> bool:
        return bool(user32.GetKeyState(0x14) & 0x01)

    def get_num_lock(self):
        return bool(user32.GetKeyState(0x90) & 0x01)

    def get_scroll_lock(self):
        return bool(user32.GetKeyState(0x91) & 0x01)

    def get_insert(self):
        return bool(user32.GetKeyState(0x2D) & 0x01)
        
    def _get_vk_form_key(self, key: KeyParameter) -> Optional[int]:
        if isinstance(key, Key):
            return key.vk
        elif isinstance(key, str):
            return get_vk(key)
        else:
            return int(key)
    
    def _get_hotkey_list(self, hotkey: HotkeyParameter) -> Sequence[KeyParameter]:
        if isinstance(hotkey, str):
            return parse_hotkey_string(hotkey)
        
        return hotkey
    
    def _create_input(self, vk: int, key_down: bool) -> INPUT:
        flags = 0 if key_down else KEYEVENTF_KEYUP
        # scan = 0 — используем VK
        return INPUT(
            type=INPUT_KEYBOARD,
            ki=KEYBDINPUT(
                wVk=wintypes.WORD(vk),
                wScan=0,
                dwFlags=flags,
                time=0,
                dwExtraInfo=None
            )
        )

    def _create_unicode_input(self, char: str, key_down: bool = True) -> INPUT:
        if len(char) != 1:
            raise ValueError("char must be a single character")
    
        # Преобразуем в UTF-16 (Windows использует UTF-16)
        utf16_code = ord(char)
    
        flags = KEYEVENTF_UNICODE
        if not key_down:
            flags |= KEYEVENTF_KEYUP
    
        return INPUT(
            type=INPUT_KEYBOARD,
            ki=KEYBDINPUT(
                wVk=0,  # Для Unicode — 0
                wScan=wintypes.WORD(utf16_code),
                dwFlags=flags,
                time=0,
                dwExtraInfo=None
            )
        )
    
    def _send_input(self, press_input: INPUT, text: str):
        result = user32.SendInput(1, ctypes.byref(press_input), INPUT_SIZE)
        if result == 0:
            raise RuntimeError(f"SendInput {text} failed")
    
    def _on_press(self, key: Key) -> bool:
        #print(f"{key} pressed")
        
        self._pressed_keys.add(key.vk)
        
        suppress = False

        for callback in self._any_key_callbacks.get_all():
            if self._process_callback(KeyEventType.PRESS, key, callback):
                suppress = True
            
        for callback in self._key_callbacks.get_by_value(key.vk):
            if self._process_callback(KeyEventType.PRESS, key, callback):
                suppress = True

        pressed_frozen = frozenset(self._pressed_keys)

        # ON_PRESS — срабатывает каждый раз
        for callback in self._hotkeys_on_press_callbacks.get_by_value(pressed_frozen):
            try:
                callback()
            except Exception as e:
                print(f"[Keyboard hotkey ON_PRESS] Error: {e}")
    
        # ON_PRESS_ONCE — только если ещё не сработало
        if pressed_frozen not in self._active_once_hotkeys:
            self._active_once_hotkeys.add(pressed_frozen)
            for callback in self._hotkeys_on_press_once_callbacks.get_by_value(pressed_frozen):
                try:
                    callback()
                except Exception as e:
                    print(f"[keyboard hotkey ON_PRESS_ONCE] Error: {e}")
        
        return suppress
    
    def _on_release(self, key: Key) -> bool:
        #print(f"{key} released")

        pressed_frozen = frozenset(self._pressed_keys)
        
        released_vk = key.vk
        self._pressed_keys.discard(key.vk)

        suppress = False

        for callback in self._any_key_callbacks.get_all():
            if self._process_callback(KeyEventType.RELEASE, key, callback):
                suppress = True

        for callback in self._key_callbacks.get_by_value(key.vk):
            if self._process_callback(KeyEventType.RELEASE, key, callback):
                suppress = True

        # ON_RELEASE: срабатывает при отпускании
        for callback in self._hotkeys_on_release_callbacks.get_by_value(pressed_frozen):
            try:
                callback()
            except Exception as e:
                print(f"[Keyboard hotkey ON_RELEASE] Error: {e}")

        to_remove = set()
        for hk in self._active_once_hotkeys:
            if released_vk in hk:
                to_remove.add(hk)
        self._active_once_hotkeys -= to_remove
        
        return suppress
    
    def _process_callback(self, event_type: KeyEventType, key: Key, callback: KeyEventCallback) -> bool:
        event = KeyEvent(event_type, key)
        try:
            return callback(event) is False
        except Exception as e:
            print(f"Callback error for keyboard event={event}: {e}")
            return False
    
    def _message_loop(self):
        def low_level_keyboard_proc(nCode, wParam, lParam):
            try:
                suppress = False
                if nCode >= 0:
                    vk = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_ulong)).contents.value
                    key = Key(vk)
                    if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
                        suppress = self._on_press(key) and wParam != WM_SYSKEYDOWN
                    elif wParam in (WM_KEYUP, WM_SYSKEYUP):
                        suppress = self._on_release(key) and wParam != WM_SYSKEYUP
                return 1 if suppress else user32.CallNextHookEx(0, nCode, wParam, lParam)
            except Exception as e:
                print(f"keyboard hook error: {e}")
                return user32.CallNextHookEx(0, nCode, wParam, lParam)
    
        self._hook_proc = HOOKPROC(low_level_keyboard_proc)
        self._hook_handle = user32.SetWindowsHookExW(WH_KEYBOARD_LL, self._hook_proc, 0, 0)
        if not self._hook_handle:
            print("Failed to install keyboard hook")
            return
    
        print("[+] Keyboard hook installed")

        msg = wintypes.MSG()
        while True:
            ret = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if ret == 0:        # WM_QUIT
                break
            elif ret == -1:
                error_code = kernel32.GetLastError()
                print(f"[!] GetMessageW failed with error {error_code}")
                break
            else:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
    
        user32.UnhookWindowsHookEx(self._hook_handle)
        self._hook_handle = None
        self._hook_proc = None
        print("[-] Keyboard hook removed")
             
keyboard: Keyboard = Keyboard()