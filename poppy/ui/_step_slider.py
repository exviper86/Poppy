from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QSlider

class StepSlider(QSlider):
    valueChanged = pyqtSignal(int)
    
    def __init__(self, step: int = 1, orientation: Qt.Orientation = Qt.Orientation.Horizontal):
        super().__init__()

        self._step = step
        self.setStep(step)
        self.setOrientation(orientation)
        
        self._last_value: int = self.value()
        self._updating = False
    
    def sliderChange(self, change):
        if change != QSlider.SliderChange.SliderValueChange or self._updating:
            super().sliderChange(change)
            return 
            
        value = self.value()
        if self._last_value == value:
            return

        self._updating = True
        self.setValue(value)
        self.valueChanged.emit(value)
        self._last_value = value
        self._updating = False

        super().sliderChange(change)
    
    def value(self):
        return round(super().value() / self._step) * self._step
    
    def setStep(self, step: int):
        self._step = step
        self.setSingleStep(step)
        self.setPageStep(step)
            