from typing import Optional
from PyQt6.QtWidgets import QWidget
from poppy.ui import LabeledSwitchTr
from poppy.ui.fluent import CardExpand, Switch


class CardExpandAuto(CardExpand):
    def __init__(self, header: Optional[QWidget | str] = None):
        self._switch = Switch()
        super().__init__(header, LabeledSwitchTr(self._switch))

        self._switch.setChecked(False)
        self._on_switch_toggled(False)
        
        self._switch.toggled.connect(self._on_switch_toggled)

    def switch(self) -> Switch:
        return self._switch
    
    def _on_switch_toggled(self, checked: bool):
        self.setExpanded(checked)
        self.setExpandedContentEnabled(checked)