from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName("Widget")
        self.setStyleSheet("#Widget { background-color: transparent; }")