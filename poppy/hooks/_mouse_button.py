from enum import Enum, auto
from typing import Optional
from ._utils import MOUSE_NAMES

class MouseButton:
    def __init__(self, code: int):
        self._code = code
        self._name = MOUSE_NAMES.get(code)

    @property
    def code(self) -> int: return self._code

    @property
    def name(self) -> str: return self._name

    def __repr__(self):
        return f"{self.name} (vk={self._code})"

    def __eq__(self, other):
        if isinstance(other, MouseButton):
            return self._code == other._code
        return False

class MouseEventType(Enum):
    PRESS = auto()
    RELEASE = auto()
    MOVE = auto()
    SCROLL = auto()

class MouseEvent:
    def __init__(self, event_type: MouseEventType, x: int, y: int, button: Optional[MouseButton] = None, delta: int = 0):
        self._type = event_type
        self._x = x
        self._y = y
        self._button = button
        self._delta = delta  # для колеса

    @property
    def event_type(self) -> MouseEventType:
        return self._type

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def button(self) -> Optional[MouseButton]:
        return self._button

    @property
    def delta(self) -> int:
        return self._delta

    def __repr__(self):
        if self._type == MouseEventType.SCROLL:
            return f"MouseEvent(SCROLL, delta={self._delta}, x={self._x}, y={self._y})"
        return f"MouseEvent({self._type}, button={self._button}, x={self._x}, y={self._y})"