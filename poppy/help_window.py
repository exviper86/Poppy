# help_window.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QToolButton, QFrame, QLabel, QScrollArea, QWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont
from utils import get_windows_theme
from translations import localizer as loc, translations as trans


class CollapsibleSection(QWidget):
    def __init__(self, title_key: str, content_key: str, parent=None):
        super().__init__(parent)
        self.title_key = title_key
        self.content_key = content_key

        self.toggle_button = QToolButton()
        self.toggle_button.setIconSize(QSize(12, 12))
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)

        self.toggle_text = QLabel("Заголовок")
        self.toggle_text.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))

        toggle_layout = QHBoxLayout()
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(8)
        toggle_layout.addWidget(self.toggle_button)
        toggle_layout.addWidget(self.toggle_text)

        self.content_frame = QFrame()
        self.content_frame.setFrameShape(QFrame.Shape.StyledPanel)
        #self.content_frame.setContentsMargins(10, 10, 10, 10)

        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        self.content_label.setFont(QFont("Segoe UI", 10))
        self.content_label.setTextFormat(Qt.TextFormat.PlainText)
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.addWidget(self.content_label)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        main_layout.addLayout(toggle_layout)
        main_layout.addWidget(self.content_frame)

        self.toggle_button.toggled.connect(self._on_toggled)
        self._on_toggled(True)
        
        self.update_text()

    def showEvent(self, a0):
        super().showEvent(a0)
        
        theme = get_windows_theme()
        self.toggle_button.setStyleSheet(f"QToolButton {{ border: none; color: {'#fff' if theme == 'dark' else '#000'}; }}")

    def _on_toggled(self, checked):
        self.content_frame.setVisible(checked)
        self.toggle_button.setArrowType(
            Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow
        )

    def update_text(self):
        self.toggle_text.setText(loc.tr(self.title_key))
        self.content_label.setText(loc.tr(self.content_key))


class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справка")
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(600, 800)
        self._init_ui()
        
        self._update_text()
        loc.language_changed.connect(self._update_text)

    def _init_ui(self):
        main_layout = QVBoxLayout()

        # Вводный текст
        self.intro_label = QLabel()
        self.intro_label.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        self.intro_label.setWordWrap(True)
        self.intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intro_label.setContentsMargins(0, 0, 0, 10)
        main_layout.addWidget(self.intro_label)

        # Прокручиваемая область для секций
        scroll_area = QScrollArea()
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        self.sections_layout = QVBoxLayout(content_widget)
        self.sections_layout.setSpacing(8)

        # Создаём секции
        self.sections = [
            CollapsibleSection(trans.help_keyboard_title, trans.help_keyboard),
            CollapsibleSection(trans.help_volume_title, trans.help_volume),
            CollapsibleSection(trans.help_media_title, trans.help_media),
            CollapsibleSection(trans.help_audio_switch_title, trans.help_audio_switch),
            CollapsibleSection(trans.help_tips_title, trans.help_tips),
        ]

        for section in self.sections:
            self.sections_layout.addWidget(section)

        self.sections_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Подсказка
        # tip_label = QLabel("Нажмите на заголовок, чтобы свернуть/развернуть раздел", self)
        # tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # tip_label.setStyleSheet("color: gray; font-size: 10px; margin-top: 6px;")
        # main_layout.addWidget(tip_label)

        self.setLayout(main_layout)

    def _update_text(self):
        self.setWindowTitle(loc.tr(trans.help_title))
        self.intro_label.setText(loc.tr(trans.help_intro))
        for section in self.sections:
            section.update_text()