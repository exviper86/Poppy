from typing import Optional
from PyQt6.QtCore import pyqtSignal, Qt, QSize, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint, QTimer
from PyQt6.QtGui import QPalette, QMouseEvent, QColor
from PyQt6.QtWidgets import QFrame, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGraphicsOpacityEffect, QSizePolicy
from ._font import Font
from ._label import Label
from ._palette_change_listener import PaletteChangeListener
from poppy.utils import Utils


class Card(QFrame, PaletteChangeListener):
    def __init__(self, header: Optional[QWidget | str] = None, content: Optional[QWidget] = None):        
        super().__init__()
        
        self._header: Optional[QWidget] = None
        self._content: Optional[QWidget] = None
        self._ident: int = 0
        
        self.setMinimumHeight(54)
        self.setFont(Font.label())
        
        self._layout = QHBoxLayout(self)
        self._layout.setSpacing(16)
        self._layout.insertStretch(1)

        self.setIdent(self._ident)
        
        self.setHeader(header)
        self.setContent(content)

        self.setObjectName("CardWidget")

    def header(self) -> Optional[QWidget]:
        return self._header

    def setHeader(self, header: QWidget | str):
        if self._header is not None:
            self._layout.removeWidget(self._header)
            self._header.deleteLater()
        
        if header is None:
            return
        
        if isinstance(header, str):
            header = Label(header)
        
        self._header = header
        self._layout.insertWidget(0, self._header, stretch=True)

    def content(self) -> Optional[QWidget]:
        return self._content

    def setContent(self, content: QWidget):
        if self._content is not None:
            self._layout.removeWidget(self._content)
            self._content.deleteLater()
        
        if content is None:
            return
        
        self._content = content
        self._layout.insertWidget(2, self._content)
    
    def ident(self) -> int:
        return self._ident
    
    def setIdent(self, ident: int):
        self._ident = ident
        self._layout.setContentsMargins((self._ident + 1) * 16, 6, 16, 6)
    
    def palette_changed(self, palette: QPalette, is_dark: bool):
        # style = f"""
        #      #CardWidget {{
        #         background-color: {"#2B2B2B" if is_dark else "#FBFBFB"};
        #         border: 1px solid {"#1D1D1D" if is_dark else "#E5E5E5"};
        #         border-radius: 5px;
        #     }}
        # """
        style = f"""
             #CardWidget {{
                background-color: {"#643E3E3E" if is_dark else "#BEFFFFFF"};
                border: 1px solid {"#1D1D1D" if is_dark else "#E5E5E5"};
                border-radius: 5px;
            }}
        """
        if isinstance(self, BaseCardAction):
            # style += f"""
            #     #CardWidget:hover {{
            #         background-color: {"#333333" if is_dark else "#F6F6F6"};
            #     }}
            # }}
            # """
            style += f"""
                    #CardWidget:hover {{
                        background-color: {"#A53E3E3E" if is_dark else "#96F9F9F9"};
                    }}
                }}
                """
        self.setStyleSheet(style)

class BaseCardAction(Card):
    clicked = pyqtSignal()

    def __init__(self, header: Optional[QWidget | str] = None, content: Optional[QWidget] = None):
        self._pixmap = Utils.load_pixmap("icons/arrow_right.png", 0.95)
        self._icon_angle = 0
        
        self._icon = QLabel()
        self._icon.setPixmap(self._pixmap)
        self._icon.setFixedSize(QSize(10, 10))
        self._icon.setContentsMargins(0, 0, 0, 0)
        self._icon.setScaledContents(True)

        super().__init__(header, content)
        
        self._layout.insertWidget(3, self._icon, alignment=Qt.AlignmentFlag.AlignRight)
        

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() != Qt.MouseButton.LeftButton:
            return

        child = self.childAt(event.position().toPoint())
        if child is not None and (self._content is not None and self._content.isAncestorOf(child)):
            return
            
        self.clicked.emit()
    
    def palette_changed(self, palette: QPalette, is_dark: bool):
        super().palette_changed(palette, is_dark)
        color = QColor(Qt.GlobalColor.white if is_dark else Qt.GlobalColor.black)
        pixmap = Utils.color_pixmap(self._pixmap, color)
        pixmap = Utils.rotate_pixmap(pixmap, self._icon_angle)
        self._icon.setPixmap(pixmap)
        
    def _rotate_icon(self, angle: float):
        self._icon_angle = angle
        self.update_palette()

