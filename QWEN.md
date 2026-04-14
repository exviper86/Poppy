# Poppy — Context for AI Assistant

## Project Overview

**Poppy** — это легковесная утилита системных уведомлений для Windows 10/11, написанная на Python. Приложение отображает современные всплывающие уведомления (popups) в стиле Fluent Design при:
- Смене раскладки клавиатуры
- Изменении громкости
- Воспроизведении медиа (треки, обложки альбомов)

Также предоставляет продвинутую систему переключения аудиоустройств.

### Основные технологии
- **Язык**: Python 3.8+
- **GUI фреймворк**: PyQt6
- **Асинхронность**: qasync (интеграция asyncio с Qt event loop)
- **Системные API**: pywin32, pycaw (Core Audio Windows API), winsdk
- **Сборка**: PyInstaller

### Архитектура проекта

```
Poppy/
├── main.py                 # Точка входа, mutex для single-instance
├── poppy/
│   ├── app.py              # Главный класс App, координирует все компоненты
│   ├── config.py           # Конфигурация через ConfigOption классы
│   ├── config_options.py   # Базовые классы для опций конфигурации
│   │
│   ├── ui/                 # UI компоненты
│   │   ├── popups/         # Всплывающие уведомления
│   │   │   ├── _base_popup.py
│   │   │   ├── _keyboard_popup.py
│   │   │   ├── _volume_popup.py
│   │   │   └── _media_info_popup.py
│   │   └── windows/        # Окна настроек
│   │       ├── _main_window.py
│   │       ├── _keyboard_settings.py
│   │       ├── _volume_settings.py
│   │       └── ...
│   │
│   ├── hooks/              # Хуки клавиатуры и мыши
│   ├── resources/          # Иконки, звуки, ресурсы
│   │
│   ├── audio_manager.py    # Управление аудиоустройствами (pycaw)
│   ├── keyboard_handler.py # Обработка событий клавиатуры
│   ├── language_handler.py # Определение текущего языка ввода
│   ├── layout_switcher.py  # Переключение раскладок
│   ├── sound_manager.py    # Воспроизведение звуковых эффектов
│   ├── tray_manager.py     # Иконка в системном трее
│   ├── animations.py       # Анимации показа/скрытия popup
│   ├── utils.py            # Вспомогательные функции
│   └── translations.py     # Локализация (en/ru)
```

## Building and Running

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Запуск приложения
```bash
python main.py
```
Или используйте `run_qwen.bat` (если настроен).

### Сборка .exe
```bash
pyinstaller --onefile --windowed --name Poppy --add-data "poppy/resources;poppy/resources" --icon="poppy/resources/icon.ico" main.py
```
Или запустите `build.bat`.

**Важно**: При сборке путь к ресурсам должен быть `poppy/resources` (не просто `resources`).

## Development Conventions

### Структура кода
- **Именование**: snake_case для функций/переменных, PascalCase для классов
- **Импорты**: относительные импорты внутри пакета (`from .module import ...`)
- **Авторские права**: Каждый файл содержит лицензию GPL v3 в начале

### Конфигурация
Конфигурация хранится в реестре Windows через классы `ConfigOption*`:
- `ConfigOptionBool` — булевы значения
- `ConfigOptionInt` — целочисленные значения
- `ConfigOptionStr` — строковые значения
- `ConfigOptionAutostart` — автозапуск
- `ConfigOptionAudioDevices` — список аудиоустройств

Пример структуры конфигурации в `config.py`:
```python
class KeyboardWindowConfig:
    def __init__(self, name: str):
        self.enable: cBool = cBool(name + "Enable", True)
        self.show_language: cBool = cBool(name + "ShowLanguage", True)
        # ...
```

### Локализация
Все тексты UI проходят через систему локализации (`translations.py`):
```python
from poppy.translations import localizer as loc, translations as trans
loc.tr(trans.input_language)  # Вернёт "Input language" или "Язык ввода"
```

### UI/UX паттерны
- **Popups**: Наследуются от `BasePopup`, используют анимации (`Animation`)
- **Окна настроек**: Наследуются от `BaseSettingsWidget`
- **Главное окно**: Наследуется от `FluentMainWindow` (кастомный класс)
- **Трей**: Использует `pywin32` для иконки в системном трее

### Ключевые классы и их назначение

| Класс | Файл | Назначение |
|-------|------|-----------|
| `App` | `app.py` | Главный класс, инициализирует все компоненты |
| `PopupManager` | `_popup_manager.py` | Управление порядком и отображением popup |
| `KeyboardHandler` | `keyboard_handler.py` | Перехват событий клавиатуры |
| `AudioManager` | `audio_manager.py` | Управление громкостью и устройствами |
| `LayoutSwitcher` | `layout_switcher.py` | Переключение раскладок по горячим клавишам |

### Особенности реализации
- **Single-instance**: Используется mutex (`Global\PoppyMutex`) для предотвращения множественных запусков
- **Асинхронность**: `qasync.QEventLoop` интегрирует asyncio с Qt
- **Медиа-мониторинг**: Использует Windows Media Session API через `winsdk`
- **Анимации**: Кастомная система анимаций в `animations.py`

## Testing Practices

Тесты в проекте отсутствуют (упоминается в README, что это первый проект на Python). Рекомендуется:
- Добавлять юнит-тесты для `audio_manager.py`, `language_handler.py`
- Интеграционные тесты для UI компонентов

## License

**GNU General Public License v3.0**

> ⚠️ **Commercial use**: Использование в проприетарных или коммерческих приложениях требует письменного разрешения автора (exviper86@gmail.com).
