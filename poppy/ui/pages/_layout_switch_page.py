from PyQt6.QtWidgets import QVBoxLayout
from ._base_page import BasePage
from poppy.ui import LabeledSwitchTr, HotkeyCard, Binding
from poppy.config import config
from poppy.ui.fluent import Label, Card
from poppy.translations import localizer as loc, translations as trans


class LayoutSwitchPage(BasePage):
    def __init__(self):
        super().__init__()

    def _create_content(self, layout: QVBoxLayout):
        
        self._last_hotkey_label = Label("Смена последнего слова")
        self._last_hotkey_labeled = LabeledSwitchTr()
        self._last_hotkey_card = Card(self._last_hotkey_label, self._last_hotkey_labeled)
        layout.addWidget(self._last_hotkey_card)
        
        self._last_hotkey_value_card = HotkeyCard()
        self._last_hotkey_value_card.setIdent(1)
        layout.addWidget(self._last_hotkey_value_card)

        self._consider_space_label = Label("Учитывать пробелы")
        self._consider_space_labeled = LabeledSwitchTr()
        self._consider_space_card = Card(self._consider_space_label, self._consider_space_labeled)
        self._consider_space_card.setIdent(1)
        layout.addWidget(self._consider_space_card)
        
        self._change_language_label = Label("Переключать раскладку, если нет последнего слова")
        self._change_language_labeled = LabeledSwitchTr()
        self._change_language_card = Card(self._change_language_label, self._change_language_labeled)
        self._change_language_card.setIdent(1)
        layout.addWidget(self._change_language_card)

        self._selected_hotkey_label = Label("Смена выделенного текста")
        self._selected_hotkey_labeled = LabeledSwitchTr()
        self._selected_hotkey_card = Card(self._selected_hotkey_label, self._selected_hotkey_labeled)
        layout.addWidget(self._selected_hotkey_card)
    
        self._selected_hotkey_value_card = HotkeyCard()
        self._selected_hotkey_value_card.setIdent(1)
        layout.addWidget(self._selected_hotkey_value_card)

        self._case_hotkey_label = Label("Смена выделенного текста")
        self._case_hotkey_labeled = LabeledSwitchTr()
        self._case_hotkey_card = Card(self._case_hotkey_label, self._case_hotkey_labeled)
        layout.addWidget(self._case_hotkey_card)

        self._case_hotkey_value_card = HotkeyCard()
        self._case_hotkey_value_card.setIdent(1)
        layout.addWidget(self._case_hotkey_value_card)

        # self._block_locks_label = Label("Не передавать системе Caps, Lock, Num Lock и Insert в сочетаниях клавиш")
        # self._block_locks_labeled = LabeledSwitchTr()
        # self._block_lock_card = Card(self._block_locks_label, self._block_locks_labeled)
        # layout.addWidget(self._block_lock_card)
        
        self.link_switch(self._last_hotkey_labeled.switch(), [self._last_hotkey_value_card, self._consider_space_card, self._change_language_card])
        self.link_switch(self._selected_hotkey_labeled.switch(), self._selected_hotkey_value_card)
        self.link_switch(self._case_hotkey_labeled.switch(), self._case_hotkey_value_card)

    def _bind(self):
        Binding.str(self._last_hotkey_value_card.hotkeyEdit(), config.layout_switch.last_hotkey)
        Binding.bool(self._consider_space_labeled.switch(), config.layout_switch.consider_spaces)
        Binding.bool(self._last_hotkey_labeled.switch(), config.layout_switch.last)
        Binding.bool(self._change_language_labeled.switch(), config.layout_switch.no_last_switch)
        Binding.bool(self._selected_hotkey_labeled.switch(), config.layout_switch.selected)
        Binding.str(self._selected_hotkey_value_card.hotkeyEdit(), config.layout_switch.selected_hotkey)
        Binding.bool(self._case_hotkey_labeled.switch(), config.layout_switch.case)
        Binding.str(self._case_hotkey_value_card.hotkeyEdit(), config.layout_switch.case_hotkey)
        #Binding.bool(self._block_locks_labeled.switch(), config.layout_switch.block_locks)


    def _update_text(self):
        self._last_hotkey_label.setText(loc.tr(trans.layout_switch_last))
        self._consider_space_label.setText(loc.tr(trans.layout_switch_spaces))
        self._change_language_label.setText(loc.tr(trans.layout_switch_if_no_last))
        self._selected_hotkey_label.setText(loc.tr(trans.layout_switch_selected))
        self._case_hotkey_label.setText(loc.tr(trans.layout_switch_case))
        #self._block_locks_label.setText(loc.tr(trans.layout_switch_block_locks))
