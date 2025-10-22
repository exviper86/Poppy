# animations.py

# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
from PyQt6.QtCore import QTimer, QPoint, QPointF, QSize, QSizeF
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication


class Animation:

    _animations = set()
    
    def __init__(self):
        self.startValue = None      # Если None — берётся из getter()
        self.endValue = None        # Если None — берётся из getter()
        self.duration = 0           # ms, если <=0 — анимация не запустится
        self.delay = 0              # ms, задержка перед запуском
        self.framerate = None       # кадров в секунду (FPS), если None — определяется автоматически
        self.getter = lambda: 0.0
        self.setter = lambda x: None
        self.onStarted = None
        self.onFinished = None
        self.getStartValueOnRun = False
        self.getEndValueOnRun = False

        self._timer = None          # таймер основной анимации
        self._delay_timer = None    # таймер задержки
        self._start_time = None
        self._running = False

    def run(self):
        """Запускает анимацию с поддержкой задержки и валидации."""
        self.stop()

        # Запуск с задержкой
        if self.delay > 0:
            self._delay_timer = QTimer()
            self._delay_timer.setSingleShot(True)
            self._delay_timer.timeout.connect(self._start_animation_core)
            self._delay_timer.start(self.delay)
            return

        # Запуск сразу
        self._start_animation_core()

    def _start_animation_core(self):
        """Ядро анимации — запускается после задержки или сразу."""
        if self._delay_timer:
            self._delay_timer.stop()
            self._delay_timer = None

        # Получаем значения, если они None
        if (self.startValue is None) or self.getStartValueOnRun:
            self.startValue = self.getter()
        if (self.endValue is None) or self.getEndValueOnRun :
            self.endValue = self.getter()

        # Проверяем совместимость типов
        if type(self.startValue) is not type(self.endValue):
            raise TypeError(
                f"startValue type ({type(self.startValue).__name__}) "
                f"must match endValue type ({type(self.endValue).__name__})"
            )

        # Не запускаем, если duration <= 0
        if self.duration <= 0:
            self.setter(self.endValue)
            self.stop(True)
            return

        # Определяем частоту кадров
        framerate = self.framerate
        if framerate is None:
            screen = QApplication.primaryScreen()
            framerate = screen.refreshRate() if screen else 60

        interval_ms = max(1, int(1000 / framerate))

        self._start_time = time.perf_counter()
        self._running = True

        self._timer = QTimer()
        self._timer.setInterval(interval_ms)
        self._timer.timeout.connect(self._update)
        self._timer.start()
        
        Animation._animations.add(self)

        if self.onStarted:
            self.onStarted()

    def _interpolate(self, start, end, progress):
        """Интерполирует между start и end с учётом типа."""
        if isinstance(start, (int, float)):
            return start + (end - start) * progress

        elif isinstance(start, QPoint):
            x = int(start.x() + (end.x() - start.x()) * progress)
            y = int(start.y() + (end.y() - start.y()) * progress)
            return QPoint(x, y)

        elif isinstance(start, QPointF):
            x = start.x() + (end.x() - start.x()) * progress
            y = start.y() + (end.y() - start.y()) * progress
            return QPointF(x, y)

        elif isinstance(start, QSize):
            w = int(start.width() + (end.width() - start.width()) * progress)
            h = int(start.height() + (end.height() - start.height()) * progress)
            return QSize(w, h)

        elif isinstance(start, QSizeF):
            w = start.width() + (end.width() - start.width()) * progress
            h = start.height() + (end.height() - start.height()) * progress
            return QSizeF(w, h)

        elif isinstance(start, QColor):
            r = int(start.red() + (end.red() - start.red()) * progress)
            g = int(start.green() + (end.green() - start.green()) * progress)
            b = int(start.blue() + (end.blue() - start.blue()) * progress)
            a = int(start.alpha() + (end.alpha() - start.alpha()) * progress)
            return QColor(r, g, b, a)

        else:
            raise TypeError(f"Unsupported type for animation: {type(start).__name__}")

    def _update(self):
        if not self._running:
            return

        now = time.perf_counter()
        elapsed_ms = (now - self._start_time) * 1000
        progress = min(elapsed_ms / self.duration, 1.0)

        try:
            current_value = self._interpolate(self.startValue, self.endValue, progress)
        except Exception as e:
            self.stop()
            raise RuntimeError(f"Interpolation failed: {e}")

        self.setter(current_value)
        
        if progress >= 1.0:
            self.stop(True)

    def stop(self, with_onFinished = False):
        """Останавливает анимацию и таймер задержки."""
        if self._delay_timer:
            self._delay_timer.stop()
            self._delay_timer = None

        if self._timer:
            self._timer.stop()
            self._timer = None

        Animation._animations.discard(self)

        if self._running and with_onFinished:
            if self.onFinished:
                self.onFinished()
        
        self._running = False

    @property
    def is_running(self):
        return self._running

    @property
    def is_delaying(self):
        return self._delay_timer is not None

    @classmethod
    def stop_all(cls):
        """Опционально: остановить все активные анимации."""
        for anim in list(cls._animations):
            anim.stop()