from PyQt6.QtGui import QFont

class Font:
    def __new__(cls):
        raise TypeError(f"'{cls.__name__}' is a static class and cannot be instantiated.")

    @staticmethod
    def label() -> QFont:
        font = QFont("Segoe UI")
        font.setPointSizeF(10.5)
        return font
    
    @staticmethod
    def header() -> QFont:
        return QFont("Segoe UI", 21, weight=QFont.Weight.DemiBold)

    @staticmethod
    def title() -> QFont:
        return QFont("Segoe UI", 16, weight=QFont.Weight.DemiBold)

    @staticmethod
    def subTitle() -> QFont:
        return QFont("Segoe UI", 12, weight=QFont.Weight.DemiBold)