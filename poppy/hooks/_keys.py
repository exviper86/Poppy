from ._key import Key

class Keys:
    # Стандартные
    @property
    def cancel(self) -> Key: return Key(0x03)
    @property
    def backspace(self) -> Key: return Key(0x08)
    @property
    def tab(self) -> Key: return Key(0x09)
    @property
    def clear(self) -> Key: return Key(0x0C)
    @property
    def enter(self) -> Key: return Key(0x0D)
    @property
    def pause(self) -> Key: return Key(0x13)
    @property
    def caps_lock(self) -> Key: return Key(0x14)
    @property
    def kana_mode(self) -> Key: return Key(0x15)
    @property
    def junja_mode(self) -> Key: return Key(0x17)
    @property
    def final_mode(self) -> Key: return Key(0x18)
    @property
    def kanji_mode(self) -> Key: return Key(0x19)
    @property
    def esc(self) -> Key: return Key(0x1B)
    @property
    def convert(self) -> Key: return Key(0x1C)
    @property
    def nonconvert(self) -> Key: return Key(0x1D)
    @property
    def accept(self) -> Key: return Key(0x1E)
    @property
    def mode_change(self) -> Key: return Key(0x1F)
    @property
    def space(self) -> Key: return Key(0x20)
    @property
    def page_up(self) -> Key: return Key(0x21)
    @property
    def page_down(self) -> Key: return Key(0x22)
    @property
    def end(self) -> Key: return Key(0x23)
    @property
    def home(self) -> Key: return Key(0x24)
    @property
    def left(self) -> Key: return Key(0x25)
    @property
    def up(self) -> Key: return Key(0x26)
    @property
    def right(self) -> Key: return Key(0x27)
    @property
    def down(self) -> Key: return Key(0x28)
    @property
    def select(self) -> Key: return Key(0x29)
    @property
    def print_key(self) -> Key: return Key(0x2A)
    @property
    def execute(self) -> Key: return Key(0x2B)
    @property
    def print_screen(self) -> Key: return Key(0x2C)
    @property
    def insert(self) -> Key: return Key(0x2D)
    @property
    def delete(self) -> Key: return Key(0x2E)
    @property
    def help(self) -> Key: return Key(0x2F)
    
    # Цифры
    @property
    def n0(self) -> Key: return Key(0x30)
    @property
    def n1(self) -> Key: return Key(0x31)
    @property
    def n2(self) -> Key: return Key(0x32)
    @property
    def n3(self) -> Key: return Key(0x33)
    @property
    def n4(self) -> Key: return Key(0x34)
    @property
    def n5(self) -> Key: return Key(0x35)
    @property
    def n6(self) -> Key: return Key(0x36)
    @property
    def n7(self) -> Key: return Key(0x37)
    @property
    def n8(self) -> Key: return Key(0x38)
    @property
    def n9(self) -> Key: return Key(0x39)
    
    # Буквы
    @property
    def a(self) -> Key: return Key(0x41)
    @property
    def b(self) -> Key: return Key(0x42)
    @property
    def c(self) -> Key: return Key(0x43)
    @property
    def d(self) -> Key: return Key(0x44)
    @property
    def e(self) -> Key: return Key(0x45)
    @property
    def f(self) -> Key: return Key(0x46)
    @property
    def g(self) -> Key: return Key(0x47)
    @property
    def h(self) -> Key: return Key(0x48)
    @property
    def i(self) -> Key: return Key(0x49)
    @property
    def j(self) -> Key: return Key(0x4A)
    @property
    def k(self) -> Key: return Key(0x4B)
    @property
    def l(self) -> Key: return Key(0x4C)
    @property
    def m(self) -> Key: return Key(0x4D)
    @property
    def n(self) -> Key: return Key(0x4E)
    @property
    def o(self) -> Key: return Key(0x4F)
    @property
    def p(self) -> Key: return Key(0x50)
    @property
    def q(self) -> Key: return Key(0x51)
    @property
    def r(self) -> Key: return Key(0x52)
    @property
    def s(self) -> Key: return Key(0x53)
    @property
    def t(self) -> Key: return Key(0x54)
    @property
    def u(self) -> Key: return Key(0x55)
    @property
    def v(self) -> Key: return Key(0x56)
    @property
    def w(self) -> Key: return Key(0x57)
    @property
    def x(self) -> Key: return Key(0x58)
    @property
    def y(self) -> Key: return Key(0x59)
    @property
    def z(self) -> Key: return Key(0x5A)

    # win
    @property
    def left_win(self) -> Key: return Key(0x5B)
    @property
    def right_win(self) -> Key: return Key(0x5C)
    @property
    def menu(self) -> Key: return Key(0x5D)
    
    # Numpad
    @property
    def numpad_0(self) -> Key: return Key(0x60)
    @property
    def numpad_1(self) -> Key: return Key(0x61)
    @property
    def numpad_2(self) -> Key: return Key(0x62)
    @property
    def numpad_3(self) -> Key: return Key(0x63)
    @property
    def numpad_4(self) -> Key: return Key(0x64)
    @property
    def numpad_5(self) -> Key: return Key(0x65)
    @property
    def numpad_6(self) -> Key: return Key(0x66)
    @property
    def numpad_7(self) -> Key: return Key(0x67)
    @property
    def numpad_8(self) -> Key: return Key(0x68)
    @property
    def numpad_9(self) -> Key: return Key(0x69)
    @property
    def numpad_multiply(self) -> Key: return Key(0x6A)
    @property
    def numpad_add(self) -> Key: return Key(0x6B)
    @property
    def numpad_separator(self) -> Key: return Key(0x6C)
    @property
    def numpad_subtract(self) -> Key: return Key(0x6D)
    @property
    def numpad_decimal(self) -> Key: return Key(0x6E)
    @property
    def numpad_divide(self) -> Key: return Key(0x6F)
    
    # F1–F24
    @property
    def f1(self) -> Key: return Key(0x70)
    @property
    def f2(self) -> Key: return Key(0x71)
    @property
    def f3(self) -> Key: return Key(0x72)
    @property
    def f4(self) -> Key: return Key(0x73)
    @property
    def f5(self) -> Key: return Key(0x74)
    @property
    def f6(self) -> Key: return Key(0x75)
    @property
    def f7(self) -> Key: return Key(0x76)
    @property
    def f8(self) -> Key: return Key(0x77)
    @property
    def f9(self) -> Key: return Key(0x78)
    @property
    def f10(self) -> Key: return Key(0x79)
    @property
    def f11(self) -> Key: return Key(0x7A)
    @property
    def f12(self) -> Key: return Key(0x7B)
    @property
    def f13(self) -> Key: return Key(0x7C)
    @property
    def f14(self) -> Key: return Key(0x7D)
    @property
    def f15(self) -> Key: return Key(0x7E)
    @property
    def f16(self) -> Key: return Key(0x7F)
    @property
    def f17(self) -> Key: return Key(0x80)
    @property
    def f18(self) -> Key: return Key(0x81)
    @property
    def f19(self) -> Key: return Key(0x82)
    @property
    def f20(self) -> Key: return Key(0x83)
    @property
    def f21(self) -> Key: return Key(0x84)
    @property
    def f22(self) -> Key: return Key(0x85)
    @property
    def f23(self) -> Key: return Key(0x86)
    @property
    def f24(self) -> Key: return Key(0x87)
    
    # Специальные
    @property
    def num_lock(self) -> Key: return Key(0x90)
    @property
    def scroll_lock(self) -> Key: return Key(0x91)
    @property
    def left_shift(self) -> Key: return Key(0xA0)
    @property
    def right_shift(self) -> Key: return Key(0xA1)
    @property
    def left_ctrl(self) -> Key: return Key(0xA2)
    @property
    def right_ctrl(self) -> Key: return Key(0xA3)
    @property
    def left_alt(self) -> Key: return Key(0xA4)
    @property
    def right_alt(self) -> Key: return Key(0xA5)
    @property
    def browser_back(self) -> Key: return Key(0xA6)
    @property
    def browser_forward(self) -> Key: return Key(0xA7)
    @property
    def browser_refresh(self) -> Key: return Key(0xA8)
    @property
    def browser_stop(self) -> Key: return Key(0xA9)
    @property
    def browser_search(self) -> Key: return Key(0xAA)
    @property
    def browser_favorites(self) -> Key: return Key(0xAB)
    @property
    def browser_home(self) -> Key: return Key(0xAC)
    @property
    def volume_mute(self) -> Key: return Key(0xAD)
    @property
    def volume_down(self) -> Key: return Key(0xAE)
    @property
    def volume_up(self) -> Key: return Key(0xAF)
    @property
    def next_track(self) -> Key: return Key(0xB0)
    @property
    def previous_track(self) -> Key: return Key(0xB1)
    @property
    def stop(self) -> Key: return Key(0xB2)
    @property
    def play_pause(self) -> Key: return Key(0xB3)
    @property
    def launch_mail(self) -> Key: return Key(0xB4)
    @property
    def launch_media_select(self) -> Key: return Key(0xB5)
    @property
    def launch_app_1(self) -> Key: return Key(0xB6)
    @property
    def launch_app_2(self) -> Key: return Key(0xB7)

    # OEM-клавиши
    @property
    def semicolon(self) -> Key: return Key(0xBA)
    @property
    def equal(self) -> Key: return Key(0xBB)
    @property
    def comma(self) -> Key: return Key(0xBC)
    @property
    def minus(self) -> Key: return Key(0xBD)
    @property
    def period(self) -> Key: return Key(0xBE)
    @property
    def slash(self) -> Key: return Key(0xBF)
    @property
    def backquote(self) -> Key: return Key(0xC0)
    @property
    def left_bracket(self) -> Key: return Key(0xDB)
    @property
    def backslash(self) -> Key: return Key(0xDC)
    @property
    def right_bracket(self) -> Key: return Key(0xDD)
    @property
    def quote(self) -> Key: return Key(0xDE)

    # Системные/редкие
    @property
    def attn(self) -> Key: return Key(0xF6)
    @property
    def crsel(self) -> Key: return Key(0xF7)
    @property
    def exsel(self) -> Key: return Key(0xF8)
    @property
    def ereof(self) -> Key: return Key(0xF9)
    @property
    def play(self) -> Key: return Key(0xFA)
    @property
    def zoom(self) -> Key: return Key(0xFB)
    @property
    def no_name(self) -> Key: return Key(0xFC)
    @property
    def pa1(self) -> Key: return Key(0xFD)
    @property
    def oem_clear(self) -> Key: return Key(0xFE)

keys: Keys = Keys()