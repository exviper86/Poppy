from PyQt6.QtCore import QTimer, QEvent, Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from ._palette_change_listener import PaletteChangeListener
from ._global_signals import globalSignals
from ._font import Font
from ._winmica import EnableMica, BackdropType, is_mica_supported

class FluentWindow(QWidget, PaletteChangeListener):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            
    def show(self):
        super().show()
        if is_mica_supported():
            hwnd = int(self.winId())
            EnableMica(hwnd, BackdropType.MICA)
        
    def palette_changed(self, palette: QPalette, is_dark_theme: bool):
        # background-color: {"#373737" if is_dark_theme else "#FEFEFE"};
        self.setStyleSheet(f"""
        QComboBox {{
            background-color: {"#22808080" if is_dark_theme else "#BEFFFFFF"};
            padding: 4 4 4 8;
        }}
        QComboBox QListView {{
            background-color: {"#2C2C2C" if is_dark_theme else "#F9F9F9"};
            border-radius: 4px;
            border: 1px solid {"#454545" if is_dark_theme else "#E5E5E5"};
        }}
        QComboBox QListView::item {{
            padding: 6 8 6 8;
        }}
        QListWidget {{
            background-color: transparent;
            border: none;
        }}
        QListWidget::item {{
            padding: 6;
            margin: 3;
        }}
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        QLineEdit {{
            background-color: {"#22808080" if is_dark_theme else "#BEFFFFFF"};
            padding: 3 8 3 8;
        }}
        """)

        # QLineEdit {{
        #     background-color: {"#373737" if is_dark_theme else "#FEFEFE"};
        # padding: 3 8 3 8;
        # }}

class FluentMainWindow(FluentWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        QApplication.setFont(Font.label())
        
        self._updating_palette = False
        self._update_palette(QApplication.palette())

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.Type.PaletteChange:
            self._update_palette(QApplication.palette())
            globalSignals.applicationPaletteChanged.emit(QApplication.palette())
        super().changeEvent(event)

    def _update_palette(self, palette: QPalette):
        if self._updating_palette:
            return
        self._updating_palette = True

        # is_dark = palette.text().color().lightness() > 128
        # window_color = QColor("#202020") if is_dark else QColor("#F3F3F3")
        # palette.setBrush(QPalette.ColorRole.Window, window_color)
        # QApplication.setPalette(palette)
        # 
        # QTimer.singleShot(20, lambda: setattr(self, '_updating_palette', False))