from PyQt6.QtWidgets import QHBoxLayout, QPushButton
from poppy.ui import HotkeyEdit
from poppy.ui.fluent import Widget, Card, Label
from poppy.translations import localizer as loc, translations as trans


class HotkeyCard(Card):
    def __init__(self):
        self._label = Label("Сочетание клавиш")
        
        hotkey_layout = QHBoxLayout()
        hotkey_layout.setContentsMargins(0, 0, 0, 0)
        hotkey_layout.setSpacing(8)

        self._hotkey_edit = HotkeyEdit("нажмите...")
        hotkey_layout.addWidget(self._hotkey_edit, stretch=True)

        self._clear_btn = QPushButton()
        self._clear_btn.setText("Cбросить")
        self._clear_btn.setFixedHeight(31)
        self._clear_btn.clicked.connect(self._hotkey_edit.clear)
        hotkey_layout.addWidget(self._clear_btn)

        hotkey_widget = Widget()
        hotkey_widget.setLayout(hotkey_layout)
    
        super().__init__(self._label, hotkey_widget)
        
        self._update_text()
        loc.language_changed.connect(self._update_text)

        self.destroyed.connect(lambda: loc.language_changed.disconnect(self._update_text))
    
    def hotkeyEdit(self) -> HotkeyEdit:
        return self._hotkey_edit
    
    def _update_text(self):
        self._label.setText(loc.tr(trans.hotkey_label))
        self._hotkey_edit.setPlaceholderText(loc.tr(trans.hotkey_placeholder))
        self._clear_btn.setText(loc.tr(trans.clear_btn))
        