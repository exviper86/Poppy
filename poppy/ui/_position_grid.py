from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QWidget, QGridLayout, QToolButton, QSizePolicy
from poppy.ui.fluent import PaletteChangeListener
from poppy.utils import Utils


class PositionGrid(QWidget, PaletteChangeListener):
    positionChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_position: str | None = None
        self._buttons = {}

        # Позиции: 9 точек, включая центр и стороны
        self._positions = {
            "left-top": (0, 0),
            "top": (0, 1),
            "right-top": (0, 2),
            "left": (1, 0),
            "center": (1, 1),
            "right": (1, 2),
            "left-bottom": (2, 0),
            "bottom": (2, 1),
            "right-bottom": (2, 2),
        }

        self._init_ui()

    def _init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        for pos_name, (row, col) in self._positions.items():
            btn = QToolButton()
            # Убираем фиксированный размер — пусть растягивается
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, p=pos_name: self._on_button_clicked(p))
            self._buttons[pos_name] = btn
            layout.addWidget(btn, row, col)

        # Важно: делаем виджет компактным по умолчанию
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def _on_button_clicked(self, position: str):
        for btn in self._buttons.values():
            btn.setChecked(False)
        self._buttons[position].setChecked(True)
        self._selected_position = position
        self.positionChanged.emit(position)

    def setPosition(self, position: str):
        if position in self._buttons:
            self._on_button_clicked(position)

    def position(self) -> str | None:
        return self._selected_position
    
    def spacing(self) -> int:
        return self.layout().spacing()
    
    def setSpacing(self, spacing: int):
        self.layout().setSpacing(spacing)
    
    def sizeHint(self):
        # Предлагаем компактный размер, например 100x100
        return QSize(100, 100)

    def minimumSizeHint(self):
        return QSize(80, 80)

    def palette_changed(self, palette: QPalette, is_dark_theme: bool):
        self.setStyleSheet(f"""
            QToolButton {{
                background-color: {"#1E808080" if is_dark_theme else "#BEFFFFFF"};
                border: 1px solid {"#1D1D1D" if is_dark_theme else "#E5E5E5"};
                border-radius: 5px;
            }}
            QToolButton:hover {{
                 background-color: {"#A53E3E3E" if is_dark_theme else "#96F9F9F9"};
            }}
            QToolButton:checked {{
                background-color: { palette.accent().color().name() };
            }}
            QToolButton:disabled {{
                background-color: {"#0F808080" if is_dark_theme else "#5FFFFFFF"};
            }}
            QToolButton:disabled:checked {{
                background-color: { Utils.color_with_alpha(palette.accent().color().name(), 128) };
            }}
        """)

        # QToolButton:pressed {{
        #     background-color: {"#272727" if is_dark_theme else "#F3F3F3"};
        # }}
        