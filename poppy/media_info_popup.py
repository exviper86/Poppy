# media_info_popup.py

# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio

import winsdk.windows.media.control as wmc
from winsdk.windows.storage.streams import Buffer, InputStreamOptions
from datetime import datetime, timezone
from base_popup import BasePopup
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QSlider, QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QSize, QRectF, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPainterPath, QColor, QImage
from utils import get_windows_theme, color_with_alpha, load_icon, get_theme_colors
from scrolling_label import ScrollingLabel

class TimelineBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._progress = 0.0  # от 0.0 до 1.0
        self._background_color = QColor(255, 255, 255, 30)
        self._progress_color = QColor(0, 120, 215)
        self._radius = 8

    def set_background_color(self, background: QColor):
        self._background_color = background
        self.update()

    def set_progress_color(self, progress: QColor):
        self._progress_color = progress
        self.update()

    def set_progress(self, value: float):
        self._progress = max(0.0, min(1.0, value))
        self.update()

    def set_radius(self, radius: int):
        self._radius = radius
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        full_rect = QRectF(self.rect())
        # Фон
        if self._background_color.alpha() > 0:
            painter.setBrush(self._background_color)
            bg_path = QPainterPath()
            bg_path.addRoundedRect(full_rect, self._radius, self._radius)
            painter.drawPath(bg_path)

        # Прогресс
        if self._progress > 0 and self._progress_color.alpha() > 0:
            crop_rect = QRectF(full_rect.left(), full_rect.top(), full_rect.width() * self._progress, full_rect.height())
            painter.setBrush(self._progress_color)
            painter.save()
            painter.setClipRect(crop_rect, Qt.ClipOperation.IntersectClip)
            pr_path = QPainterPath()
            pr_path.addRoundedRect(full_rect, self._radius, self._radius)
            painter.drawPath(pr_path)
            painter.restore()

