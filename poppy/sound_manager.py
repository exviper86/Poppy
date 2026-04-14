from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtMultimedia import QSoundEffect, QMediaPlayer
from .config import config
from .utils import Utils

class SoundManager:
    def __init__(self):
        self._effect = QSoundEffect()
        self._set_sound(config.keyboard_window.sound_type.value)
        self._effect.setVolume(1)
        
        config.keyboard_window.sound_type.valueChanged.connect(self._set_sound)
        config.keyboard_window.sound_type.valueChanged.connect(lambda: QTimer.singleShot(20, self.play_sound))

    def play_sound(self):
        if config.keyboard_window.sound.value:
            self._effect.play()
    
    def _set_sound(self, sound_type: int):
        sound_path = Utils.get_resource_path(f'sounds/click{sound_type + 1}.wav')
        self._effect.setSource(QUrl.fromLocalFile(sound_path))