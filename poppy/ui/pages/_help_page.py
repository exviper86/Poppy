from PyQt6.QtWidgets import QVBoxLayout, QWidget
from poppy.ui.fluent import Label, Font, Card
from ._base_page import BasePage
from poppy.translations import localizer as loc, translations as trans

class Section(QWidget):
    def __init__(self, title_key: str, content_key: str):
        super().__init__()
        
        self._title_key = title_key
        self._content_key = content_key
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self._title = Label("", Font.subTitle())
        self._title.setContentsMargins(4, 8, 8, 8)
        layout.addWidget(self._title)
        
        self._content = Label()
        self._content.setContentsMargins(0, 10, 0, 10)
        self._content.setWordWrap(True)
        layout.addWidget(Card(self._content))
        
        self.update_text()

    def update_text(self):
        self._title.setText(loc.tr(self._title_key))
        self._content.setText(loc.tr(self._content_key))

class HelpPage(BasePage):
    def __init__(self):
        super().__init__()

    def _create_content(self, layout: QVBoxLayout):
        # Вводный текст
        self.intro_label = Label()
        self.intro_label.setWordWrap(True)
        #self.intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intro_label.setContentsMargins(0, 0, 0, 10)
        layout.addWidget(self.intro_label)

        # Создаём секции
        self.sections = [
            Section(trans.help_keyboard_title, trans.help_keyboard),
            Section(trans.help_volume_title, trans.help_volume),
            Section(trans.help_media_title, trans.help_media),
            Section(trans.help_audio_switch_title, trans.help_audio_switch),
            Section(trans.help_layout_switch_title, trans.help_layout_switch),
            Section(trans.help_tips_title, trans.help_tips),
        ]

        for section in self.sections:
            layout.addWidget(section)

    def _update_text(self):
        self.intro_label.setText(loc.tr(trans.help_intro))
        for section in self.sections:
            section.update_text()
        