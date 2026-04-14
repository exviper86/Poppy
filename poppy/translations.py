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
        self._add_layout_switch_translations()
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
        self._add(self.lang_en, self.on, "On")
        self._add(self.lang_ru, self.on, "Вкл")
        
        self.off = "off"
        self._add(self.lang_en, self.off, "Off")
        self._add(self.lang_ru, self.off, "Выкл")
        
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
        self.audio_switch_group = "audio_switch_group"
        self.layout_switch_group = "layout_switch_group"

        self._add(self.lang_en, self.keyboard_group, "Keyboard")
        self._add(self.lang_ru, self.keyboard_group, "Клавиатура")

        self._add(self.lang_en, self.volume_group, "Volume")
        self._add(self.lang_ru, self.volume_group, "Громкость")

        self._add(self.lang_en, self.media_group, "Media")
        self._add(self.lang_ru, self.media_group, "Мультимедиа")

        self._add(self.lang_en, self.general_group, "Common settings")
        self._add(self.lang_ru, self.general_group, "Общие настройки")

        self._add(self.lang_en, self.audio_switch_group, "Audio devices")
        self._add(self.lang_ru, self.audio_switch_group, "Аудио устройства")

        self._add(self.lang_en, self.layout_switch_group, "Layout")
        self._add(self.lang_ru, self.layout_switch_group, "Раскладка")
        
        # Клавиатура
        self.keyboard_enable = "keyboard_enable"
        self.keyboard_show_language = "keyboard_show_language"
        self.keyboard_show_cursor = "keyboard_show_cursor"
        self.keyboard_show_modifiers = "keyboard_show_modifiers"
        self.sound_enable = "sound_enable"
        self.sound_type = "sound_type"
        self.sound_type_cb = "sound_type_cb"
        self.override_duration = "override_duration"

        self._add(self.lang_en, self.keyboard_enable, "Show keyboard popup")
        self._add(self.lang_ru, self.keyboard_enable, "Показывать окно клавиатуры")

        self._add(self.lang_en, self.keyboard_show_language, "Show on language switch")
        self._add(self.lang_ru, self.keyboard_show_language, "Показывать при смене языка")

        self._add(self.lang_en, self.keyboard_show_cursor, "Language popup near cursor")
        self._add(self.lang_ru, self.keyboard_show_cursor, "Окно языка рядом с курсором")

        self._add(self.lang_en, self.keyboard_show_modifiers, "Show on lock keys press")
        self._add(self.lang_ru, self.keyboard_show_modifiers, "Показывать при нажатии клавиш режима")

        self._add(self.lang_en, self.sound_enable, "Sound effect on show")
        self._add(self.lang_ru, self.sound_enable, "Звуковой эффект при показе")

        self._add(self.lang_en, self.sound_type, "Sound type")
        self._add(self.lang_ru, self.sound_type, "Тип звука")
        
        self._add(self.lang_en, self.sound_type_cb, "Sound")
        self._add(self.lang_ru, self.sound_type_cb, "Звук")
        
        self._add(self.lang_en, self.override_duration, "Override popup duration")
        self._add(self.lang_ru, self.override_duration, "Переопределить длительность отображения")
        
        # Громкость
        self.volume_enable = "volume_enable"
        self.volume_show_media = "volume_show_media"
        self.volume_step = "volume_step"
        self.volume_show_name = "volume_show_name"
        self.volume_full_name = "volume_full_name"

        self._add(self.lang_en, self.volume_enable, "Show volume popup")
        self._add(self.lang_ru, self.volume_enable, "Показывать окно громкости")

        self._add(self.lang_en, self.volume_show_media, "Also show media popup")
        self._add(self.lang_ru, self.volume_show_media, "Также показывать окно мультимедиа")

        self._add(self.lang_en, self.volume_step, "Volume change step via keys")
        self._add(self.lang_ru, self.volume_step, "Шаг изменения громкости клавишами")

        self._add(self.lang_en, self.volume_show_name, "Show audio device name")
        self._add(self.lang_ru, self.volume_show_name, "Показывать имя аудио устройства")

        self._add(self.lang_en, self.volume_full_name, "Show full device name")
        self._add(self.lang_ru, self.volume_full_name, "Показывать полное имя устройства")

        # Мультимедиа
        self.media_enable = "media_enable"
        self.media_show_volume = "media_show_volume"
        self.media_show_on_change = "media_show_on_change"
        self.media_show_timeline = "media_show_timeline"
        self.media_color_by_cover = "media_color_by_cover"

        self._add(self.lang_en, self.media_enable, "Show media popup")
        self._add(self.lang_ru, self.media_enable, "Показывать окно мультимедиа")

        self._add(self.lang_en, self.media_show_volume, "Also show volume popup")
        self._add(self.lang_ru, self.media_show_volume, "Также показывать окно громкости")

        self._add(self.lang_en, self.media_show_on_change, "Show on track change")
        self._add(self.lang_ru, self.media_show_on_change, "Показывать при смене трека")

        self._add(self.lang_en, self.media_show_timeline, "Show track timeline")
        self._add(self.lang_ru, self.media_show_timeline, "Показывать прогресс трека")

        self._add(self.lang_en, self.media_color_by_cover, "Color popup by cover")
        self._add(self.lang_ru, self.media_color_by_cover, "Красить окно в цвет обложки")

        # Общие настройки
        self.app_language_label = "app_language_label"
        self.duration_label = "duration_label"
        self.transparency_label = "transparency_label"
        self.show_duration_label = "show_duration_label"
        self.animation_label = "animation_label"
        self.taskbar_label = "taskbar_label"
        self.autostart_label = "autostart_label"

        self._add(self.lang_en, self.app_language_label, "Application language")
        self._add(self.lang_ru, self.app_language_label, "Язык приложения")
        
        self._add(self.lang_en, self.duration_label, "Popup duration")
        self._add(self.lang_ru, self.duration_label, "Длительность отображения окна")

        self._add(self.lang_en, self.transparency_label, "Popup opacity")
        self._add(self.lang_ru, self.transparency_label, "Непрозрачность окна")

        self._add(self.lang_en, self.show_duration_label, "Popup fade-in time")
        self._add(self.lang_ru, self.show_duration_label, "Время появления окна")

        self._add(self.lang_en, self.animation_label, "Popup slide animation")
        self._add(self.lang_ru, self.animation_label, "Всплывающая анимация окна")

        self._add(self.lang_en, self.taskbar_label, "Padding for taskbar_label")
        self._add(self.lang_ru, self.taskbar_label, "Учитывать панель задач")

        self._add(self.lang_en, self.autostart_label, "Launch on system startup")
        self._add(self.lang_ru, self.autostart_label, "Запускать при старте системы")

        # Общее
        self.hotkey_label = "hotkey_label"
        self.hotkey_placeholder = "hotkey_placeholder"
        self.clear_btn = "clear_btn"
        self.close_btn = "close_btn"

        self._add(self.lang_en, self.hotkey_label, "Hotkey")
        self._add(self.lang_ru, self.hotkey_label, "Сочетание клавиш")
        
        self._add(self.lang_en, self.hotkey_placeholder, "press hotkey...")
        self._add(self.lang_ru, self.hotkey_placeholder, "нажмите...")

        self._add(self.lang_en, self.clear_btn, "Reset")
        self._add(self.lang_ru, self.clear_btn, "Сбросить")

        self._add(self.lang_en, self.close_btn, "Close")
        self._add(self.lang_ru, self.close_btn, "Закрыть")

        # Суффиксы
        self.s_suffix = "s_suffix"
        self.ms_suffix = "ms_suffix"

        self._add(self.lang_en, self.s_suffix, "sec")
        self._add(self.lang_ru, self.s_suffix, "сек")
        
        self._add(self.lang_en, self.ms_suffix, "ms")
        self._add(self.lang_ru, self.ms_suffix, "мс")

    def _add_audio_switch_translations(self):
        self.audio_switch_title = "audio_switch_title"
        self.audio_switch_double_click = "audio_switch_double_click"
        self.audio_switch_tray = "audio_switch_tray"
        self.audio_switch_tray_full_name = "audio_switch_tray_full_name"
        self.audio_switch_hotkey = "audio_switch_hotkey"
        self.audio_switch_set_communication = "audio_switch_set_communication"
        self.audio_switch_select_audio = "audio_switch_select_audio"
        self.audio_switch_devices_select = "audio_switch_devices_select"
        self.audio_switch_default_mic = "audio_switch_default_mic"

        self._add(self.lang_en, self.audio_switch_title, "Audio device switching settings")
        self._add(self.lang_ru, self.audio_switch_title, "Настройка переключения аудио устройств")
    
        self._add(self.lang_en, self.audio_switch_double_click, "On double-click on volume popup")
        self._add(self.lang_ru, self.audio_switch_double_click, "По двойному клику на окне громкости")
    
        self._add(self.lang_en, self.audio_switch_tray, "In system tray")
        self._add(self.lang_ru, self.audio_switch_tray, "В системном трее")
    
        self._add(self.lang_en, self.audio_switch_tray_full_name, "Full device name in system tray")
        self._add(self.lang_ru, self.audio_switch_tray_full_name, "Полное имя устройства в системном трее")
    
        self._add(self.lang_en, self.audio_switch_hotkey, "By hotkey")
        self._add(self.lang_ru, self.audio_switch_hotkey, "Cочетанием клавиш")
    
        self._add(self.lang_en, self.audio_switch_set_communication, "Also set as communication device")
        self._add(self.lang_ru, self.audio_switch_set_communication, "Установливать и как устройство связи")
    
        self._add(self.lang_en, self.audio_switch_select_audio, "Only among selected devices")
        self._add(self.lang_ru, self.audio_switch_select_audio, "Только среди выбранных устройств")
    
        self._add(self.lang_en, self.audio_switch_devices_select, "Devices to switch between")
        self._add(self.lang_ru, self.audio_switch_devices_select, "Выбор устройств для переключения")

        self._add(self.lang_en, self.audio_switch_default_mic, "default mic")
        self._add(self.lang_ru, self.audio_switch_default_mic, "микрофон по умолчанию")
    
    def _add_layout_switch_translations(self):
        self.layout_switch_last = "layout_switch_last" 
        self.layout_switch_if_no_last = "layout_switch_if_no_last"
        self.layout_switch_selected = "layout_switch_selected"
        self.layout_switch_case = "layout_switch_case"
        self.layout_switch_block_locks = "layout_switch_block_locks"

        self._add(self.lang_en, self.layout_switch_last, "Switch last typed word layout")
        self._add(self.lang_ru, self.layout_switch_last, "Смена раскладки последнего набранного слова")

        self._add(self.lang_en, self.layout_switch_if_no_last, "Switch layout even if there is no last word")
        self._add(self.lang_ru, self.layout_switch_if_no_last, "Переключать раскладку, даже если нет последнего слова")
        
        self._add(self.lang_en, self.layout_switch_selected, "Switch selected text layout")
        self._add(self.lang_ru, self.layout_switch_selected, "Смена раскладки выделенного текста")

        self._add(self.lang_en, self.layout_switch_case, "Switch selected text case")
        self._add(self.lang_ru, self.layout_switch_case, "Смена регистра выделенного текста")
        
        self._add(self.lang_en, self.layout_switch_block_locks, "Do not send Caps, Scroll, Num Lock and Insert to system in hotkeys")
        self._add(self.lang_ru, self.layout_switch_block_locks, "Не передавать системе Caps, Scroll, Num Lock и Insert в сочетаниях клавиш")
        
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


translations: Translations = Translations()

from .localizer import Localizer
localizer: Localizer = Localizer(translations._translations, "en")