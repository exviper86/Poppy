from typing import Optional
from poppy.ui.fluent import LabeledSwitch, Switch
from poppy.translations import localizer as loc, translations as trans

class LabeledSwitchTr(LabeledSwitch):
    def __init__(self, switch: Optional[Switch] = None):
        super().__init__(switch)

        self._update_text()
        loc.language_changed.connect(self._update_text)

        self.destroyed.connect(lambda: loc.language_changed.disconnect(self._update_text))
        
    def _update_text(self):
        if self.switch() is not None:
            self.setTexts(loc.tr(trans.on), loc.tr(trans.off))