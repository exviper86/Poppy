from typing import Optional, Type
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QSize, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QScrollArea, QListWidgetItem, QGraphicsOpacityEffect, QSizePolicy
from ._label import Label
from ._font import Font
from ._widget import Widget

class Page(Widget):
    def __init__(self):
        super().__init__()
        
        self._name: Optional[str] = None
        
    def name(self) -> str:
        return self._name
    
    def setName(self, name: str):
        self._name = name

class NavigationViewItem(QListWidgetItem):
    def __init__(self, page_type: Type[Page], text: str , icon: Optional[QIcon] = None):
        super().__init__(text)
        
        if icon is not None:
            self.setIcon(icon)
        
        self.page_type = page_type

class NavigationView(QWidget):
    selectedItemChanged = pyqtSignal(NavigationViewItem)
    
    def __init__(self, title: Optional[QWidget | str] = None, header: Optional[QWidget] = None):
        super().__init__()
        
        self._selected_item: Optional[NavigationViewItem] = None
        
        self._title: Optional[QWidget] = None
        self._header: Optional[QWidget] = None
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 0)
        main_layout.setSpacing(16)
        
        self._list_layout = QVBoxLayout()
        self._list_layout.setContentsMargins(0, 0, 0, 16)
        self._list_layout.setSpacing(0)
        main_layout.addLayout(self._list_layout)
        
        self._items_list = QListWidget()
        self._items_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._items_list.setFocusProxy(None)
        self._list_layout.addWidget(self._items_list, stretch=True)
        
        self._footer_items_list = QListWidget()
        self._footer_items_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._footer_items_list.setFocusProxy(None)
        self._footer_items_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._footer_items_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list_layout.addWidget(self._footer_items_list)
                
        self.setListWidth(200)
        
        self._view_layout = QVBoxLayout()
        self._view_layout.setContentsMargins(0, 0, 0, 0)
        self._view_layout.setSpacing(0)
        main_layout.addLayout(self._view_layout)
        
        self._scroll = QScrollArea()
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._view_layout.addWidget(self._scroll, stretch=True)
        
        self.setTitle(title)
        self.setHeader(header)
        
        self._items_list.itemClicked.connect(self._item_changed)
        self._footer_items_list.itemClicked.connect(self._item_changed)

    def title(self) -> Optional[QWidget]:
        return self._title

    def setTitle(self, title: QWidget | str):
        if self._title is not None:
            self._list_layout.removeWidget(self._title)
            self._title.deleteLater()
        
        if title is None:
            return
        
        if isinstance(title, str):
            title = Label(title, Font.title())
            title.setContentsMargins(8, 0, 8, 16)
        
        self._title = title
        self._list_layout.insertWidget(0, self._title)
            
    def header(self) -> Optional[QWidget]:
        return self._header
    
    def setHeader(self, header: QWidget):
        if self._header is not None:
            self._list_layout.removeWidget(self._header)
            self._header.deleteLater()

        if header is None:
            return

        self._header = header
        self._view_layout.insertWidget(0, self._header)
        
    def listWidth(self) -> int:
        return self._items_list.width()
    
    def setListWidth(self, width: int):
        self._items_list.setFixedWidth(width)
        self._footer_items_list.setFixedWidth(width)
        
    def addItem(self, item: NavigationViewItem):
        self._items_list.addItem(item)
        if self._items_list.count() == 1:
            self._item_changed(item)

    def removeItem(self, item: NavigationViewItem):
        self._items_list.removeItemWidget(item)
    
    def removeAllItems(self):
        self._items_list.clear()
    
    def itemsCount(self) -> int:
        return self._items_list.count()
    
    def getItem(self, index: int) -> NavigationViewItem:
        return self._items_list.item(index)
    
    def selectedItem(self) -> Optional[NavigationViewItem]:
        return self._selected_item
    
    def setSelectedItem(self, item: NavigationViewItem):
        self._item_changed(item)
    
    def addFooterItem(self, item: NavigationViewItem):
        self._footer_items_list.addItem(item)
        self._update_footer_height()
    
    def removeFooterItem(self, item: NavigationViewItem):
        self._footer_items_list.removeItemWidget(item)
        self._update_footer_height()
    
    def removeAllFooterItems(self):
        self._footer_items_list.clear()
        self._update_footer_height()
    
    def footerItemsCount(self) -> int:
        return self._footer_items_list.count()
    
    def getFooterItem(self, index: int) -> NavigationViewItem:
        return self._footer_items_list.item(index)
        
    def setIconSize(self, size: QSize):
        self._items_list.setIconSize(size)
        self._footer_items_list.setIconSize(size)
    
    def _item_changed(self, item: NavigationViewItem):
        if item == self._selected_item:
            return
        
        old_page = self._scroll.widget()
        if old_page:
            old_page.deleteLater()
        
        #self._items_list.blockSignals(True)
        #self._footer_items_list.blockSignals(True)
        
        if self._selected_item is not None:
            self._selected_item.setSelected(False)
            #self._items_list.setCurrentItem(None)
            #self._footer_items_list.setCurrentItem(None)
            
        #self._items_list.blockSignals(False)
        #self._footer_items_list.blockSignals(False)

        item.setSelected(True)
        self._selected_item = item
        
        self.selectedItemChanged.emit(item)
        
        if item.page_type is None:
            return
        
        page = item.page_type()

        opacity_effect = QGraphicsOpacityEffect(page)
        page.setGraphicsEffect(opacity_effect)
        
        self._scroll.setWidget(page)
        self._scroll.setWidgetResizable(True)

        self._animate_page(page, opacity_effect)

    def _animate_page(self, page: QWidget, effect: QGraphicsOpacityEffect):
        self._opacity_anim = QPropertyAnimation(effect, b"opacity")
        self._opacity_anim.setDuration(250)
        self._opacity_anim.setStartValue(0.0)
        self._opacity_anim.setEndValue(1.0)
        self._opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._pos_anim = QPropertyAnimation(page, b"pos")
        self._pos_anim.setDuration(250)
        self._pos_anim.setStartValue(QPoint(0, 20))
        self._pos_anim.setEndValue(QPoint(0, 0))
        self._pos_anim.setEasingCurve(QEasingCurve.Type.OutExpo)

        self._opacity_anim.start()
        self._pos_anim.start()

        self._opacity_anim.finished.connect(lambda: page.setGraphicsEffect(None))

    def _update_footer_height(self):
        count = self._footer_items_list.count()
        
        height = 0
        for i in range(count):
            height += self._footer_items_list.sizeHintForRow(i)

        self._footer_items_list.setFixedHeight(height)