class MediaInfoPopup(BasePopup):
    def start_monitoring(self):
        self._session = None
        self._session_manager = None
        self._session_changed_token = None
        self._media_props_token = None
        self._playback_info_token = None
        
        self._last_track = None
        self._last_cover = None
        
        asyncio.create_task(self._init_session_monitoring())
        
        self._timeline_timer = QTimer()
        self._timeline_timer.timeout.connect(self._update_timeline)
        self._timeline_timer.setInterval(200)
        
        self.cover_color = None
    
    def create_content(self, background_widget):
        self.timeline = TimelineBar(background_widget)
        self.timeline.resize(self.window_width, self.window_height)
        self.timeline.set_background_color(QColor(0, 0, 0, 0))
        
        main_layout = QHBoxLayout(background_widget)
        main_layout.setSpacing(5)
    
        # Обложка (слева)
        self.cover_label = QLabel()
        self.cover_label.setFixedSize(80, 80)
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_default_cover()
    
        # Текст и кнопки (справа)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)
    
        # Текст
        self.title_label = ScrollingLabel()
        self.title_label.setFont(QFont("Segoe UI Variable", 11, QFont.Weight.DemiBold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.title_label.setFixedHeight(18)
    
        self.artist_label = ScrollingLabel()
        self.artist_label.setFont(QFont("Segoe UI Variable", 10, QFont.Weight.DemiBold))
        self.artist_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        #self.artist_label.setFixedHeight(18)
    
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.prev_button = QToolButton()
        self.play_pause_button = QToolButton()
        self.next_button = QToolButton()
    
        # Устанавливаем минимальный размер и стиль
        for btn in (self.prev_button, self.play_pause_button, self.next_button):
            btn.setFixedSize(50, 35)
            btn.setIconSize(QSize(20, 20))
    
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.play_pause_button)
        buttons_layout.addWidget(self.next_button)
    
        # Собираем правую часть
        right_layout.addWidget(self.title_label)
        right_layout.addWidget(self.artist_label)
        right_layout.addLayout(buttons_layout)
        #right_layout.addStretch()
    
        # Основной layout
        main_layout.addWidget(self.cover_label)
        main_layout.addLayout(right_layout)

        # Подключаем кнопки
        self.prev_button.clicked.connect(lambda: asyncio.create_task(self._on_prev_clicked()))
        self.next_button.clicked.connect(lambda: asyncio.create_task(self._on_next_clicked()))
        self.play_pause_button.clicked.connect(lambda: asyncio.create_task(self._on_play_pause_clicked()))

    def apply_theme_content(self, colors):
        self.title_label.setStyleSheet(f"color: {colors['accent']};")
        self.artist_label.setStyleSheet(f"color: {colors['text']};")
        #self.cover_label.setStyleSheet(f"background-color: {color_with_alpha(colors['border'], 175)}; border-radius: 8px;")
        self.cover_label.setStyleSheet(f"background-color: transparent;")

        for btn in (self.prev_button, self.play_pause_button, self.next_button):
            btn.setStyleSheet(f"""
                QToolButton {{
                    background-color: transparent;
                    border: none;
                    border-radius: 6px;
                }}
                QToolButton:hover {{
                    background-color: {color_with_alpha(colors['border'], 175)};
                }}
                QToolButton:pressed {{
                    background-color: {color_with_alpha(colors['text'], 50)};
                }}
                QToolButton:disabled {{
                }}
            """)

        #self.timeline.set_progress_color(QColor(color_with_alpha(colors['border'], 100)))

    def update_screen_position(self):
        self.screen_position = self.app.config.media_window_position
    
    def showEvent(self, a0):
        super().showEvent(a0)
        if self.app.config.media_window_show_timeline:
            self._timeline_timer.start()
    
    def hideEvent(self, a0):
        super().hideEvent(a0)
        self._timeline_timer.stop()
    
    def show_popup(self):
        if not self.app.config.media_window_enable:
            return

        if not self._session:
            return 

        if self.app.config.media_window_show_volume and (not self.app.volume_popup.isVisible() or not self.app.volume_popup.is_active):
            self.app.volume_popup.show_popup(self.app.keyboard_handler.get_volume())
            return

        """
        Синхронная обёртка для обратной совместимости.
        Запускает асинхронную загрузку без блокировки GUI.
        """
        asyncio.create_task(self._show_popup_async())

    async def _show_popup_async(self):
        """Асинхронная загрузка медиа-информации с обложкой."""
        try:
            info = await self._get_media_info()
        except Exception as e:
            info = {"title": "Неизвестное название", "artist": "Неизвестный исполнитель"}
            print(f"[MediaInfoPopup] Ошибка при загрузке: {e}")
        
        # Обновляем UI (всё ещё в основном потоке — безопасно)
        self.title_label.setText(info["title"])
        self.artist_label.setText(info["artist"])
    
        if info.get("cover_bytes"):
            self._set_cover_from_bytes(info["cover_bytes"])
        else:
            self._set_default_cover()

        self._update_timeline()
        self._update_buttons()
        
        self._show_popup()
        
        self._set_background_color()

    def _update_timeline(self):
        if not self._session or not self.app.config.media_window_show_timeline:
            self.timeline.set_progress(0.0)
            return
        
        try:
            # 'end_time', 'last_updated_time', 'max_seek_time', 'min_seek_time', 'position', 'start_time'
            playback_info = self._session.get_playback_info()
            if not playback_info:
                return
            
            is_playing = playback_info.playback_status == wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING
            
            timeline = self._session.get_timeline_properties()
            if not timeline:
                return
            
            position = timeline.position.total_seconds()
            start = timeline.start_time.total_seconds()
            end = timeline.end_time.total_seconds()
    
            now = datetime.now(timezone.utc)
            elapsed = (now - timeline.last_updated_time).total_seconds()
    
            playback_rate = playback_info.playback_rate or 1.0
    
            if is_playing:
                current = position + (elapsed * playback_rate)
            else:
                current = position
            
            progress = (current - start) / (end - start) if end else 0.0 
            self.timeline.set_progress(progress)
            
        except Exception as e:
            print(f"[MediaInfoPopup] Ошибка обновления состояния таймлайна: {e}")

    def _update_buttons(self):
        if not self._session:
            self.prev_button.setEnabled(False)
            self.play_pause_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return
        
        try:
            playback_info = self._session.get_playback_info()
            if not playback_info:
                return 
            
            is_playing = playback_info.playback_status == wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING
            prev_enabled = playback_info.controls.is_previous_enabled
            play_enabled = playback_info.controls.is_play_pause_toggle_enabled
            next_enabled = playback_info.controls.is_next_enabled

            icon_name = "pause.png" if is_playing else "play.png"
            icon_path = f"icons/{get_windows_theme()}/{icon_name}"
            self.play_pause_button.setIcon(load_icon(icon_path, 1 if play_enabled else 0.5))
            self.prev_button.setIcon(load_icon(f"icons/{get_windows_theme()}/prev.png", 1 if prev_enabled else 0.5))
            self.next_button.setIcon(load_icon(f"icons/{get_windows_theme()}/next.png", 1 if next_enabled else 0.5))
            
            self.prev_button.setEnabled(bool(playback_info.controls.is_previous_enabled))
            self.play_pause_button.setEnabled(bool(playback_info.controls.is_play_pause_toggle_enabled))
            self.next_button.setEnabled(bool(playback_info.controls.is_next_enabled))
    
        except Exception as e:
            print(f"[MediaInfoPopup] Ошибка обновления состояния кнопок: {e}")
            self.prev_button.setEnabled(False)
            self.play_pause_button.setEnabled(False)
            self.next_button.setEnabled(False)

    async def _get_media_info(self):
        """Получает метаданные и обложку текущей медиасессии."""
        try:
            if self._session is None:
                return None

            media_properties = await self._session.try_get_media_properties_async()
            
            if not media_properties:
                return None

            title = media_properties.title or "Без названия"
            artist = media_properties.artist or "Неизвестен"
            track = title + artist
            
            if self._last_track != track:
                self._last_track = track
                self._last_cover = None
                
            if not self._last_cover:
                cover_bytes = None
                thumbnail = media_properties.thumbnail
                if thumbnail:
                    cover_bytes = await self._read_thumbnail(thumbnail)
                self._last_cover = cover_bytes


            return {
                "title": title,
                "artist": artist,
                "cover_bytes": self._last_cover
            }

        except Exception as e:
            print(f"[MediaInfoPopup] Ошибка в get_media_info: {e}")
            return None

    async def _read_thumbnail(self, thumbnail):
        """Читает обложку из thumbnail с корректным использованием Buffer."""
        try:
            stream = await thumbnail.open_read_async()
            buf = Buffer(stream.size)
            buf = await stream.read_async(buf, stream.size, InputStreamOptions.READ_AHEAD)
            return bytes(buf)
        except Exception as e:
            print(f"[MediaInfoPopup] Ошибка чтения обложки: {e}")
            return None

    def _set_cover_from_bytes(self, image_data: bytes):
        """Принимает raw bytes изображения и отображает обложку с закруглёнными краями."""
        if not image_data:
            self._set_default_cover()
            return

        pixmap = QPixmap()
        if not pixmap.loadFromData(image_data):
            self._set_default_cover()
            return

        # Масштабируем до квадрата 80x80 (обложка обычно квадратная)
        size = 80
        pixmap = pixmap.scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        # Обрезаем до квадрата (берём центр)
        if pixmap.width() > size or pixmap.height() > size:
            rect = pixmap.rect()
            rect.setSize(QSize(size, size))
            rect.moveCenter(pixmap.rect().center())
            pixmap = pixmap.copy(rect)

        # Создаём маску с закруглёнными краями
        rounded_pixmap = QPixmap(size, size)
        rounded_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, size, size), 5, 5)  # радиус 6px
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.cover_label.setPixmap(rounded_pixmap)
        self.cover_label.setText("")  # убираем текст

        self._update_timeline_colors(pixmap)
        
    def _set_default_cover(self):
        self.cover_label.setText("♪")
        self.cover_label.setFont(QFont("Arial", 36))
        self.cover_color = None
    
    def _update_timeline_colors(self, pixmap: QPixmap):
        avg_color = self._get_average_color(pixmap)
        h, s, l, _ = avg_color.getHsl()
        if h == -1:
            # Чёрный, белый или серый — используем нейтральный серый с L=128
            timeline_color = QColor.fromHsl(0, 0, 128)
        else:
            # Сохраняем оттенок и насыщенность, устанавливаем L=128
            timeline_color = QColor.fromHsl(h, s, 128)

        self.cover_color = timeline_color

        if self.app.config.media_window_color_by_cover:
            theme = get_windows_theme()
            if theme == "dark":
                color = QColor("white")
            else:
                color = QColor("black")
            color.setAlpha(20)
            self.timeline.set_progress_color(color)
        else:
            timeline_color.setAlpha(35)
            self.timeline.set_progress_color(timeline_color)
    
    def _get_average_color(self, pixmap: QPixmap, step: int = 5) -> QColor:
        """Возвращает усреднённый цвет изображения, анализируя каждый `step`-й пиксель."""
        if pixmap.isNull():
            return QColor(128, 128, 128)  # fallback цвет
    
        image = pixmap.toImage()
        width = image.width()
        height = image.height()
    
        if width == 0 or height == 0:
            return QColor(128, 128, 128)
    
        r = g = b = 0
        pixel_count = 0
    
        # Проходим с шагом `step` по обеим осям
        for y in range(0, height, step):
            for x in range(0, width, step):
                color = QColor(image.pixel(x, y))
                # Опционально: пропускать прозрачные/почти прозрачные пиксели
                if color.alpha() < 10:
                    continue
                r += color.red()
                g += color.green()
                b += color.blue()
                pixel_count += 1
    
        # Если все пиксели были прозрачными — возвращаем fallback
        if pixel_count == 0:
            return QColor(128, 128, 128)
    
        avg_r = r // pixel_count
        avg_g = g // pixel_count
        avg_b = b // pixel_count
    
        return QColor(avg_r, avg_g, avg_b)
    
    def _set_background_color(self):
        colors = get_theme_colors()

        bg = colors["bg"]
        border = colors["border"]
        
        if self.app.config.media_window_color_by_cover and self.cover_color:
            theme = get_windows_theme()
            h, s, l, _ = self.cover_color.getHsl()
            if theme == "dark":
                bg = QColor.fromHsl(h, s, 50).name()
            else:
                bg = QColor.fromHsl(h, s, 200).name()
            
        
        self.setStyleSheet(f"""
            #backgroundWidget {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 8px;
            }}
        """)
    
    async def _on_prev_clicked(self):
        if self._session:
            await self._session.try_skip_previous_async()

    async def _on_next_clicked(self):
        if self._session:
            await self._session.try_skip_next_async()
            
    async def _on_play_pause_clicked(self):
        if self._session:
            await self._session.try_toggle_play_pause_async()

    # Мониторинг сессии
    async def _init_session_monitoring(self):
        """Инициализирует менеджер сессий и подписывается на события."""
        try:
            self._session_manager = await wmc.GlobalSystemMediaTransportControlsSessionManager.request_async()
            self._session_changed_token = self._session_manager.add_current_session_changed(self._on_current_session_changed)
            self._on_current_session_changed(None, None)  # Инициализация текущей сессии
        except Exception as e:
            print(f"[MediaInfoPopup] Ошибка инициализации мониторинга: {e}")

    def _on_current_session_changed(self, sender, args):
        """Вызывается при смене активной медиасессии."""
        # Отписываемся от старой сессии, если она есть
        try:
            if self._session:
                if self._media_props_token is not None:
                    self._session.remove_media_properties_changed(self._media_props_token)
            if self._playback_info_token is not None:
                self._session.remove_playback_info_changed(self._playback_info_token)

            # Подписываемся на новую сессию
            self._session = self._session_manager.get_current_session()
            if self._session:
                self._media_props_token = self._session.add_media_properties_changed(self._on_media_properties_changed)
                self._playback_info_token = self._session.add_playback_info_changed(self._on_playback_info_changed)
                if sender:
                    print("_on_current_session_changed")
                    # if self.isVisible() or self.app.config.media_window_show_on_change:
                    #     self.app.loop.call_soon_threadsafe(self.show_popup)
            else:
                self._media_props_token = None
                self._playback_info_token = None
        except Exception as e:
            print(f"[MediaInfoPopup] Ошибка смены сессии: {e}")
    
    def _on_media_properties_changed(self, sender, args):
        """Вызывается при смене метаданных (трек, исполнитель, обложка)."""
        print("_on_media_properties_changed")
        if self.isVisible() or self.app.config.media_window_show_on_change:
            self.app.loop.call_soon_threadsafe(self.show_popup)
        return 
    
    def _on_playback_info_changed(self, sender, args):
        """Вызывается при смене состояния (play/pause). Можно обновлять иконку кнопки."""
        if self.isVisible():
            self.app.loop.call_soon_threadsafe(self._update_buttons)
            #self.app.loop.call_soon_threadsafe(self.show_popup)
        return 