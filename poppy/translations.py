# translations.py

# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Dict

class Translations():
    def __init__(self):
        self.lang_en = "en"
        self.lang_ru = "ru"

        # Инициализируем словарь ПЕРЕД вызовом _add_translations
        self._translations: Dict[str, Dict[str, str]] = {
            self.lang_en: {},
            self.lang_ru: {},
        }
        
        self._languages: Dict[str, str] = {
            self.lang_en: "English", 
            self.lang_ru: "Русский"
        }
        
        self._add_popup_translation()
        self._add_tray_translations()
        self._add_settings_translations()
        self._add_audio_switch_translations()
        self._add_info_translations()

    @property
    def languages(self) -> Dict[str, str]:
        return self._languages
    
    def _add(self, lang: str, key: str, value: str):
        self._translations[lang][key] = value
        
    def _add_popup_translation(self):
        self.input_language = "input_language"
        self._add(self.lang_en, self.input_language, "Input language")
        self._add(self.lang_ru, self.input_language, "Язык ввода")
        
        self.on = "on"
        self._add(self.lang_en, self.on, "on")
        self._add(self.lang_ru, self.on, "вкл")
        
        self.off = "off"
        self._add(self.lang_en, self.off, "off")
        self._add(self.lang_ru, self.off, "выкл")
        
        self.insert = "insert"
        self._add(self.lang_en, self.insert, "Insert")
        self._add(self.lang_ru, self.insert, "Вставка")
        
        self.replace = "replace"
        self._add(self.lang_en, self.replace, "Replace")
        self._add(self.lang_ru, self.replace, "Замена")
        
        self.lock = "lock"
        self._add(self.lang_en, self.lock, "Lock")
        self._add(self.lang_ru, self.lock, "Режим")
        
    def _add_tray_translations(self):
        self.settings = "settings"
        self.audio_device = "audio_device"
        self.exit = "exit"
        
        self._add(self.lang_en, self.settings, "Settings")
        self._add(self.lang_ru, self.settings, "Настройки")

        self._add(self.lang_en, self.audio_device, "Audio device")
        self._add(self.lang_ru, self.audio_device, "Аудио устройство")
        
        self._add(self.lang_en, self.exit, "Exit")
        self._add(self.lang_ru, self.exit, "Выход")
        
    def _add_settings_translations(self):
        # Общие
        self.settings_title = "settings_title"
        
        self._add(self.lang_en, self.settings_title, "Poppy Settings")
        self._add(self.lang_ru, self.settings_title, "Настройки Poppy")

        # Группы
        self.keyboard_group = "keyboard_group"
        self.volume_group = "volume_group"
        self.media_group = "media_group"
        self.general_group = "general_group"

        self._add(self.lang_en, self.keyboard_group, "KEYBOARD")
        self._add(self.lang_ru, self.keyboard_group, "КЛАВИАТУРА")

        self._add(self.lang_en, self.volume_group, "VOLUME")
        self._add(self.lang_ru, self.volume_group, "ГРОМКОСТЬ")

        self._add(self.lang_en, self.media_group, "MEDIA")
        self._add(self.lang_ru, self.media_group, "МУЛЬТИМЕДИА")

        self._add(self.lang_en, self.general_group, "GENERAL")
        self._add(self.lang_ru, self.general_group, "ОБЩИЕ")

        # Клавиатура
        self.keyboard_enable = "keyboard_enable"
        self.keyboard_show_language = "keyboard_show_language"
        self.keyboard_show_cursor = "keyboard_show_cursor"
        self.keyboard_show_locks = "keyboard_show_locks"
        self.sound_enable = "sound_enable"
        self.sound_type_1 = "sound_type_1"
        self.sound_type_2 = "sound_type_2"
        self.sound_type_3 = "sound_type_3"
        self.sound_type_4 = "sound_type_4"
        self.sound_type_5 = "sound_type_5"
        self.sound_type_6 = "sound_type_6"
        self.override_duration = "override_duration"

        self._add(self.lang_en, self.keyboard_enable, "Show keyboard popup")
        self._add(self.lang_ru, self.keyboard_enable, "Показывать окно клавиатуры")

        self._add(self.lang_en, self.keyboard_show_language, "on language switch")
        self._add(self.lang_ru, self.keyboard_show_language, "при смене языка")

        self._add(self.lang_en, self.keyboard_show_cursor, "language near cursor")
        self._add(self.lang_ru, self.keyboard_show_cursor, "смена языка рядом с курсором")

        self._add(self.lang_en, self.keyboard_show_locks, "on lock keys press")
        self._add(self.lang_ru, self.keyboard_show_locks, "при нажатии клавиш режима")

        self._add(self.lang_en, self.sound_enable, "sound effect:")
        self._add(self.lang_ru, self.sound_enable, "звуковой эффект:")

        self._add(self.lang_en, self.sound_type_1, "sound 1")
        self._add(self.lang_ru, self.sound_type_1, "звук 1")
        self._add(self.lang_en, self.sound_type_2, "sound 2")
        self._add(self.lang_ru, self.sound_type_2, "звук 2")
        self._add(self.lang_en, self.sound_type_3, "sound 3")
        self._add(self.lang_ru, self.sound_type_3, "звук 3")
        self._add(self.lang_en, self.sound_type_4, "sound 4")
        self._add(self.lang_ru, self.sound_type_4, "звук 4")
        self._add(self.lang_en, self.sound_type_5, "sound 5")
        self._add(self.lang_ru, self.sound_type_5, "звук 5")
        self._add(self.lang_en, self.sound_type_6, "sound 6")
        self._add(self.lang_ru, self.sound_type_6, "звук 6")
        
        self._add(self.lang_en, self.override_duration, "override duration:")
        self._add(self.lang_ru, self.override_duration, "своя длительность:")
        
        # Громкость
        self.volume_enable = "volume_enable"
        self.volume_show_media = "volume_show_media"
        self.volume_step = "volume_step"
        self.volume_show_name = "volume_show_name"
        self.volume_full_name = "volume_full_name"

        self._add(self.lang_en, self.volume_enable, "Show volume popup")
        self._add(self.lang_ru, self.volume_enable, "Показывать окно громкости")

        self._add(self.lang_en, self.volume_show_media, "+ media popup")
        self._add(self.lang_ru, self.volume_show_media, "+ окно мультимедиа")

        self._add(self.lang_en, self.volume_step, "volume step via keys")
        self._add(self.lang_ru, self.volume_step, "шаг громкости клавишами")

        self._add(self.lang_en, self.volume_show_name, "audio device name")
        self._add(self.lang_ru, self.volume_show_name, "имя аудио устройства")

        self._add(self.lang_en, self.volume_full_name, "full device name")
        self._add(self.lang_ru, self.volume_full_name, "полное имя устройства")

        # Мультимедиа
        self.media_enable = "media_enable"
        self.media_show_volume = "media_show_volume"
        self.media_show_on_change = "media_show_on_change"
        self.media_show_timeline = "media_show_timeline"
        self.media_color_by_cover = "media_color_by_cover"

        self._add(self.lang_en, self.media_enable, "Show media popup")
        self._add(self.lang_ru, self.media_enable, "Показывать окно мультимедиа")

        self._add(self.lang_en, self.media_show_volume, "+ volume popup")
        self._add(self.lang_ru, self.media_show_volume, "+ окно громкости")

        self._add(self.lang_en, self.media_show_on_change, "show on track change")
        self._add(self.lang_ru, self.media_show_on_change, "показывать при смене трека")

        self._add(self.lang_en, self.media_show_timeline, "track timeline")
        self._add(self.lang_ru, self.media_show_timeline, "прогресс трека")

        self._add(self.lang_en, self.media_color_by_cover, "popup colored by cover")
        self._add(self.lang_ru, self.media_color_by_cover, "окно в цвет обложки")

        # Общие
        self.app_language = "app_language"
        self.duration_label = "duration_label"
        self.transparency_label = "transparency_label"
        self.show_duration_label = "show_duration_label"
        self.animation = "animation"
        self.taskbar = "taskbar"
        self.autostart = "autostart"
        self.audio_switch_btn = "audio_switch_btn"
        self.close_btn = "close_btn"

        self._add(self.lang_en, self.app_language, "Application language:")
        self._add(self.lang_ru, self.app_language, "Язык приложения:")
        
        self._add(self.lang_en, self.duration_label, "Popup duration:")
        self._add(self.lang_ru, self.duration_label, "Длительность отображения:")

        self._add(self.lang_en, self.transparency_label, "Popup opacity:")
        self._add(self.lang_ru, self.transparency_label, "Непрозрачность окна:")

        self._add(self.lang_en, self.show_duration_label, "Popup fade-in time:")
        self._add(self.lang_ru, self.show_duration_label, "Время появления окна:")

        self._add(self.lang_en, self.animation, "Slide animation")
        self._add(self.lang_ru, self.animation, "Анимация появления")

        self._add(self.lang_en, self.taskbar, "Padding for taskbar")
        self._add(self.lang_ru, self.taskbar, "Учитывать панель задач")

        self._add(self.lang_en, self.autostart, "Launch on system startup")
        self._add(self.lang_ru, self.autostart, "Запускать при старте системы")

        self._add(self.lang_en, self.audio_switch_btn, "Audio device switching settings")
        self._add(self.lang_ru, self.audio_switch_btn, "Настройка переключения аудио устройств")

        self._add(self.lang_en, self.close_btn, "Close")
        self._add(self.lang_ru, self.close_btn, "Закрыть")

        # Суффиксы
        self.ms_suffix = "ms_suffix"
        self.percent_suffix = "percent_suffix"

        self._add(self.lang_en, self.ms_suffix, " ms")
        self._add(self.lang_ru, self.ms_suffix, " мс")

        self._add(self.lang_en, self.percent_suffix, "%")
        self._add(self.lang_ru, self.percent_suffix, "%")

    def _add_audio_switch_translations(self):
        # Заголовок окна
        self.audio_switch_title = "audio_switch_title"
        self._add(self.lang_en, self.audio_switch_title, "Audio device switching settings")
        self._add(self.lang_ru, self.audio_switch_title, "Настройки переключения аудио устройств")
    
        # Опции
        self.audio_switch_double_click = "audio_switch_double_click"
        self.audio_switch_tray = "audio_switch_tray"
        self.audio_switch_tray_full_name = "audio_switch_tray_full_name"
        self.audio_switch_hotkey = "audio_switch_hotkey"
        self.audio_switch_hotkey_placeholder = "audio_switch_hotkey_placeholder"
        self.audio_switch_clear_btn = "audio_switch_clear_btn"
        self.audio_switch_set_communication = "audio_switch_set_communication"
        self.audio_switch_select_audio = "audio_switch_select_audio"
        self.audio_switch_devices_group = "audio_switch_devices_group"
    
        self._add(self.lang_en, self.audio_switch_double_click, "On double-click on volume popup")
        self._add(self.lang_ru, self.audio_switch_double_click, "По двойному клику на окне громкости")
    
        self._add(self.lang_en, self.audio_switch_tray, "In system tray")
        self._add(self.lang_ru, self.audio_switch_tray, "В системном трее")
    
        self._add(self.lang_en, self.audio_switch_tray_full_name, "Full device name in system tray")
        self._add(self.lang_ru, self.audio_switch_tray_full_name, "Полное имя устройства в системном трее")
    
        self._add(self.lang_en, self.audio_switch_hotkey, "By hotkey:")
        self._add(self.lang_ru, self.audio_switch_hotkey, "Cочетанием клавиш:")
    
        self._add(self.lang_en, self.audio_switch_hotkey_placeholder, "press hotkey...")
        self._add(self.lang_ru, self.audio_switch_hotkey_placeholder, "нажмите сочетание...")
    
        self._add(self.lang_en, self.audio_switch_clear_btn, "Reset")
        self._add(self.lang_ru, self.audio_switch_clear_btn, "Сбросить")
    
        self._add(self.lang_en, self.audio_switch_set_communication, "Also set as communication device")
        self._add(self.lang_ru, self.audio_switch_set_communication, "Установливать и как устройство связи")
    
        self._add(self.lang_en, self.audio_switch_select_audio, "Only among selected devices")
        self._add(self.lang_ru, self.audio_switch_select_audio, "Только среди выбранных устройств")
    
        self._add(self.lang_en, self.audio_switch_devices_group, "Devices to switch between")
        self._add(self.lang_ru, self.audio_switch_devices_group, "Выбор устройств для переключения")
        
    def _add_info_translations(self):
        # О приложении
        self.about_title = "about_title"
        self.about_info = "about_info"
        self.about_version = "about_version"
        
        self._add(self.lang_en, self.about_title, "About")
        self._add(self.lang_ru, self.about_title, "О приложении")
        
        self._add(self.lang_en, self.about_info,
            "A system utility for Windows: displays pop-up hints on switching keyboard layout, "
            "pressing keyboard mode keys, changing volume, shows and controls media info, "
            "and features an advanced audio device switching system."
        )
        self._add(self.lang_ru, self.about_info, 
            "Системный инструмент для Windows: показывает всплывающие подсказки при переключении раскладки, "
            "нажатии клавиш режима клавиатуры, изменении громкости, отображает и управляет медиаданными, "
            "и имеет продвинутую систему переключения аудиоустройств"
        )
        
        self._add(self.lang_en, self.about_version, "Version:")
        self._add(self.lang_ru, self.about_version, "Версия:")

        # Справка
        self.help_title = "help_title"
        self.help_intro = "help_intro"
    
        # Заголовки секций
        self.help_keyboard_title = "help_keyboard_title"
        self.help_volume_title = "help_volume_title"
        self.help_media_title = "help_media_title"
        self.help_audio_switch_title = "help_audio_switch_title"
        self.help_tips_title = "help_tips_title"
    
        # Содержимое секций
        self.help_keyboard = "help_keyboard"
        self.help_volume = "help_volume"
        self.help_media = "help_media"
        self.help_audio_switch = "help_audio_switch"
        self.help_tips = "help_tips"
    
        # --- Русский ---
        self._add(self.lang_ru, self.help_title, "Справка")
        self._add(self.lang_ru, self.help_intro,
                  "Poppy показывает всплывающие подсказки при системных событиях.\nНиже — подробности по каждому разделу."
                  )
    
        self._add(self.lang_ru, self.help_keyboard_title, "Клавиатура")
        self._add(self.lang_ru, self.help_volume_title, "Громкость")
        self._add(self.lang_ru, self.help_media_title, "Мультимедиа")
        self._add(self.lang_ru, self.help_audio_switch_title, "Переключение аудио")
        self._add(self.lang_ru, self.help_tips_title, "Советы")
    
        self._add(self.lang_ru, self.help_keyboard,
                  "• Включите «Показывать окно клавиатуры», чтобы видеть уведомления о смене языка и нажатии клавиш режима (Caps Lock, Num Lock и др.).\n"
                  "• Опция «смена языка рядом с курсором» показывает попап в текущей позиции курсора.\n"
                  "• Звуковые эффекты можно включить и выбрать один из 6 вариантов.\n"
                  "• Длительность показа окна можно переопределить."
                  )
        self._add(self.lang_ru, self.help_volume,
                  "• Окно громкости появляется при изменении уровня звука с клавиатуры.\n"
                  "• Можно отображать имя аудиоустройства: краткое (например, «Динамики») или полное (например, «Динамики(Realtek)»).\n"
                  "• «шаг громкости» определяет, на сколько процентов меняется звук за одно нажатие."
                  )
        self._add(self.lang_ru, self.help_media,
                  "• Окно мультимедиа показывает информацию о текущем треке: название, исполнителя и обложку.\n"
                  "• «прогресс трека» отображает полосу воспроизведения на заднем фоне окна. Подстраивается под доминирующий цвет обложки, "
                  "если не выбрана опция «окно в цвет обложки».\n"
                  "• При включённой опции «окно в цвет обложки» фон автоматически подстраивается под доминирующий цвет обложки."
                  )
        self._add(self.lang_ru, self.help_audio_switch,
                  "• Переключение аудиоустройств можно вызвать тремя способами:\n"
                  "  – двойным кликом по окну громкости (если включена опция «полное имя устройства» в настройках окна громкости, то удобнее всего "
                  "    нажимать на название устройства, если нет - но на текст громкости),\n"
                  "  – через контекстное меню иконки в системном трее, отображение: краткое (например, «Динамики») или полное (например, «Динамики(Realtek)»),\n"
                  "  – с помощью горячей клавиши.\n"
                  "• Переключать можно по всем подключенным устройствам или только по выбраным.\n"
                  "• Если выбрана опция «Только среди выбранных устройств», можно привязать входное устройство (микрофон) для каждого аудиоустройства.\n"
                  )
        self._add(self.lang_ru, self.help_tips,
                  "💡 Советы:\n"
                  "• Чтобы сбросить горячую клавишу — нажмите Esc в поле ввода.\n"
                  "• Если окно не появляется — проверьте, не перекрывает ли его игра в полноэкранном режиме или системный интерфейс (Пуск, Win+Tab и др.).\n"
                  "• Poppy работает только на Windows 10 и 11.\n"
                  "• Тестировалось на Windows 11 23H2."
                  )

        # --- Английский ---
        self._add(self.lang_en, self.help_title, "Help")
        self._add(self.lang_en, self.help_intro,
                  "Poppy shows pop-up hints for system events.\nDetails by section below."
                  )

        self._add(self.lang_en, self.help_keyboard_title, "Keyboard")
        self._add(self.lang_en, self.help_volume_title, "Volume")
        self._add(self.lang_en, self.help_media_title, "Media")
        self._add(self.lang_en, self.help_audio_switch_title, "Audio Switching")
        self._add(self.lang_en, self.help_tips_title, "Tips")

        self._add(self.lang_en, self.help_keyboard,
                  "• Enable 'Show keyboard popup' to see notifications for layout changes and mode key presses (Caps Lock, Num Lock, etc.).\n"
                  "• 'language near cursor' displays the popup at the current cursor position.\n"
                  "• Sound effects can be enabled and selected from 6 available options.\n"
                  "• Popup duration can be overriden."
                  )
        self._add(self.lang_en, self.help_volume,
                  "• The volume popup appears when adjusting sound level using the keyboard.\n"
                  "• You can display the audio device name: short (e.g., 'Speakers') or full (e.g., 'Speakers (Realtek)').\n"
                  "• 'volume step' defines how many percent the volume changes per key press."
                  )
        self._add(self.lang_en, self.help_media,
                  "• The media popup shows information about the current track: title, artist, and cover art.\n"
                  "• 'Track timeline' displays a playback progress bar at the popup background. It adapts to the cover's dominant color of the cover "
                  "unless 'popup colored by cover' is enabled.\n"
                  "• When 'popup colored by cover' is enabled, the background automatically matches the dominant color of the cover."
                  )
        self._add(self.lang_en, self.help_audio_switch,
                  "• Audio device switching can be triggered in three ways:\n"
                  "  – by double-clicking the volume popup (if 'Full device name' is enabled in volume settings, it's easiest to click the device name; "
                  "    otherwise, click the volume text),\n"
                  "  – via the system tray icon context menu, which shows either short (e.g., 'Speakers') or full (e.g., 'Speakers (Realtek)') device name,\n"
                  "  – using a hotkey.\n"
                  "• You can switch between all connected devices or only selected ones.\n"
                  "• If 'Only among selected devices' is enabled, you can assign an input device (microphone) to each output device."
                  )
        self._add(self.lang_en, self.help_tips,
                  "💡 Tips:\n"
                  "• To clear a hotkey, press Esc in the input field.\n"
                  "• If the popup doesn't appear, check if it's being blocked by a fullscreen game or system UI (Start menu, Win+Tab, etc.).\n"
                  "• Poppy works only on Windows 10 and 11.\n"
                  "• Tested on Windows 11 23H2."
                  )


translations = Translations()

from localizer import Localizer
localizer = Localizer(translations._translations, "en")