from PyQt6.QtCore import QSize
from poppy.config import config
from poppy.ui import StepSlider, PositionGrid, LabeledSwitchTr, Binding
from poppy.ui.fluent import Label, Card, LabeledSlider
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from poppy.translations import localizer as loc, translations as trans
from ._base_page import BasePage

class VolumePage(BasePage):
    def __init__(self):
        super().__init__()

    def _create_content(self, layout: QVBoxLayout):
        enable_layout = QHBoxLayout()
        enable_layout.setContentsMargins(0, 0, 0, 0)
        enable_layout.setSpacing(8)

        self._enable_label = Label("Показывать окно громкости")
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

        self._show_media_label = Label("Показывать окно мультимедиа")
        self._show_media_labeled = LabeledSwitchTr()
        self._show_media_card = Card(self._show_media_label, self._show_media_labeled)
        content_layout.addWidget(self._show_media_card)

        self._step_label = Label("Шаг громкости клавишами")
        self._step_slider = StepSlider()
        self._step_slider.setRange(1, 10)
        self._step_slider.setFixedWidth(self.slider_width)
        labeled_step = LabeledSlider(self._step_slider)
        self._step_card = Card(self._step_label, labeled_step)
        content_layout.addWidget(self._step_card)

        self._show_name_label = Label("Показывать имя аудио устройства")
        self._show_name_labeled = LabeledSwitchTr()
        self._show_name_card = Card(self._show_name_label, self._show_name_labeled)
        content_layout.addWidget(self._show_name_card)

        self._full_name_label = Label("Полное имя устройства")
        self._full_name_labeled = LabeledSwitchTr()
        self._full_name_card = Card(self._full_name_label, self._full_name_labeled)
        self._full_name_card.setIdent(1)
        content_layout.addWidget(self._full_name_card)

        self._override_duration_label = Label("Переопределить длительность отображения")
        self._override_duration_labeled = LabeledSwitchTr()
        self._override_duration_card = Card(
            self._override_duration_label,
            self._override_duration_labeled
        )
        content_layout.addWidget(self._override_duration_card)

        self._duration_label = Label("Длительность отображения")
        self._duration_slider = StepSlider(100)
        self._duration_slider.setRange(500, 5000)
        self._duration_slider.setFixedWidth(self.slider_width)
        self._labeled_duration = LabeledSlider(self._duration_slider, "{} с")
        self._labeled_duration.setValueProcessor(lambda v: v / 1000)
        self._duration_card = Card(self._duration_label, self._labeled_duration)
        self._duration_card.setIdent(1)
        content_layout.addWidget(self._duration_card)

        self.link_switch(self._enable_labeled.switch(), [self._content, self._position_grid])
        self.link_switch(self._show_name_labeled.switch(), self._full_name_card)
        self.link_switch(self._override_duration_labeled.switch(), self._duration_card)

    def _bind(self):
        Binding.position(self._position_grid, config.volume_window.position)
        Binding.bool(self._enable_labeled.switch(), config.volume_window.enable)
        Binding.bool(self._show_media_labeled.switch(), config.volume_window.show_media)
        Binding.int(self._step_slider, config.volume_window.step)
        Binding.bool(self._show_name_labeled.switch(), config.volume_window.show_name)
        Binding.bool(self._full_name_labeled.switch(), config.volume_window.full_name)
        Binding.bool(self._override_duration_labeled.switch(), config.volume_window.override_duration)
        Binding.int(self._duration_slider, config.volume_window.duration)

    def _update_text(self):
        self._enable_label.setText(loc.tr(trans.volume_enable))
        self._show_media_label.setText(loc.tr(trans.volume_show_media))
        self._step_label.setText(loc.tr(trans.volume_step))
        self._show_name_label.setText(loc.tr(trans.volume_show_name))
        self._full_name_label.setText(loc.tr(trans.volume_full_name))
        self._override_duration_label.setText(loc.tr(trans.override_duration))
        self._duration_label.setText(loc.tr(trans.duration_label))

        self._labeled_duration.setValueFormat(f"{{}} {loc.tr(trans.s_suffix)}")
