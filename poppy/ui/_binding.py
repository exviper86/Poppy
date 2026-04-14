from abc import ABC
from typing import Union
from PyQt6.QtWidgets import QSlider, QSpinBox, QCheckBox, QTextEdit, QComboBox, QLineEdit
from poppy.config_options import ConfigOptionInt, ConfigOptionBool, ConfigOptionStr
from poppy.ui import PositionGrid
from poppy.ui.fluent import Toggle

IntWidgetParameter = Union[QSlider, QSpinBox, QComboBox] 
BoolWidgetParameter = Union[QCheckBox, Toggle]
StrWidgetParameter = Union[QTextEdit, QLineEdit]

class Binding(ABC):
    @staticmethod
    def int(widget: IntWidgetParameter, config_option: ConfigOptionInt):
        if isinstance(widget, QComboBox):
            widget.setCurrentIndex(config_option.value)
            widget.currentIndexChanged.connect(config_option.save)
        else:
            widget.setValue(config_option.value)
            widget.valueChanged.connect(config_option.save)

    @staticmethod
    def bool(widget: BoolWidgetParameter, config_option: ConfigOptionBool):
        widget.setChecked(config_option.value)
        widget.toggled.connect(config_option.save)

    @staticmethod
    def str(widget: StrWidgetParameter, config_option: ConfigOptionStr):
        widget.setText(config_option.value)
        widget.textChanged.connect(config_option.save)

    @staticmethod
    def position(widget: PositionGrid, config_option: ConfigOptionStr):
        widget.setPosition(config_option.value)
        widget.positionChanged.connect(config_option.save)
        