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
from ._mouse_button import MouseButton, MouseEvent, MouseEventType
from ._mouse_buttons import mouseButtons
from ._key import HotkeyType
from ._utils import get_mouse, parse_hotkey_string
from ._callbacks import Callbacks, ValuableCallbacks

# === Добавляем недостающие типы ===
if not hasattr(wintypes, 'LRESULT'):
    wintypes.LRESULT = ctypes.c_ssize_t
if not hasattr(wintypes, 'HHOOK'):
    wintypes.HHOOK = wintypes.HANDLE
if not hasattr(wintypes, 'LPMSG'):
    wintypes.LPMSG = ctypes.POINTER(wintypes.MSG)

# === WinAPI ===
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# === Константы ===
WH_MOUSE_LL = 14
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_MOUSEWHEEL = 0x020A
WM_XBUTTONDOWN = 0x020B
WM_XBUTTONUP = 0x020C
WM_MOUSEMOVE = 0x0200
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x1000
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100
MOUSEEVENTF_ABSOLUTE = 0x8000
FLAGS_DOWN = {
    0: MOUSEEVENTF_LEFTDOWN,
    1: MOUSEEVENTF_RIGHTDOWN,
    2: MOUSEEVENTF_MIDDLEDOWN,
    3: MOUSEEVENTF_XDOWN,
    4: MOUSEEVENTF_XDOWN,
}
FLAGS_UP = {
    0: MOUSEEVENTF_LEFTUP,
    1: MOUSEEVENTF_RIGHTUP,
    2: MOUSEEVENTF_MIDDLEUP,
    3: MOUSEEVENTF_XUP,
    4: MOUSEEVENTF_XUP,
}
INPUT_SIZE = 40 if ctypes.sizeof(ctypes.c_void_p) == 8 else 28

# === Структуры для SendInput ===
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("mi", MOUSEINPUT),
    ]

