from PyQt6.QtCore import QSize
from poppy.config import config
from poppy.ui import StepSlider, PositionGrid, LabeledSwitchTr, Binding
from poppy.ui.fluent import Label, Card, LabeledSlider
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from poppy.translations import localizer as loc, translations as trans
from ._base_page import BasePage

class MultimediaPage(BasePage):
    def __init__(self):
        super().__init__()

    def _create_content(self, layout: QVBoxLayout):
        enable_layout = QHBoxLayout()
        enable_layout.setContentsMargins(0, 0, 0, 0)
        enable_layout.setSpacing(8)

        self._enable_label = Label("Показывать окно мультимедиа")
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

        self._show_volume_label = Label("Показывать окно громкости")
        self._show_volume_labeled = LabeledSwitchTr()
        self._show_volume_card = Card(self._show_volume_label, self._show_volume_labeled)
        content_layout.addWidget(self._show_volume_card)

        self._show_on_change_label = Label("Показывать при смене трека")
        self._show_on_change_labeled = LabeledSwitchTr()
        self._show_on_change_card = Card(self._show_on_change_label, self._show_on_change_labeled)
        content_layout.addWidget(self._show_on_change_card)

        self._show_timeline_label = Label("Прогресс трека")
        self._show_timeline_labeled = LabeledSwitchTr()
        self._show_timeline_card = Card(self._show_timeline_label, self._show_timeline_labeled)
        content_layout.addWidget(self._show_timeline_card)

        self._color_by_cover_label = Label("Окно в цвет обложки")
        self._color_by_cover_labeled = LabeledSwitchTr()
        self._color_by_cover_card = Card(self._color_by_cover_label, self._color_by_cover_labeled)
        content_layout.addWidget(self._color_by_cover_card)

        self._override_duration_label = Label("Переопределить длительность отображения")
        self._override_duration_labeled = LabeledSwitchTr()
        self._override_duration_card = Card(self._override_duration_label, self._override_duration_labeled)
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
        self.link_switch(self._override_duration_labeled.switch(), self._duration_card)

    def _bind(self):
        Binding.position(self._position_grid, config.media_window.position)
        Binding.bool(self._enable_labeled.switch(), config.media_window.enable)
        Binding.bool(self._show_volume_labeled.switch(), config.media_window.show_volume)
        Binding.bool(self._show_on_change_labeled.switch(), config.media_window.show_on_change)
        Binding.bool(self._show_timeline_labeled.switch(), config.media_window.show_timeline)
        Binding.bool(self._color_by_cover_labeled.switch(), config.media_window.color_by_cover)
        Binding.bool(self._override_duration_labeled.switch(), config.media_window.override_duration)
        Binding.int(self._duration_slider, config.media_window.duration)

    def _update_text(self):
        self._enable_label.setText(loc.tr(trans.media_enable))
        self._show_volume_label.setText(loc.tr(trans.media_show_volume))
        self._show_on_change_label.setText(loc.tr(trans.media_show_on_change))
        self._show_timeline_label.setText(loc.tr(trans.media_show_timeline))
        self._color_by_cover_label.setText(loc.tr(trans.media_color_by_cover))
        self._override_duration_label.setText(loc.tr(trans.override_duration))
        self._duration_label.setText(loc.tr(trans.duration_label))

        self._labeled_duration.setValueFormat(f"{{}} {loc.tr(trans.s_suffix)}")