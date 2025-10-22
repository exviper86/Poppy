# sound_manager.py

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect
from utils import get_resource_path

class SoundManager:
    def __init__(self, config):
        self.config = config
        self.effect = None

        self.effect = QSoundEffect()
        self.set_sound(self.config.sound_type)
        self.effect.setVolume(1)

    def play_sound(self):
        if self.config.sound:
            self.effect.play()
    
    def set_sound(self, sound_type):
        sound_path = get_resource_path(f'sounds/click{sound_type + 1}.wav')
        self.effect.setSource(QUrl.fromLocalFile(sound_path))