# === Структура для хука ===
class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt", POINT),
        ("mouseData", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
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

user32.GetCursorPos.argtypes = (ctypes.POINTER(POINT),)
user32.GetCursorPos.restype = wintypes.BOOL


MouseEventCallback = Callable[[MouseEvent], Optional[bool]]
HotkeyCallback = Callable[[], None]
MouseButtonParameter = Union[MouseButton, str, int]
MouseHotkeyParameter = Union[Sequence[MouseButtonParameter], str]

class Mouse:
    def __init__(self):
        self._thread: threading.Thread | None = None
        self._hook_proc: HOOKPROC | None = None
        self._hook_handle: wintypes.HHOOK | None = None

        self._pressed_buttons: set[int] = set()

        self._any_button_callbacks = Callbacks[MouseEventCallback]()
        self._button_callbacks = ValuableCallbacks[int, MouseEventCallback]()

        self._move_callbacks = Callbacks[MouseEventCallback]()
        self._scroll_callbacks = Callbacks[MouseEventCallback]()

        self._hotkeys_on_press_callbacks = ValuableCallbacks[frozenset[int], HotkeyCallback]()
        self._hotkeys_on_press_once_callbacks = ValuableCallbacks[frozenset[int], HotkeyCallback]()
        self._hotkeys_on_release_callbacks = ValuableCallbacks[frozenset[int], HotkeyCallback]()
        self._active_once_hotkeys: set[frozenset[int]] = set()

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self):
        if self.is_running:
            print("[!] Mouse hook is already running")
            return
        
        self._thread = threading.Thread(target=self._message_loop, daemon=True)
        self._thread.start()

    def stop(self):
        if self.is_running:
            user32.PostThreadMessageW(wintypes.DWORD(self._thread.native_id), 0x0012, 0, 0)     # WM_QUIT
            self._thread.join(timeout=1)

            if self._thread.is_alive():
                print("[!] Mouse thread did not terminate cleanly, forcing unhook")
                if self._hook_handle:
                    user32.UnhookWindowsHookEx(self._hook_handle)
                    self._hook_handle = None
                    self._hook_proc = None

        self._thread = None
        self._pressed_buttons.clear()
    
    def hook(self, callback: MouseEventCallback) -> int:
        return self._any_button_callbacks.add(callback)

    def unhook(self, callback_id: int):
        self._any_button_callbacks.remove(callback_id)

    def unhook_global(self):
        self._any_button_callbacks.clear()

    def hook_button(self, button: MouseButtonParameter, callback: MouseEventCallback) -> Optional[int]:
        code = self._get_code_form_button(button)
        if code is None:
            return None

        return self._button_callbacks.add(code, callback)

    def unhook_button(self, callback_id: int):
        self._button_callbacks.remove(callback_id)

    def unhook_button_global(self, button: MouseButtonParameter):
        code = self._get_code_form_button(button)
        if code is not None:
            self._button_callbacks.remove_by_value(code)

    def unhook_all_buttons(self):
        self._button_callbacks.clear()

    def hook_hotkey(self, hotkey: MouseHotkeyParameter, callback: HotkeyCallback, hotkey_type: HotkeyType = HotkeyType.ON_PRESS_ONCE) -> Optional[int]:
        key_list = self._get_hotkey_list(hotkey)
        codes = (self._get_code_form_button(k) for k in key_list)
        code_set = frozenset(code for code in codes if code is not None)
        if not code_set:
            print(f"[!] Invalid mouse hotkey: {hotkey}")
            return None

        if hotkey_type == HotkeyType.ON_PRESS:
            return self._hotkeys_on_press_callbacks.add(code_set, callback)
        if hotkey_type == HotkeyType.ON_PRESS_ONCE:
            return self._hotkeys_on_press_once_callbacks.add(code_set, callback)
        if hotkey_type == HotkeyType.ON_RELEASE:
            return self._hotkeys_on_release_callbacks.add(code_set, callback)

        return None

    def unhook_hotkey(self, callback_id: int):
        callback = self._hotkeys_on_press_once_callbacks.remove(callback_id)
        if callback:
            self._active_once_hotkeys.discard(callback.value)
            return

        if self._hotkeys_on_release_callbacks.remove(callback_id):
            return

        self._hotkeys_on_press_callbacks.remove(callback_id)

    def unhook_hotkey_global(self, hotkey: MouseHotkeyParameter, hotkey_type: HotkeyType | None = None):
        key_list = self._get_hotkey_list(hotkey)
        codes = (self._get_code_form_button(k) for k in key_list)
        code_set = frozenset(code for code in codes if code is not None)
        if not code_set:
            print(f"[!] Invalid mouse hotkey: {hotkey}")
            return

        if hotkey_type is None:
            self._hotkeys_on_press_callbacks.remove_by_value(code_set)
            self._hotkeys_on_press_once_callbacks.remove_by_value(code_set)
            self._hotkeys_on_release_callbacks.remove_by_value(code_set)
            self._active_once_hotkeys.discard(code_set)
        else:
            if hotkey_type == HotkeyType.ON_PRESS:
                self._hotkeys_on_press_callbacks.remove_by_value(code_set)
            elif hotkey_type == HotkeyType.ON_PRESS_ONCE:
                self._hotkeys_on_press_once_callbacks.remove_by_value(code_set)
                self._active_once_hotkeys.discard(code_set)
            elif hotkey_type == HotkeyType.ON_RELEASE:
                self._hotkeys_on_release_callbacks.remove_by_value(code_set)

    def unhook_all_hotkeys(self):
        self._hotkeys_on_press_callbacks.clear()
        self._hotkeys_on_press_once_callbacks.clear()
        self._hotkeys_on_release_callbacks.clear()
        self._active_once_hotkeys.clear()

    def hook_move(self, callback: MouseEventCallback) -> int:
        return self._move_callbacks.add(callback)

    def unhook_move(self, callback_id: int):
        self._move_callbacks.remove(callback_id)

    def unhook_move_global(self):
        self._move_callbacks.clear()

    def hook_scroll(self, callback: MouseEventCallback) -> int:
        return self._scroll_callbacks.add(callback)

    def unhook_scroll(self, callback_id: int):
        self._scroll_callbacks.remove(callback_id)

    def unhook_scroll_global(self):
        self._scroll_callbacks.clear()

    def unhook_all(self):
        self.unhook_global()
        self.unhook_all_buttons()
        self.unhook_all_hotkeys()
        self.unhook_move_global()
        self.unhook_scroll_global()

    def press(self, button: MouseButtonParameter):
        self.send_button(button, press=True)

    def release(self, button: MouseButtonParameter):
        self.send_button(button, release=True)

    def click(self, button: MouseButtonParameter):
        self.press(button)
        self.release(button)

    def send_button(self, button: MouseButtonParameter, press: bool = False, release: bool = False):
        if not press and not release:
            return

        code = self._get_code_form_button(button)
        if code is None:
            raise ValueError(f"Invalid mouse button: {button}")

        mouse_data = 1 if code == 3 else (2 if code == 4 else 0)

        if press:
            self._send_input(self._create_input(code, flags=FLAGS_DOWN.get(code), mouse_data=mouse_data), "mouse button press")
        if release:
            self._send_input(self._create_input(code, flags=FLAGS_UP.get(code), mouse_data=mouse_data), "mouse button release")

    def move(self, x: int, y: int):
        self._send_input(self._create_input(x=x, y=y, flags=MOUSEEVENTF_MOVE | 0), "mouse move")
    
    def scroll(self, delta: int = 1, horizontal: bool = False):
        # Прокрутка колеса. delta > 0 — вверх/вправо
        flags = MOUSEEVENTF_HWHEEL if horizontal else MOUSEEVENTF_WHEEL
        # delta * 120 — стандартный шаг
        self._send_input(self._create_input(flags=flags, mouse_data=delta * 120), "mouse scroll")

    @contextmanager
    def hold(self, *hold_buttons: MouseButtonParameter):
        pressed_codes = []
        try:
            # Нажимаем все клавиши
            for button in hold_buttons:
                code = self._get_code_form_button(button)
                if code is None:
                    raise ValueError(f"Invalid mouse in hold(): {button}")
                self.send_button(button, press=True)
                pressed_codes.append(code)
            yield
        finally:
            # Отпускаем в обратном порядке (необязательно, но аккуратно)
            for code in reversed(pressed_codes):
                # Используем vk напрямую, чтобы не парсить заново
                self.send_button(code, release=True)

    def is_button_pressed(self, button: MouseButtonParameter) -> bool:
        return self._get_code_form_button(button) in self._pressed_buttons

    def get_position(self) -> tuple[int, int]:
        pt = POINT()
        if user32.GetCursorPos(ctypes.byref(pt)):
            return pt.x, pt.y
        else:
            raise RuntimeError("Failed to get cursor position")
    
    def _get_code_form_button(self, button: MouseButtonParameter) -> Optional[int]:
        if isinstance(button, MouseButton):
            return button.code
        elif isinstance(button, str):
            return get_mouse(button)
        else:
            return int(button)

    def _get_hotkey_list(self, hotkey: MouseHotkeyParameter) -> Sequence[str] | Sequence[MouseButtonParameter]:
        if isinstance(hotkey, str):
            return parse_hotkey_string(hotkey)

        return hotkey
    
    def _send_input(self, inp: INPUT, action: str):
        result = user32.SendInput(1, ctypes.byref(inp), INPUT_SIZE)
        if result == 0:
            raise RuntimeError(f"SendInput {action} failed")

    def _create_input(self, x: int = 0, y: int = 0, mouse_data: int = 0, flags: int = 0) -> INPUT:
        return INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(
                dx=x,
                dy=y,
                mouseData=mouse_data,
                dwFlags=flags,
                time=0,
                dwExtraInfo=None
            )
        )

    def _on_press(self, x: int, y: int, button: MouseButton) -> bool:
        #print(f"{button} pressed")

        self._pressed_buttons.add(button.code)

        suppress = False

        for callback in self._any_button_callbacks.get_all():
            if self._process_callback(MouseEventType.PRESS, callback, x, y, button):
                suppress = True

        for callback in self._button_callbacks.get_by_value(button.code):
            if self._process_callback(MouseEventType.PRESS, callback, x, y, button):
                suppress = True

        pressed_frozen = frozenset(self._pressed_buttons)

        # ON_PRESS — срабатывает каждый раз
        for callback in self._hotkeys_on_press_callbacks.get_by_value(pressed_frozen):
            try:
                callback()
            except Exception as e:
                print(f"[Mouse hotkey ON_PRESS] Error: {e}")

        # ON_PRESS_ONCE — только если ещё не сработало
        if pressed_frozen not in self._active_once_hotkeys:
            self._active_once_hotkeys.add(pressed_frozen)
            for callback in self._hotkeys_on_press_once_callbacks.get_by_value(pressed_frozen):
                try:
                    callback()
                except Exception as e:
                    print(f"[Mouse hotkey ON_PRESS_ONCE] Error: {e}")

        return suppress

    def _on_release(self, x: int, y: int, button: MouseButton) -> bool:
        #print(f"{button} released")

        pressed_frozen = frozenset(self._pressed_buttons)

        released_code = button.code
        self._pressed_buttons.discard(button.code)

        suppress = False

        for callback in self._any_button_callbacks.get_all():
            if self._process_callback(MouseEventType.RELEASE, callback, x, y, button):
                suppress = True

        for callback in self._button_callbacks.get_by_value(button.code):
            if self._process_callback(MouseEventType.RELEASE, callback, x, y, button):
                suppress = True

        # ON_RELEASE: срабатывает при отпускании
        for callback in self._hotkeys_on_release_callbacks.get_by_value(pressed_frozen):
            try:
                callback()
            except Exception as e:
                print(f"[Mouse hotkey ON_RELEASE] Error: {e}")

        to_remove = set()
        for hk in self._active_once_hotkeys:
            if released_code in hk:
                to_remove.add(hk)
        self._active_once_hotkeys -= to_remove

        return suppress

    def _on_move(self, x: int, y: int) -> bool:
        #print(f"move x: {x} y: {y}")

        suppress = False

        for callback in self._move_callbacks.get_all():
            if self._process_callback(MouseEventType.MOVE, callback, x, y):
                suppress = True

        return suppress

    def _on_scroll(self, x: int, y: int, delta: int) -> bool:
        #print(f"scroll delta: {delta}")

        suppress = False

        for callback in self._scroll_callbacks.get_all():
            if self._process_callback(MouseEventType.SCROLL, callback, x, y, delta=delta):
                suppress = True

        return suppress

    def _process_callback(self, event_type: MouseEventType, callback: MouseEventCallback, x: int, y: int, button: Optional[MouseButton] = None, delta: int = 0) -> bool:
        event = MouseEvent(event_type, x, y, button, delta)
        try:
            return callback(event) is False
        except Exception as e:
            print(f"Callback error for mouse event={event}: {e}")
            return False
    
    def _message_loop(self):
        def low_level_mouse_proc(nCode, wParam, lParam):
            try:
                suppress = False
                if nCode >= 0:
                    # lParam указывает на MSLLHOOKSTRUCT
                    ms = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
                    x, y = ms.pt.x, ms.pt.y

                    if wParam == WM_MOUSEMOVE:
                        suppress = self._on_move(x, y)
                    elif wParam == WM_MOUSEWHEEL:
                        delta = ctypes.c_short(ms.mouseData >> 16).value // 120
                        suppress = self._on_scroll(x, y, delta) 
                    elif wParam == WM_LBUTTONDOWN:
                        suppress = self._on_press(x, y, mouseButtons.left)
                    elif wParam == WM_LBUTTONUP:
                        suppress = self._on_release(x, y, mouseButtons.left)
                    elif wParam == WM_RBUTTONDOWN:
                        suppress = self._on_press(x, y, mouseButtons.right)
                    elif wParam == WM_RBUTTONUP:
                        suppress = self._on_release(x, y, mouseButtons.right)
                    elif wParam == WM_MBUTTONDOWN:
                        suppress = self._on_press(x, y, mouseButtons.middle)
                    elif wParam == WM_MBUTTONUP:
                        suppress = self._on_release(x, y, mouseButtons.middle)
                    elif wParam == WM_XBUTTONDOWN:
                        suppress = self._on_press(x, y, mouseButtons.x1 if ms.mouseData == 0x10000 else mouseButtons.x2)
                    elif wParam == WM_XBUTTONUP:
                        suppress = self._on_release(x, y, mouseButtons.x1 if ms.mouseData == 0x10000 else mouseButtons.x2)

                return 1 if suppress else user32.CallNextHookEx(0, nCode, wParam, lParam)
            except Exception as e:
                print(f"Mouse hook error: {e}")
                return user32.CallNextHookEx(0, nCode, wParam, lParam)

        self._hook_proc = HOOKPROC(low_level_mouse_proc)
        self._hook_handle = user32.SetWindowsHookExW(WH_MOUSE_LL, self._hook_proc, 0, 0)
        if not self._hook_handle:
            print("Failed to install mouse hook")
            return

        print("[+] Mouse hook installed")

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
        print("[-] Mouse hook removed")

mouse: Mouse = Mouse()