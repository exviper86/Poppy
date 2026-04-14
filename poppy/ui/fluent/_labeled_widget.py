from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Optional, Any
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSlider
from ._label import Label
from ._switch import Switch

TValue = TypeVar('TValue')

class BaseLabeledWidget(QWidget, Generic[TValue]):
    def __init__(self, widget: TValue, value_format: str = "{}"):
        super().__init__()

        self._label = Label()
        self._widget: TValue = widget

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(12)
        self._layout.addStretch()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._widget)

        self._value_format = value_format
        self._value_processor: Optional[Callable[[Any], str]] = None
        self._update_label()

    def widget(self) -> TValue:
        return self._widget

    def valueFormat(self) -> str:
        return self._value_format

    def setValueFormat(self, value_format: str):
        self._value_format = value_format
        self._update_label()
    
    def valueProcessor(self) -> Callable[[Any], str]:
        return self._value_processor
    
    def setValueProcessor(self, value_processor: Callable[[Any], str]):
        self._value_processor = value_processor
        self._update_label()
    
    @abstractmethod
    def _value_getter(self) -> object:
        pass

    def _update_label(self):
        try:
            value = self._value_getter()
            if self._value_processor is not None:
                value = self._value_processor(value)
            text = self._value_format.format(value)
            self._label.setText(text)
        except Exception as e:
            self._label.setText("???")

class LabeledSlider(BaseLabeledWidget[QSlider]):
    def __init__(self, slider: QSlider | None = None, value_format: str = "{}"):
        if slider is None:
            slider = QSlider()
            slider.setOrientation(Qt.Orientation.Horizontal)
        self._slider = slider
        
        super().__init__(self._slider, value_format)

        self._slider.valueChanged.connect(self._update_label)
        
    def _value_getter(self) -> int:
        return self._slider.value()
    
    def slider(self) -> QSlider:
        return self._slider

class LabeledSwitch(BaseLabeledWidget[Switch]):
    def __init__(self, switch: Switch | None = None, checked_text: str = "On", unchecked_text: str = "Off"):
        if switch is None:
            switch = Switch()
        self._switch = switch

        self._checked_text = checked_text
        self._unchecked_text = unchecked_text
        
        super().__init__(self._switch)
        
        self._switch.toggled.connect(self._update_label)

    def _value_getter(self) -> str:
        return self._checked_text if self._switch.isChecked() else self._unchecked_text
    
    def switch(self) -> Switch:
        return self._switch
        
    def checkedText(self) -> str:
        return self._checked_text
    
    def setCheckedText(self, checked_text: str):
        self._checked_text = checked_text
        self._update_label()

    def uncheckedText(self) -> str:
        return self._unchecked_text

    def setUncheckedText(self, unchecked_text: str):
        self._unchecked_text = unchecked_text
        self._update_label()
        
    def setTexts(self, checked_text: str, unchecked_text: str):
        self._checked_text = checked_text
        self._unchecked_text = unchecked_text
        self._update_label()
        