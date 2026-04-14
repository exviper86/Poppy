from abc import abstractmethod
from PyQt6.QtCore import QObject
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication
from ._global_signals import globalSignals

class PaletteChangeListener:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_palette()
        globalSignals.applicationPaletteChanged.connect(self._on_palette_changed)

        if isinstance(self, QObject):
            self.destroyed.connect(self._cleanup)

    def _cleanup(self):
        try:
            globalSignals.applicationPaletteChanged.disconnect(self._on_palette_changed)
        except (TypeError, RuntimeError):
            pass
    
    def __del__(self):
        self._cleanup()
    
    def update_palette(self):
        self._on_palette_changed(QApplication.palette())
    
    @abstractmethod
    def palette_changed(self, palette: QPalette, is_dark_theme: bool):
        pass
    
    def _on_palette_changed(self, palette: QPalette):
        try:
            is_dark = palette.window().color().lightness() < 128
            self.palette_changed(palette, is_dark)
        except RuntimeError:
            pass