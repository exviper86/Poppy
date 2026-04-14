from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPalette


class GlobalSignals(QObject):
    applicationPaletteChanged = pyqtSignal(QPalette)

globalSignals: GlobalSignals = GlobalSignals()