from collections import defaultdict
from typing import TypeVar, Generic, Optional

TValue = TypeVar('TValue')
TCallback = TypeVar('TCallback')

_id = 0

class Callbacks(Generic[TCallback]):
    def __init__(self):
        self._callbacks: dict[int, TCallback] = {}

    def add(self, callback: TCallback) -> int:
        global _id
        _id += 1
        self._callbacks[_id] = callback
        return _id

    def remove(self, callback_id: int) -> bool:
        return self._callbacks.pop(callback_id, None) is not None

    def clear(self):
        self._callbacks.clear()

    def get_all(self) -> list[TCallback]:
        return list(self._callbacks.values())

class ValuableCallback(Generic[TValue, TCallback]):
    def __init__(self, value: TValue, callback: TCallback):
        self._value = value
        self._callback = callback
        
    @property
    def value(self) -> TValue:
        return self._value
    
    @property
    def callback(self) -> TCallback:
        return self._callback

class ValuableCallbacks(Generic[TValue, TCallback]):
    def __init__(self):
        self._callbacks: dict[int, ValuableCallback[TValue, TCallback]] = {}
        self._by_value: defaultdict[TValue, set[int]] = defaultdict(set)       # индекс для быстрого поиска

    def add(self, value: TValue, callback: TCallback) -> int:
        global _id
        _id += 1
        self._callbacks[_id] = ValuableCallback(value, callback)
        self._by_value[value].add(_id)
        return _id

    def remove(self, callback_id: int) -> Optional[ValuableCallback]:
        callback = self._callbacks.pop(callback_id, None)
        if callback is not None:
            self._by_value[callback.value].discard(callback_id)
            if not self._by_value[callback.value]:
                del self._by_value[callback.value]
            return callback
        return None

    def remove_by_value(self, value: TValue):
        callback_ids = self._by_value.pop(value, None)
        if callback_ids is None:
            return
        for lid in callback_ids:
            self._callbacks.pop(lid, None)
    
    def clear(self):
        self._callbacks.clear()
        self._by_value.clear()
     
    def get_by_value(self, value: TValue) -> list[TCallback]:
        return [
            self._callbacks[lid].callback
            for lid in self._by_value.get(value, ())
            if lid in self._callbacks
        ]