class CardAction(BaseCardAction):
    def __init__(self, header: Optional[QWidget | str] = None, content: Optional[QWidget] = None):
        super().__init__(header, content)

class CardExpand(QWidget):
    def __init__(self, header: Optional[QWidget | str] = None, content: Optional[QWidget] = None):
        super().__init__()

        self._is_expanded = False

        self._height_anim: Optional[QPropertyAnimation] = None
        self._opacity_anim: Optional[QPropertyAnimation] = None
        self._opacity_effect: Optional[QGraphicsOpacityEffect] = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self._card = BaseCardAction(header, content)
        self._card._rotate_icon(90)
        self._card.clicked.connect(self._on_card_clicked)
        layout.addWidget(self._card)
        
        self._expanded_content = QWidget()
        #self._expanded_content.setVisible(False)
        self._expanded_content.setMaximumHeight(0)
        self._expanded_content.move(0, self._card.height() - 20)
        
        self._expanded_layout = QVBoxLayout(self._expanded_content)
        self._expanded_layout.setContentsMargins(0, 0, 0, 0)
        self._expanded_layout.setSpacing(0)
        
        layout.addWidget(self._expanded_content)
    
    def setExpandedContentEnabled(self, enabled: bool):
        self._expanded_content.setEnabled(enabled)
    
    def addExpandContent(self, content: Card):
        margin = content.contentsMargins()
        margin.setLeft(16)
        margin.setRight(26)
        content.setContentsMargins(margin)
        
        self._expanded_layout.addWidget(content)
    
    def isExpanded(self) -> bool:
        return self._is_expanded
    
    def setExpanded(self, expanded: bool, with_animation: bool = True):
        if self._is_expanded == expanded:
            return
        
        self._is_expanded = expanded
        self._card.raise_()
        
        #self._expanded_content.setVisible(self._is_expanded)
            
        self._card._rotate_icon(-90 if self._is_expanded else 90)

        if self._height_anim is not None:
            self._height_anim.stop()
        if self._opacity_anim is not None:
            self._opacity_anim.stop()
        
        if not with_animation:
            self._expanded_content.setMaximumHeight(self._expanded_content.sizeHint().height() if self._is_expanded else 0)
            if self._opacity_effect is not None:
                self._opacity_effect.setOpacity(1.0 if self._is_expanded else 0.0)
            self.updateGeometry()
            self._expanded_content.updateGeometry()
            return
        
        
        # Настройка анимации
        anim_duration = 250
        
        self._height_anim = QPropertyAnimation(self._expanded_content, b"maximumHeight")
        self._height_anim.setDuration(anim_duration)
        self._height_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        if self._opacity_effect is None:
            self._opacity_effect = QGraphicsOpacityEffect(self._expanded_content)
            self._opacity_effect.setOpacity(0.0 if self._is_expanded else 1.0)
        self._expanded_content.setGraphicsEffect(self._opacity_effect)

        self._opacity_anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._opacity_anim.setDuration(anim_duration)
        self._opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self._height_anim.setEndValue(self._expanded_content.sizeHint().height() if self._is_expanded else 0)
        self._opacity_anim.setEndValue(1.0 if self._is_expanded else 0.0)
        
        self._height_anim.start()
        self._height_anim.valueChanged.connect(self.updateGeometry)
        self._opacity_anim.start()
        self._opacity_anim.valueChanged.connect(self._expanded_content.updateGeometry)

        self.updateGeometry()
        self._expanded_content.updateGeometry()
    
    def _on_card_clicked(self):
        self.setExpanded(not self._is_expanded)
        
