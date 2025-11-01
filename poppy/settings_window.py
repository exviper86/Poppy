# settings_window.py

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QCheckBox, QLabel, QPushButton, QSpinBox, QFormLayout, QGridLayout, QSizePolicy, QToolButton, QDialog, QComboBox, QStyle, QApplication, QSlider
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from audio_switch_settings_window import AudioSwitchSettingsWindow
from about_window import AboutWindow
from help_window import HelpWindow
from utils import get_windows_theme
from translations import localizer as loc, translations as trans


class PositionGridWidget(QWidget):
    positionChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_button = None
        self.buttons = {}

        # Позиции: 9 точек, включая центр и стороны
        self.positions = {
            "left-top": (0, 0),
            "top": (0, 1),
            "right-top": (0, 2),
            "left": (1, 0),
            "center": (1, 1),
            "right": (1, 2),
            "left-bottom": (2, 0),
            "bottom": (2, 1),
            "right-bottom": (2, 2),
        }

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        for pos_name, (row, col) in self.positions.items():
            btn = QToolButton()
            # Убираем фиксированный размер — пусть растягивается
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, p=pos_name: self._on_button_clicked(p))
            self.buttons[pos_name] = btn
            layout.addWidget(btn, row, col)

        self.setLayout(layout)

        # Важно: делаем виджет компактным по умолчанию
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    def _on_button_clicked(self, position):
        for btn in self.buttons.values():
            btn.setChecked(False)
        self.buttons[position].setChecked(True)
        self.selected_button = position
        self.positionChanged.emit(position)

    def set_position(self, position):
        if position in self.buttons:
            self._on_button_clicked(position)

    def get_position(self):
        return self.selected_button

    def sizeHint(self):
        # Предлагаем компактный размер, например 100x100
        return QSize(100, 100)

    def minimumSizeHint(self):
        return QSize(80, 80)

