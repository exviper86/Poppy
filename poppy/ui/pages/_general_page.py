from poppy.config import config
from poppy.ui import StepSlider, LabeledSwitchTr, Binding
from poppy.ui.fluent import Label, Card, LabeledSlider
from PyQt6.QtWidgets import QComboBox, QVBoxLayout
from poppy.translations import localizer as loc, translations as trans
from ._base_page import BasePage


class GeneralPage(BasePage):
    def __init__(self):
        super().__init__()

    def _create_content(self, layout: QVBoxLayout):
        self._duration_label = Label("Длительность отображения")
        self._duration_slider = StepSlider(100)
        self._duration_slider.setRange(500, 5000)
        self._duration_slider.setFixedWidth(self.slider_width)
        self._labeled_duration = LabeledSlider(self._duration_slider, "{} с")
        self._labeled_duration.setValueProcessor(lambda v: v / 1000)
        duration_card = Card(self._duration_label, self._labeled_duration)
        layout.addWidget(duration_card)

        self._transparency_label = Label("Непрозрачность окна")
        self._transparency_slider = StepSlider(5)
        self._transparency_slider.setRange(10, 100)
        self._transparency_slider.setFixedWidth(self.slider_width)
        self._labeled_transparency = LabeledSlider(self._transparency_slider, "{} %")
        transparency_card = Card(self._transparency_label, self._labeled_transparency)
        layout.addWidget(transparency_card)
        
        self._show_duration_label = Label("Время появления окна")
        self._show_duration_slider = StepSlider(10)
        self._show_duration_slider.setRange(50, 200)
        self._show_duration_slider.setFixedWidth(self.slider_width)
        self._labeled_show_duration = LabeledSlider(self._show_duration_slider, "{} мс")
        duration_card = Card(self._show_duration_label, self._labeled_show_duration)
        layout.addWidget(duration_card)

        self._animation_label = Label("Анимация появления")
        self._animation_labeled = LabeledSwitchTr()
        animation_card = Card(self._animation_label, self._animation_labeled)
        layout.addWidget(animation_card)

        self._taskbar_label = Label("Учитывать панель задач")
        self._taskbar_labeled = LabeledSwitchTr()
        taskbar_card = Card(self._taskbar_label, self._taskbar_labeled)
        layout.addWidget(taskbar_card)

        self._autostart_label = Label("Запускать при старте системы")
        self._autostart_labeled = LabeledSwitchTr()
        autostart_card = Card(self._autostart_label, self._autostart_labeled)
        layout.addWidget(autostart_card)

        self._language_label = Label("Язык приложения")
        self._language_combo = QComboBox()
        for key, value in trans.languages.items():
            self._language_combo.addItem(value, key)
        language_card = Card(self._language_label, self._language_combo)
        layout.addWidget(language_card)
        
    def _bind(self):
        Binding.int(self._duration_slider, config.common.popup_duration)
        Binding.int(self._transparency_slider, config.common.popup_transparency)
        Binding.int(self._show_duration_slider, config.common.popup_show_duration)
        Binding.bool(self._animation_labeled.switch(), config.common.animation)
        Binding.bool(self._taskbar_labeled.switch(), config.common.taskbar)
        Binding.bool(self._autostart_labeled.switch(), config.common.autostart)
        
        self._language_combo.setCurrentText(trans.languages.get(config.common.language.value))
        self._language_combo.currentIndexChanged.connect(self._on_language_changed)
    
    def _update_text(self):
        self._duration_label.setText(loc.tr(trans.duration_label))
        self._transparency_label.setText(loc.tr(trans.transparency_label))
        self._show_duration_label.setText(loc.tr(trans.show_duration_label))
        self._animation_label.setText(loc.tr(trans.animation_label))
        self._taskbar_label.setText(loc.tr(trans.taskbar_label))
        self._autostart_label.setText(loc.tr(trans.autostart_label))
        self._language_label.setText(loc.tr(trans.app_language_label))

        self._labeled_duration.setValueFormat(f"{{}} {loc.tr(trans.s_suffix)}")
        self._labeled_show_duration.setValueFormat(f"{{}} {loc.tr(trans.ms_suffix)}")

    def _on_language_changed(self, index: int):
        lang = self._language_combo.itemData(index)
        config.common.language.save(lang)
        loc.set_language(lang)
        