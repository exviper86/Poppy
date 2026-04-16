# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pyperclip
from .language_handler import LanguageHandler
from .hooks import *
from .config import config
import asyncio

class LayoutSwitcher:
    def __init__(self):
        from .app import App
        self._app = App.instance()
        self._language_handler: LanguageHandler = self._app.language_handler

        self._keys: list[KeyStroke] = []
        self._is_busy = False
        self._just_switched_last = False

        self._switch_last_id: int | None = None
        self._switch_selected_id: int | None = None
        self._switch_case_id: int | None = None
        self._mouse_hook_id: int | None = None
        self._key_hook_id: int | None = None

        self.set_switch_last_hotkey(config.layout_switch.last_hotkey.value)
        self.set_switch_selected_hotkey(config.layout_switch.selected_hotkey.value)
        self.set_switch_case_hotkey(config.layout_switch.case_hotkey.value)
        
        config.layout_switch.last_hotkey.valueChanged.connect(self.set_switch_last_hotkey)
        config.layout_switch.selected_hotkey.valueChanged.connect(self.set_switch_selected_hotkey)
        config.layout_switch.case_hotkey.valueChanged.connect(self.set_switch_case_hotkey)
    
    def start(self):
        if not keyboard.is_running:
            keyboard.start()
        if not mouse.is_running:
            mouse.start()
    
    def stop(self):
        if keyboard.is_running:
            keyboard.stop()
        if mouse.is_running:
            mouse.stop()

    def set_switch_last_hotkey(self, hotkey: str):
        if self._switch_last_id:
            keyboard.unhook_hotkey(self._switch_last_id)
            self._switch_last_id = None
        if self._key_hook_id:
            keyboard.unhook(self._key_hook_id)
            self._key_hook_id = None
        if self._mouse_hook_id:
            mouse.unhook(self._mouse_hook_id)
            self._mouse_hook_id = None

        if hotkey:
            self._switch_last_id = keyboard.hook_hotkey(hotkey, self._switch_last)
            self._key_hook_id = keyboard.hook(self._on_key)
            self._mouse_hook_id = mouse.hook(self._on_click)
    
    def set_switch_selected_hotkey(self, hotkey: str):
        if self._switch_selected_id:
            keyboard.unhook_hotkey(self._switch_selected_id)
            self._switch_selected_id = None

        if hotkey:
            self._switch_selected_id = keyboard.hook_hotkey(hotkey, self._switch_selected)

    def set_switch_case_hotkey(self, hotkey: str):
        if self._switch_case_id:
            keyboard.unhook_hotkey(self._switch_case_id)
            self._switch_case_id = None

        if hotkey:
            self._switch_case_id = keyboard.hook_hotkey(hotkey, self._switch_register)
    
    def _switch_last(self):
        if config.layout_switch.last_hotkey.value:
            self._app.call_soon_threadsafe(
                lambda: asyncio.create_task(self._switch_last_async())
            )

    def _switch_selected(self):
        if config.layout_switch.selected_hotkey.value:
            self._app.call_soon_threadsafe(
                lambda: asyncio.create_task(self._switch_selected_async())
            )

    def _switch_register(self):
        if config.layout_switch.case_hotkey.value:
            self._app.call_soon_threadsafe(
                lambda: asyncio.create_task(self._switch_register_async())
            )

    async def _switch_last_async(self):
        print("switch last")

        if self._is_busy:
            return

        if len(self._keys) == 0:
            layout = self._language_handler.get_layout()
            new_layout = self._language_handler.set_next_layout(layout)
            self._app.show_layout(new_layout)
            return
        
        self._is_busy = True
        
        try:
            layout = self._language_handler.get_layout()
            new_layout = self._language_handler.set_next_layout(layout)
            self._app.show_layout(new_layout)
            
            print(self._keys)
    
            for _ in self._keys:
                keyboard.click_key(keys.backspace)

            await asyncio.sleep(0.02)

            for ks in self._keys:
                keyboard.click_keystroke(ks)
            
            self._just_switched_last = True

        except Exception as e:
            print(e)
        finally:
            self._is_busy = False
    
    async def _switch_selected_async(self):
        print("switch selected")

        if self._is_busy:
            return
        
        self._is_busy = True

        original = pyperclip.paste()
        #print("original", original)
        
        try:
            keyboard.release_key("left shift")
            keyboard.release_key("right shift")
            keyboard.release_key("left alt")
            keyboard.release_key("right alt")
            
            keyboard.click_hotkey("ctrl+c")
    
            await asyncio.sleep(0.03)
            
            copied = pyperclip.paste()
            print("copied", copied)
            
            if not copied.strip() or original == copied:
                return
            
            layouts = self._language_handler.get_all_layouts()
            
            keystrokes: list[KeyStroke] = []
            layout = None
            for l in layouts:
                keystrokes.clear()
                for char in copied:
                    keystroke = keyboard.char_to_keystroke(char, l)
                    if keystroke is not None:
                        keystrokes.append(keystroke)
                if len(keystrokes) == len(copied):
                    layout = l
                    break
            
            if layout is None:
                return 
            
            new_layout = self._language_handler.set_next_layout(layout)
            self._app.show_layout(new_layout)
            #print("new_layout", new_layout)
            #print("layout", layout)

            await asyncio.sleep(0.02)
            
            result = ""
            for ks in keystrokes:
                result += keyboard.keystroke_to_char(ks, new_layout)
            
            print("result", result)

            pyperclip.copy(result)
            await asyncio.sleep(0.03)

            keyboard.click_hotkey("ctrl+v")
            #keyboard.type(result)
            
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(0.03)
            pyperclip.copy(original)
            self._is_busy = False
    
    async def _switch_register_async(self):
        print("switch register")

        if self._is_busy:
            return

        self._is_busy = True

        original = pyperclip.paste()
        #print("original", original)

        try:
            keyboard.release_key("left shift")
            keyboard.release_key("right shift")
            keyboard.release_key("left alt")
            keyboard.release_key("right alt")
            
            keyboard.click_hotkey("ctrl+c")

            await asyncio.sleep(0.03)

            copied = pyperclip.paste()
            print("copied", copied)

            if not copied.strip() or original == copied:
                self._is_busy = False
                return

            result = copied.swapcase()

            print("result", result)

            pyperclip.copy(result)
            await asyncio.sleep(0.03)

            keyboard.click_hotkey("ctrl+v")
            # keyboard.type(result)

        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(0.03)
            pyperclip.copy(original)
            self._is_busy = False

    def _on_key(self, e: KeyEvent):
        if config.layout_switch.last_hotkey.value:
            self._app.call_soon_threadsafe(self._do_on_key, e)

    def _do_on_key(self, e: KeyEvent):
        if e.event_type == KeyEventType.RELEASE or self._is_busy or e.key == keys.pause:
            return

        if e.key == keys.backspace:
            if self._keys:
                self._keys.pop()
            return

        if self._just_switched_last:
            self._just_switched_last = False
            self._keys.clear()

        if e.key in [keys.space, keys.enter, keys.esc, keys.tab, keys.left, keys.right, keys.up, keys.down,
                     keys.delete, keys.home, keys.end, keys.page_up, keys.page_down]:
            self._keys.clear()
            return

        if self._is_printable(e.key):
            if keyboard.is_ctrl_pressed() or keyboard.is_alt_pressed():
                self._keys.clear()  # это хоткей, не текст
                return

            shift_pressed = keyboard.is_shift_pressed()
            caps_on = keyboard.get_caps_lock()
            shifted = (shift_pressed and not caps_on) or (not shift_pressed and caps_on)
            self._keys.append(KeyStroke(vk=e.key.vk, shift=shifted))
    
    def _on_click(self, e: MouseEvent):
        if config.layout_switch.last_hotkey.value:
            self._app.call_soon_threadsafe(self._do_on_click, e)
        
    def _do_on_click(self, e: MouseEvent):
        if e.event_type == MouseEventType.RELEASE or self._is_busy:
            return

        self._keys.clear()
    
    @staticmethod
    def _is_printable(key: Key) -> bool:
        # 1. Буквы (a-z) и цифры верхнего ряда (0-9) → их name односимвольный
        if len(key.name) == 1:
            return True
    
        # 2. OEM-клавиши, которые печатают знаки препинания (их name — многосимвольный)
        return key in [
            keys.semicolon,         # ;
            keys.equal,             # =
            keys.comma,             # ,
            keys.minus,             # -
            keys.period,            # .
            keys.slash,             # /
            keys.backquote,         # `
            keys.left_bracket,      # [
            keys.backslash,         # \
            keys.right_bracket,     # ]
            keys.quote,             # '
            # Цифровая клавиатура (печатает, если Num Lock включён)
            keys.numpad_0,
            keys.numpad_1,
            keys.numpad_2,
            keys.numpad_3,
            keys.numpad_4,
            keys.numpad_5,
            keys.numpad_6,
            keys.numpad_7,
            keys.numpad_8,
            keys.numpad_9,
            keys.numpad_decimal,     # точка
            keys.numpad_add,         # +
            keys.numpad_subtract,    # -
            keys.numpad_multiply,    # *
            keys.numpad_divide,      # /
        ]