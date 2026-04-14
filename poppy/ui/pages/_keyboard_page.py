from PyQt6.QtCore import QSize
from poppy.config import config
from poppy.ui import StepSlider, PositionGrid, LabeledSwitchTr
from poppy.ui.fluent import Label, Card, LabeledSlider
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QComboBox
from poppy.translations import localizer as loc, translations as trans
from ._base_page import BasePage
from poppy.ui import Binding 

class KeyboardPage(BasePage):
    def __init__(self):
        super().__init__()
    
    def _create_content(self, layout: QVBoxLayout):
        enable_layout = QHBoxLayout()
        enable_layout.setContentsMargins(0, 0, 0, 0)
        enable_layout.setSpacing(8)
        
        self._enable_label = Label("Показывать окно клавиатуры")
        self._enable_labeled = LabeledSwitchTr()
        enable_card = Card(self._enable_label, self._enable_labeled)
        enable_layout.addWidget(enable_card)
        self._position_grid = PositionGrid()
        self._position_grid.setFixedSize(QSize(120, 80))
        enable_layout.addWidget(self._position_grid)
        layout.addLayout(enable_layout)
        
        layout.addSpacing(5)

        self._content = QWidget()
        content_layout = QVBoxLayout(self._content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(3)
        layout.addWidget(self._content)
        
        self._show_language_label = Label("Показывать при смене языка")
        self._show_language_labeled = LabeledSwitchTr()
        self._show_language_card = Card(self._show_language_label, self._show_language_labeled)
        content_layout.addWidget(self._show_language_card)

        self._show_cursor_label = Label("Окно смены языка рядом с курсором")
        self._show_cursor_labeled = LabeledSwitchTr()
        self._show_cursor_card = Card(self._show_cursor_label, self._show_cursor_labeled)
        self._show_cursor_card.setIdent(1)
        content_layout.addWidget(self._show_cursor_card)

        self._show_modifiers_label = Label("Показывать при нажатии клавиш режима")
        self._show_modifiers_labeled = LabeledSwitchTr()
        self._show_modifiers_card = Card(self._show_modifiers_label, self._show_modifiers_labeled)
        content_layout.addWidget(self._show_modifiers_card)

        self._sound_label = Label("Звуковой эффект при показе")
        self._sound_labeled = LabeledSwitchTr()
        self._sound_card = Card(self._sound_label, self._sound_labeled)
        content_layout.addWidget(self._sound_card)

        self._sound_type_label = Label("Тип звука")
        self._sound_type_combo = QComboBox()
        self._sound_type_combo.addItems(["звук 1", "звук 2", "звук 3", "звук 4", "звук 5", "звук 6"])
        self._sound_type_card = Card(self._sound_type_label, self._sound_type_combo)
        self._sound_type_card.setIdent(1)
        content_layout.addWidget(self._sound_type_card)

        self._override_duration_label = Label("Переопределить длительность отображения" )
        self._override_duration_labeled = LabeledSwitchTr()
        self._override_duration_card = Card(self._override_duration_label, self._override_duration_labeled)
        content_layout.addWidget(self._override_duration_card)

        self._duration_label = Label("Длительность отображения")
        self._duration_slider = StepSlider(100)
        self._duration_slider.setRange(500, 5000)
        self._duration_slider.setFixedWidth(self.slider_width)
        self._duration_labeled = LabeledSlider(self._duration_slider, "{} с")
        self._duration_labeled.setValueProcessor(lambda v: v / 1000)
        self._duration_card = Card(self._duration_label, self._duration_labeled)
        self._duration_card.setIdent(1)
        content_layout.addWidget(self._duration_card)

        self.link_switch(self._enable_labeled.switch(), [self._content, self._position_grid])
        self.link_switch(self._show_language_labeled.switch(), self._show_cursor_card)
        self.link_switch(self._sound_labeled.switch(), self._sound_type_card)
        self.link_switch(self._override_duration_labeled.switch(), self._duration_card)
    
    def _bind(self):
        Binding.position(self._position_grid, config.keyboard_window.position)
        Binding.bool(self._enable_labeled.switch(), config.keyboard_window.enable)
        Binding.bool(self._show_language_labeled.switch(), config.keyboard_window.show_language)
        Binding.bool(self._show_cursor_labeled.switch(), config.keyboard_window.show_cursor)
        Binding.bool(self._show_modifiers_labeled.switch(), config.keyboard_window.show_modifiers)
        Binding.bool(self._sound_labeled.switch(), config.keyboard_window.sound)
        Binding.int(self._sound_type_combo, config.keyboard_window.sound_type)
        Binding.bool(self._override_duration_labeled.switch(), config.keyboard_window.override_duration)
        Binding.int(self._duration_slider, config.keyboard_window.duration)

    def _update_text(self):
        self._enable_label.setText(loc.tr(trans.keyboard_enable))
        self._show_language_label.setText(loc.tr(trans.keyboard_show_language))
        self._show_cursor_label.setText(loc.tr(trans.keyboard_show_cursor))
        self._show_modifiers_label.setText(loc.tr(trans.keyboard_show_modifiers))
        self._sound_label.setText(loc.tr(trans.sound_enable))
        self._sound_type_label.setText(loc.tr(trans.sound_type))
        self._override_duration_label.setText(loc.tr(trans.override_duration))
        self._duration_label.setText(loc.tr(trans.duration_label))

        self._duration_labeled.setValueFormat(f"{{}} {loc.tr(trans.s_suffix)}")

        sound_type = loc.tr(trans.sound_type_cb)
        for i in range(self._sound_type_combo.count()):
            self._sound_type_combo.setItemText(i, f"{sound_type} {i + 1}")
        
        