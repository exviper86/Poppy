# utils.py

import ctypes
import locale
import os
import sys
import winreg
from winsdk.windows.ui.viewmanagement import UIColorType, UISettings
from PyQt6.QtGui import QPixmap, QIcon, QPainter
from PyQt6.QtCore import Qt, QSize

def get_windows_ui_language() -> str:
    """Возвращает код языка интерфейса Windows, например 'en', 'ru', 'de'."""
    try:
        # Получаем LCID (Language Code Identifier)
        lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        # Преобразуем LCID в стандартный языковой тег (например, 'ru_RU')
        lang_tag = locale.windows_locale.get(lcid, 'en_US')
        # Берём только первые 2 буквы (код языка)
        return lang_tag.split('_')[0]
    except Exception:
        return 'en'  # fallback

# === Цвета и тема ===
# def _get_windows_accent_color(theme):
#     try:
#         key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
#         try:
#             accent_color, _ = winreg.QueryValueEx(key, "AccentColor")
#         except:
#             accent_color = 0xff0078d7
#         winreg.CloseKey(key)
#         blue = (accent_color >> 16) & 0xFF
#         green = (accent_color >> 8) & 0xFF
#         red = accent_color & 0xFF
#         coeff = 1 if theme == "light" else 1.3
#         red = min(255, int(red * coeff))
#         green = min(255, int(green * coeff))
#         blue = min(255, int(blue * coeff))
#         return f'#{red:02x}{green:02x}{blue:02x}'
#     except:
#         return '#0078d7'

def _get_windows_accent_color(theme):
    color = UISettings().get_color_value(UIColorType.ACCENT_LIGHT2 if theme == "dark" else UIColorType.ACCENT_DARK1)
    return f'#{color.r:02x}{color.g:02x}{color.b:02x}'

def get_windows_theme():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        apps_use_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return "light" if apps_use_light_theme else "dark"
    except:
        return "light"

def get_theme_colors():
    theme = get_windows_theme()
    if theme == "light":
        return {
            "bg": "#fcfcfc",
            "text": "#222222",
            "border": "#cccccc",
            "accent": _get_windows_accent_color(theme)
        }
    else:
        return {
            "bg": "#222222",
            "text": "#dddddd",
            "border": "#3D3D3D",
            "accent": _get_windows_accent_color(theme)
        }
    
def get_resource_path(path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "resources", path)
    else:
        return os.path.join("resources", path)
    
def color_with_alpha(hex_color: str, alpha: int) -> str:
    """
    Добавляет альфу к цвету в формате #RRGGBB.
    alpha — от 0 до 255.
    Возвращает #AARRGGBB.
    """
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    if len(hex_color) != 6:
        raise ValueError("Цвет должен быть в формате #RRGGBB")
    alpha_hex = hex(alpha)[2:].upper().zfill(2)
    return f"#{alpha_hex}{hex_color}"

def load_icon(path: str, opacity: float = 1.0, size: QSize = None) -> QIcon:
    #Загружает иконку из файла и применяет прозрачность и (опционально) масштабирование.
    
    # Загружаем исходное изображение
    original_pixmap = QPixmap(get_resource_path(path))
    if original_pixmap.isNull():
        return QIcon()  # Возвращаем пустую иконку при ошибке

    # Масштабируем, если нужно
    if size is not None and (original_pixmap.size() != size):
        scaled_pixmap = original_pixmap.scaled(
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
    else:
        scaled_pixmap = original_pixmap

    # Применяем прозрачность
    if opacity < 1.0:
        transparent_pixmap = QPixmap(scaled_pixmap.size())
        transparent_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(transparent_pixmap)
        painter.setOpacity(opacity)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        final_pixmap = transparent_pixmap
    else:
        final_pixmap = scaled_pixmap

    return QIcon(final_pixmap)


def strip_audio_name(name: str) -> str:
    if '(' in name and name.endswith(')'):
        idx = name.rfind('(')
        if idx != -1:  # нашлась открывающая скобка
            name = name[:idx]
    return name.strip()