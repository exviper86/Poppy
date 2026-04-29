from typing import Iterable
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from poppy.ui.fluent import Page, Switch, CardExpand
from abc import abstractmethod
from poppy.translations import localizer as loc


class BasePage(Page):
    def __init__(self):
        super().__init__()

        self._linked_switches: dict[Switch, list[QWidget]] = {}
          
        self._slider_width = 150
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        
        self._create_content(layout)

        layout.addStretch()
        layout.addSpacing(16)
        
        self._bind()

        for switch, widgets in self._linked_switches.items():
            initial_state = switch.isChecked()
            for widget in widgets:
                widget.setEnabled(initial_state)
                switch.toggled.connect(widget.setEnabled)
        
        self._update_text()
        loc.language_changed.connect(self._update_text)
        
        self.destroyed.connect(lambda: loc.language_changed.disconnect(self._update_text))
    
    @property
    def slider_width(self) -> int:
        return self._slider_width
    
    @abstractmethod
    def _create_content(self, layout: QVBoxLayout):
        pass
    
    @abstractmethod
    def _bind(self):
        pass

    @abstractmethod
    def _update_text(self):
        pass

    def link_switch(self, switch: Switch, widgets: QWidget | Iterable[QWidget]):
        if isinstance(widgets, QWidget):
            widgets = [widgets]
        self._linked_switches[switch] = list(widgets)