from dataclasses import dataclass
from typing import Optional

from ._utils import VK_NAMES
from enum import Enum, auto
import time

class Key:
    def __init__(self, vk_code: int):
        self._vk_code = vk_code
        self._name = VK_NAMES.get(vk_code) or "Unknown"

    @property
    def vk(self) -> int: return self._vk_code

    @property
    def name(self) -> str: return self._name

    def __repr__(self):
        return f"{self.name} (vk={self._vk_code})"

    def __eq__(self, other):
        if isinstance(other, Key):
            return self._vk_code == other._vk_code
        return False

class KeyEventType(Enum):
    PRESS = auto()
    RELEASE = auto()

class KeyEvent:
    def __init__(self, event_type: KeyEventType, key: Key):
        self._type = event_type
        self._key = key
        self._time = time.time()

    @property
    def event_type(self) -> KeyEventType:
        return self._type

    @property
    def key(self) -> Key:
        return self._key

    @property
    def time(self) -> float:
        return self._time

    def __repr__(self):
        return f"KeyEvent({self._type}, key={self._key}, time={self._time})"

class HotkeyType(Enum):
    ON_PRESS = auto()
    ON_PRESS_ONCE = auto()
    ON_RELEASE = auto()

@dataclass(frozen=True)
class KeyStroke:
    vk: Optional[int] = None
    shift: bool = False
    ctrl: bool = False
    alt: bool = False