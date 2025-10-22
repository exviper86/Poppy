# localization.py

from typing import Dict
from PyQt6.QtCore import QObject, pyqtSignal

class Localizer(QObject):
    language_changed = pyqtSignal(str)

    def __init__(self, translations: Dict[str, Dict[str, str]], default_lang: str):
        super().__init__()
        if default_lang not in translations:
            raise ValueError(f"Default language '{default_lang}' not in translations")
        self._translations = translations
        self._lang = default_lang

    def set_language(self, lang: str):
        if lang not in self._translations:
            raise ValueError(f"Unsupported language: {lang}")
        if self._lang == lang:
            return
        self._lang = lang
        self.language_changed.emit(lang)

    def tr(self, key: str) -> str:
        return self._translations[self._lang].get(key, f"{{{key}}}")

    @property
    def current_language(self) -> str:
        return self._lang