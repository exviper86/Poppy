import ctypes
import locale
import os
import sys
import winreg
from winsdk.windows.ui.viewmanagement import UIColorType, UISettings
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt6.QtCore import Qt, QSize

class Utils:
    def __new__(cls):
        raise TypeError(f"'{cls.__name__}' is a static class and cannot be instantiated.")

    @staticmethod
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
    # @staticmethod
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

    @staticmethod
    def _get_windows_accent_color(theme: str):
        color = UISettings().get_color_value(UIColorType.ACCENT_LIGHT2 if theme == "dark" else UIColorType.ACCENT_DARK1)
        return f'#{color.r:02x}{color.g:02x}{color.b:02x}'

    @staticmethod
    def get_windows_theme() -> str:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            apps_use_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return "light" if apps_use_light_theme else "dark"
        except (OSError, WindowsError, FileNotFoundError):
            return "light"

    @staticmethod
    def get_theme_colors() -> dict:
        theme = Utils.get_windows_theme()
        if theme == "light":
            return {
                "bg": "#fcfcfc",
                "text": "#202020",
                "border": "#cccccc",
                "accent": Utils._get_windows_accent_color(theme)
            }
        else:
            return {
                "bg": "#202020",
                "text": "#dddddd",
                "border": "#3D3D3D",
                "accent": Utils._get_windows_accent_color(theme)
            }
        
    @staticmethod
    def get_resource_path(path: str) -> str:
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, "poppy/resources", path)
        else:
            return os.path.join("poppy/resources", path)

    @staticmethod    
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
    
    @staticmethod
    def load_icon(path: str, opacity: float = 1.0, color: QColor = None, size: QSize = None) -> QIcon:
        return QIcon(Utils.load_pixmap(path, opacity, color, size))
    
    @staticmethod
    def load_pixmap(path: str, opacity: float = 1.0, color: QColor = None, size: QSize = None) -> QPixmap:
        pixmap = QPixmap(Utils.get_resource_path(path))
        if pixmap.isNull():
            return QPixmap()

        if size is not None and (pixmap.size() != size):
            pixmap = Utils.resize_pixmap(pixmap, size)
        
        if color is not None:
            pixmap = Utils.color_pixmap(pixmap, color)
        
        if opacity < 1.0:
            pixmap = Utils.alpha_pixmap(pixmap, opacity)
        
        return pixmap
        
    @staticmethod
    def resize_pixmap(pixmap: QPixmap, size: QSize) -> QPixmap:
        return pixmap.scaled(
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )   
    
    @staticmethod
    def alpha_pixmap(pixmap: QPixmap, opacity: float = 1.0) -> QPixmap:
        result_pixmap = QPixmap(pixmap.size())
        result_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(result_pixmap)
        painter.setOpacity(opacity)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        return result_pixmap
    
    @staticmethod
    def color_pixmap(pixmap: QPixmap, color: QColor) -> QPixmap:
        result_pixmap = QPixmap(pixmap.size())
        result_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(result_pixmap)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(result_pixmap.rect(), color)
        painter.end()

        return result_pixmap
    
    @staticmethod
    def rotate_pixmap(pixmap: QPixmap, angle: float) -> QPixmap:
        result_pixmap = QPixmap(pixmap.size())
        result_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(result_pixmap)
        painter.translate(result_pixmap.width() / 2.0, result_pixmap.height() / 2.0)
        painter.rotate(angle)
        painter.translate(-pixmap.width() / 2.0, -pixmap.height() / 2.0)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return result_pixmap
    
    @staticmethod
    def strip_audio_name(name: str) -> str:
        if '(' in name and name.endswith(')'):
            idx = name.rfind('(')
            if idx != -1:  # нашлась открывающая скобка
                name = name[:idx]
        return name.strip()