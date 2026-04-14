from typing import Optional
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel
from ._font import Font


class Label(QLabel):
     def __init__(self, text: Optional[str] = None, font: Optional[QFont] = None):
        super().__init__()
        
        if font is None:
            font = Font.label()
            
        self.setFont(font)
        self.setText(text)
        self.setWordWrap(True)
        self.setContentsMargins(0,-2,0,0)