class SettingsWindow(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("Настройки Poppy")
        self.setMinimumWidth(400)
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        
        self._audio_switch_window = AudioSwitchSettingsWindow(self.app)
        self._about_window = AboutWindow()
        self._help_window = HelpWindow()

        self._position = None
        
        self._init_ui()
        
        self._update_text()
        loc.language_changed.connect(self._update_text)
        
        self._overlay = QWidget(self)
        self._overlay.hide()

    def showEvent(self, a0):
        super().showEvent(a0)
        
        if self._position:
            self.move(self._position)
        else:
            self.move(self.screen().geometry().center() - self.rect().center())

        self.app.qt_app.setStyle(self.app.qt_app.style().objectName())
    
    def closeEvent(self, a0):
        super().closeEvent(a0)
        self._position = self.pos()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._overlay.resize(self.size())
    
    def _init_ui(self):
        layout = QVBoxLayout()

        position_grid_size = QSize(120, 80)

        # === Клавиатура ===
        self.keyboard_group = QGroupBox("КЛАВИАТУРА")
        keyboard_layout = QHBoxLayout()
        #keyboard_layout.setSpacing(5)
        keyboard_left_layout = QVBoxLayout()
        keyboard_right_layout = QVBoxLayout()
        
        self.keyboard_enable_cb = QCheckBox("Показывать окно клавиатуры")
        font = self.keyboard_enable_cb.font()
        font.setBold(True)
        self.keyboard_enable_cb.setFont(font)
        self.keyboard_show_language_cb = QCheckBox("при смене языка")
        self.keyboard_show_cursor_cb = QCheckBox("смена языка рядом с курсором")
        self.keyboard_show_modifiers_cb = QCheckBox("при нажатии клавиш режима")

        sound_layout = QHBoxLayout()
        self.sound_enable_cb = QCheckBox("звуковой эффект:")
        self.sound_type_combo = QComboBox()
        self.sound_type_combo.addItems(["звук 1", "звук 2", "звук 3", "звук 4", "звук 5", "звук 6"])
        sound_layout.addWidget(self.sound_enable_cb)
        sound_layout.addWidget(self.sound_type_combo)
        sound_layout.addStretch()

        keyboard_duration_layout = QHBoxLayout()
        self.keyboard_override_duration_cb = QCheckBox("своя длительность:")
        self.keyboard_duration_spin = QSpinBox()
        self.keyboard_duration_spin.setRange(500, 5000)
        self.keyboard_duration_spin.setSingleStep(100)
        self.keyboard_duration_spin.setSuffix(" мс")
        keyboard_duration_layout.addWidget(self.keyboard_override_duration_cb)
        keyboard_duration_layout.addWidget(self.keyboard_duration_spin)
        keyboard_duration_layout.addStretch()
        
        keyboard_left_layout.addWidget(self.keyboard_enable_cb)
        keyboard_left_layout.addWidget(self.keyboard_show_language_cb)
        keyboard_left_layout.addWidget(self.keyboard_show_cursor_cb)
        keyboard_left_layout.addWidget(self.keyboard_show_modifiers_cb)
        keyboard_left_layout.addLayout(sound_layout)
        keyboard_left_layout.addLayout(keyboard_duration_layout)
        keyboard_left_layout.addStretch()
        
        # Положение — компактная строка
        #keyboard_right_layout.addWidget(QLabel("Позиция:"))
        self.keyboard_position_grid = PositionGridWidget()
        self.keyboard_position_grid.setFixedSize(position_grid_size)
        keyboard_right_layout.addWidget(self.keyboard_position_grid)
        keyboard_right_layout.addStretch()
        
        keyboard_layout.addLayout(keyboard_left_layout)
        keyboard_layout.addLayout(keyboard_right_layout)
        self.keyboard_group.setLayout(keyboard_layout)
        
        
        # === Громкость ===
        self.volume_group = QGroupBox("ГРОМКОСТЬ")
        volume_layout = QHBoxLayout()
        #volume_layout.setSpacing(10)
        volume_left_layout = QVBoxLayout()
        volume_right_layout = QVBoxLayout()
        
        self.volume_enable_cb = QCheckBox("Показывать окно громкости")
        font = self.volume_enable_cb.font()
        font.setBold(True)
        self.volume_enable_cb.setFont(font)
        self.volume_show_media_cb = QCheckBox("+ окно мультимедиа")
        self.volume_step_combo = QComboBox()
        self.volume_step_combo.addItems(["1", "2", "3", "5", "10"])
        self.volume_show_name_cb = QCheckBox("имя аудио устройства")
        self.volume_full_name_cb = QCheckBox("полное имя устройства")

        step_layout = QHBoxLayout()
        step_layout.addWidget(self.volume_step_combo)
        self.volume_step_lb = QLabel("шаг громкости клавишами")
        step_layout.addWidget(self.volume_step_lb)
        step_layout.addStretch()
        
        volume_left_layout.addWidget(self.volume_enable_cb)
        volume_left_layout.addWidget(self.volume_show_media_cb)
        volume_left_layout.addWidget(self.volume_show_name_cb)
        volume_left_layout.addWidget(self.volume_full_name_cb)
        volume_left_layout.addLayout(step_layout)
        volume_left_layout.addStretch()

        #volume_right_layout.addWidget(QLabel("Позиция:"))
        self.volume_position_grid = PositionGridWidget()
        self.volume_position_grid.setFixedSize(position_grid_size)
        volume_right_layout.addWidget(self.volume_position_grid)
        volume_right_layout.addStretch()
        
        volume_layout.addLayout(volume_left_layout)
        volume_layout.addLayout(volume_right_layout)
        self.volume_group.setLayout(volume_layout)
        
        
        # === Мультимедиа ===
        self.media_group = QGroupBox("МУЛЬТИМЕДИА")
        media_layout = QHBoxLayout()
        #media_layout.setSpacing(10)
        media_left_layout = QVBoxLayout()
        media_right_layout = QVBoxLayout()
        
        self.media_enable_cb = QCheckBox("Показывать окно мультимедиа")
        font = self.media_enable_cb.font()
        font.setBold(True)
        self.media_enable_cb.setFont(font)
        self.media_show_volume_cb = QCheckBox("+ окно громкости")
        self.media_show_on_change_cb = QCheckBox("показывать при смене трека")
        self.media_show_timeline_cb = QCheckBox("прогресс трека")
        self.media_color_by_cover_cb = QCheckBox("окно в цвет обложки")

        media_left_layout.addWidget(self.media_enable_cb)
        media_left_layout.addWidget(self.media_show_volume_cb)
        media_left_layout.addWidget(self.media_show_on_change_cb)
        media_left_layout.addWidget(self.media_show_timeline_cb)
        media_left_layout.addWidget(self.media_color_by_cover_cb)
        media_left_layout.addStretch()
        
        #media_right_layout.addWidget(QLabel("Позиция:"))
        self.media_position_grid = PositionGridWidget()
        self.media_position_grid.setFixedSize(position_grid_size)
        media_right_layout.addWidget(self.media_position_grid)
        media_right_layout.addStretch()
        
        media_layout.addLayout(media_left_layout)
        media_layout.addLayout(media_right_layout)
        self.media_group.setLayout(media_layout)

        # === Общие настройки ===
        self.general_group = QGroupBox("ОБЩИЕ")
        general_layout = QVBoxLayout()

        language_layout = QHBoxLayout()
        self.language_lb = QLabel("Язык приложения:")
        language_layout.addWidget(self.language_lb)
        self.language_combo = QComboBox()
        for key, value in trans.languages.items():
            self.language_combo.addItem(value, key)
        self.language_combo.setFixedWidth(position_grid_size.width())
        language_layout.addWidget(self.language_combo)
        general_layout.addLayout(language_layout)
                
        duration_layout = QHBoxLayout()
        self.duration_lb = QLabel("Длительность отображения:")
        duration_layout.addWidget(self.duration_lb)
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(500, 5000)
        self.duration_spin.setSingleStep(100)
        self.duration_spin.setSuffix(" мс")
        self.duration_spin.setFixedWidth(position_grid_size.width())
        duration_layout.addWidget(self.duration_spin)
        general_layout.addLayout(duration_layout)

        transparency_layout = QHBoxLayout()
        self.transparency_lb = QLabel("Непрозрачность окна:")
        transparency_layout.addWidget(self.transparency_lb)
        self.transparency_spin = QSpinBox()
        self.transparency_spin.setRange(50, 100)
        self.transparency_spin.setSingleStep(5)
        self.transparency_spin.setSuffix("%")
        self.transparency_spin.setFixedWidth(position_grid_size.width())
        transparency_layout.addWidget(self.transparency_spin)
        general_layout.addLayout(transparency_layout)

        show_duration_layout = QHBoxLayout()
        self.show_duration_lb = QLabel("Время появления окна:")
        show_duration_layout.addWidget(self.show_duration_lb)
        self.show_duration_spin = QSpinBox()
        self.show_duration_spin.setRange(50, 200)
        self.show_duration_spin.setSingleStep(10)
        self.show_duration_spin.setSuffix(" мс")
        self.show_duration_spin.setFixedWidth(position_grid_size.width())
        show_duration_layout.addWidget(self.show_duration_spin)
        general_layout.addLayout(show_duration_layout)

        self.animation_cb = QCheckBox("Анимация появления")
        general_layout.addWidget(self.animation_cb)

        self.taskbar_cb = QCheckBox("Учитывать панель задач")
        general_layout.addWidget(self.taskbar_cb)

        self.autostart_cb = QCheckBox("Запускать при старте системы")
        general_layout.addWidget(self.autostart_cb)

        self.audio_switch_btn = QPushButton("Настройка переключения аудио устройств")
        self.audio_switch_btn.setFixedHeight(30)
        general_layout.addWidget(self.audio_switch_btn)

        self.general_group.setLayout(general_layout)

        # === Кнопки ===
        button_layout = QHBoxLayout()
        
        self.close_btn = QPushButton("Закрыть")
        self.close_btn.setFixedHeight(30)

        self.about_btn = QToolButton()
        self.about_btn.setText("ⓘ")
        self.about_btn.setFont(QFont("Sergoe UI", 13, QFont.Weight.DemiBold))
        self.about_btn.setFixedSize(30, 30)

        self.help_btn = QToolButton()
        self.help_btn.setText("?")
        self.help_btn.setFont(QFont("Arial", 13))
        self.help_btn.setFixedSize(30, 30)
        
        button_layout.addWidget(self.about_btn)
        button_layout.addWidget(self.help_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        # Собираем всё
        layout.addWidget(self.keyboard_group)
        layout.addWidget(self.volume_group)
        layout.addWidget(self.media_group)
        layout.addWidget(self.general_group)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        
        # Подключаем сигналы
        config = self.app.config
        
        self.keyboard_enable_cb.toggled.connect(config.save_keyboard_window_enable)
        self.sound_enable_cb.toggled.connect(config.save_sound)
        self.sound_enable_cb.toggled.connect(self.sound_type_combo.setEnabled)
        self.sound_type_combo.currentIndexChanged.connect(config.save_sound_type)
        self.keyboard_show_language_cb.toggled.connect(config.save_keyboard_window_show_language)
        self.keyboard_show_cursor_cb.toggled.connect(config.save_keyboard_window_show_cursor)
        self.keyboard_show_modifiers_cb.toggled.connect(config.save_keyboard_window_show_modifiers)
        self.keyboard_override_duration_cb.toggled.connect(config.save_keyboard_window_override_duration)
        self.keyboard_override_duration_cb.toggled.connect(self.keyboard_duration_spin.setEnabled)
        self.keyboard_duration_spin.valueChanged.connect(config.save_keyboard_window_duration)
        self.keyboard_position_grid.positionChanged.connect(config.save_keyboard_window_position)

        self.volume_enable_cb.toggled.connect(config.save_volume_window_enable)
        self.volume_show_media_cb.toggled.connect(config.save_volume_window_show_media)
        self.volume_show_name_cb.toggled.connect(config.save_volume_window_show_name)
        self.volume_full_name_cb.toggled.connect(config.save_volume_window_full_name)
        self.volume_step_combo.currentTextChanged.connect(lambda text: config.save_volume_window_step(int(text)))
        self.audio_switch_btn.clicked.connect(lambda: self._show_dialog(self._audio_switch_window))
        self.volume_position_grid.positionChanged.connect(config.save_volume_window_position)

        self.media_enable_cb.toggled.connect(config.save_media_window_enable)
        self.media_show_volume_cb.toggled.connect(config.save_media_window_show_volume)
        self.media_show_on_change_cb.toggled.connect(config.save_media_window_show_on_change)
        self.media_show_timeline_cb.toggled.connect(config.save_media_window_show_timeline)
        self.media_color_by_cover_cb.toggled.connect(config.save_media_window_color_by_cover)
        self.media_position_grid.positionChanged.connect(config.save_media_window_position)

        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        self.duration_spin.valueChanged.connect(config.save_popup_duration)
        self.transparency_spin.valueChanged.connect(config.save_popup_transparency)
        self.show_duration_spin.valueChanged.connect(config.save_popup_show_duration)
        self.animation_cb.toggled.connect(config.save_animation)
        self.taskbar_cb.toggled.connect(config.save_taskbar)
        self.autostart_cb.toggled.connect(config.save_autostart)

        self.close_btn.clicked.connect(self.close)
        self.about_btn.clicked.connect(lambda: self._show_dialog(self._about_window))
        self.help_btn.clicked.connect(lambda: self._show_dialog(self._help_window))

        self._load_settings()

        self.keyboard_enable_cb.toggled.connect(self._on_keyboard_enable)
        self.volume_enable_cb.toggled.connect(self._on_volume_enable)
        self.media_enable_cb.toggled.connect(self._on_media_enable)
        self.sound_type_combo.currentIndexChanged.connect(self._on_sound_type_changed)
        self.keyboard_show_language_cb.toggled.connect(lambda checked: self.keyboard_show_cursor_cb.setEnabled(checked))

    def _load_settings(self):
        """Загружает текущие настройки из config"""
        config = self.app.config

        self.keyboard_enable_cb.setChecked(config.keyboard_window_enable)
        self.sound_enable_cb.setChecked(config.sound)
        self.sound_type_combo.setCurrentIndex(config.sound_type)
        self.keyboard_show_language_cb.setChecked(config.keyboard_window_show_language)
        self.keyboard_show_cursor_cb.setChecked(config.keyboard_window_show_cursor)
        self.keyboard_show_modifiers_cb.setChecked(config.keyboard_window_show_modifiers)
        self.keyboard_override_duration_cb.setChecked(config.keyboard_window_override_duration)
        self.keyboard_duration_spin.setValue(config.keyboard_window_duration)
        self.keyboard_position_grid.set_position(config.keyboard_window_position)

        self.volume_enable_cb.setChecked(config.volume_window_enable)
        self.volume_show_media_cb.setChecked(config.volume_window_show_media)
        self.volume_step_combo.setCurrentText(str(config.volume_window_step))
        self.volume_show_name_cb.setChecked(config.volume_window_show_name)
        self.volume_full_name_cb.setChecked(config.volume_window_full_name)
        self.volume_position_grid.set_position(config.volume_window_position)

        self.media_enable_cb.setChecked(config.media_window_enable)
        self.media_show_volume_cb.setChecked(config.media_window_show_volume)
        self.media_show_on_change_cb.setChecked(config.media_window_show_on_change)
        self.media_show_timeline_cb.setChecked(config.media_window_show_timeline)
        self.media_color_by_cover_cb.setChecked(config.media_window_color_by_cover)
        self.media_position_grid.set_position(config.media_window_position)

        self.language_combo.setCurrentText(trans.languages.get(config.language))
        self.duration_spin.setValue(config.popup_duration)
        self.transparency_spin.setValue(config.popup_transparency)
        self.show_duration_spin.setValue(config.popup_show_duration)
        self.animation_cb.setChecked(config.animation)
        self.taskbar_cb.setChecked(config.taskbar)
        self.autostart_cb.setChecked(config.autostart)
        
        self._on_keyboard_enable(config.keyboard_window_enable)
        self._on_volume_enable(config.volume_window_enable)
        self._on_media_enable(config.media_window_enable)
        self.sound_type_combo.setEnabled(config.sound)
        self.keyboard_show_cursor_cb.setEnabled(config.keyboard_window_show_language)
        self.keyboard_duration_spin.setEnabled(config.keyboard_window_override_duration)
        
    def _on_keyboard_enable(self, enabled):
        for widget in (
            self.sound_enable_cb,
            self.keyboard_show_language_cb,
            self.keyboard_show_cursor_cb,
            self.keyboard_show_modifiers_cb,
            self.keyboard_position_grid,
        ):
            widget.setEnabled(enabled)

    def _on_volume_enable(self, enabled):
        for widget in (
            self.volume_show_media_cb,
            self.media_show_volume_cb,
            self.volume_show_name_cb,
            self.volume_full_name_cb,
            self.volume_step_combo,
            self.volume_position_grid
        ):
            widget.setEnabled(enabled)

    def _on_media_enable(self, enabled):
        for widget in (
            self.media_show_volume_cb,
            self.volume_show_media_cb,
            self.media_show_on_change_cb,
            self.media_show_timeline_cb,
            self.media_color_by_cover_cb,
            self.media_position_grid,
        ):
            widget.setEnabled(enabled)
    
    def _show_dialog(self, dialog: QDialog):
        theme = get_windows_theme()
        self._overlay.setStyleSheet("background-color: rgba(0, 0, 0, 128)" if theme == "dark" else "background-color: rgba(255, 255, 255, 128)")
        self._overlay.show()
        dialog.exec()
        self._overlay.hide()
    
    def _on_sound_type_changed(self, index):
        self.app.sound_manager.set_sound(index)
        self.app.sound_manager.play_sound()
    
    def _on_language_changed(self, index):
        lang = self.language_combo.itemData(index)
        self.app.config.save_language(lang)
        loc.set_language(lang)
    
    def _update_text(self):
        self.setWindowTitle(loc.tr(trans.settings_title))
        self.keyboard_group.setTitle(loc.tr(trans.keyboard_group))  # КЛАВИАТУРА
        self.volume_group.setTitle(loc.tr(trans.volume_group))      # ГРОМКОСТЬ
        self.media_group.setTitle(loc.tr(trans.media_group))        # МУЛЬТИМЕДИА
        self.general_group.setTitle(loc.tr(trans.general_group))    # ОБЩИЕ

        # Клавиатура
        self.keyboard_enable_cb.setText(loc.tr(trans.keyboard_enable))  # Показывать окно клавиатуры
        self.keyboard_show_language_cb.setText(loc.tr(trans.keyboard_show_language))  # при смене языка
        self.keyboard_show_cursor_cb.setText(loc.tr(trans.keyboard_show_cursor))  # смена языка рядом с курсором
        self.keyboard_show_modifiers_cb.setText(loc.tr(trans.keyboard_show_locks))  # при нажатии клавиш режима
        self.sound_enable_cb.setText(loc.tr(trans.sound_enable))  # звуковой эффект
        self.keyboard_override_duration_cb.setText(loc.tr(trans.override_duration)) # своя длительность

        # Звуки
        self.sound_type_combo.setItemText(0, loc.tr(trans.sound_type_1))
        self.sound_type_combo.setItemText(1, loc.tr(trans.sound_type_2))
        self.sound_type_combo.setItemText(2, loc.tr(trans.sound_type_3))
        self.sound_type_combo.setItemText(3, loc.tr(trans.sound_type_4))
        self.sound_type_combo.setItemText(4, loc.tr(trans.sound_type_5))
        self.sound_type_combo.setItemText(5, loc.tr(trans.sound_type_6))

        # Громкость
        self.volume_enable_cb.setText(loc.tr(trans.volume_enable))  # Показывать окно громкости
        self.volume_show_media_cb.setText(loc.tr(trans.volume_show_media))  # + окно мультимедиа
        self.volume_show_name_cb.setText(loc.tr(trans.volume_show_name))  # имя аудио устройства
        self.volume_full_name_cb.setText(loc.tr(trans.volume_full_name))  # полное имя устройства
        self.volume_step_lb.setText(loc.tr(trans.volume_step))  # громкость клавишами

        # Мультимедиа
        self.media_enable_cb.setText(loc.tr(trans.media_enable))  # Показывать окно мультимедиа
        self.media_show_volume_cb.setText(loc.tr(trans.media_show_volume))  # + окно громкости
        self.media_show_on_change_cb.setText(loc.tr(trans.media_show_on_change))  # показывать при смене трека
        self.media_show_timeline_cb.setText(loc.tr(trans.media_show_timeline))  # прогресс трека
        self.media_color_by_cover_cb.setText(loc.tr(trans.media_color_by_cover))  # окно в цвет обложки

        # Общие
        self.language_lb.setText(loc.tr(trans.app_language))  # Язык приложения:
        self.duration_lb.setText(loc.tr(trans.duration_label))  # Длительность отображения:
        self.transparency_lb.setText(loc.tr(trans.transparency_label))  # Непрозрачность окна:
        self.show_duration_lb.setText(loc.tr(trans.show_duration_label))  # Время появления окна:
        self.animation_cb.setText(loc.tr(trans.animation))  # Анимация появления
        self.taskbar_cb.setText(loc.tr(trans.taskbar))  # Учитывать панель задач
        self.autostart_cb.setText(loc.tr(trans.autostart))  # Запускать при старте системы
        self.audio_switch_btn.setText(loc.tr(trans.audio_switch_btn))  # Настройка переключения аудио устройств
        self.close_btn.setText(loc.tr(trans.close_btn))  # Закрыть

        # Суффиксы
        self.duration_spin.setSuffix(loc.tr(trans.ms_suffix))  # мс
        self.transparency_spin.setSuffix(loc.tr(trans.percent_suffix))  # %
        self.show_duration_spin.setSuffix(loc.tr(trans.ms_suffix))  # мс
        