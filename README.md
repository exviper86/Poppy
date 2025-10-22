<p align="center">
  <img src="header.png" height="80" />
</p>

<p align="center">
  <strong>English</strong> | <a href="README.ru.md">Русский</a>
</p>

## Windows System Notification Utility

![Downloads](https://img.shields.io/github/downloads/exviper86/poppy/total)
![GitHub Release](https://img.shields.io/github/v/release/exviper86/poppy)

---

A lightweight, elegant utility for Windows 10/11 that displays modern fluent flyout popups 
for keyboard layout changes, volume adjustments, media playback and has an advanced audio device switching.

![Keyboard Popup](screenshots/popup.png)  
*Keyboard layout change notification*

![Media + Volume Popup](screenshots/popup%20media.png)  
*Volume control + media info*

## ✨ Features

---

Poppy enhances your Windows experience with customizable notifications:

### 🔤 Keyboard
- Shows pop-up hints when switching input language (e.g., EN → RU).
- Notifies on lock key presses (Caps Lock, Num Lock, Scroll Lock).
- Option to display popup near cursor position.
- Customizable sound effects.

### 🔊 Volume
- Displays volume level on every adjustment (and hides system one).
- Сan show audio device name (short or full).
- Configurable volume step per key press.

### 🎵 Media
- Shows current track title, artist, and album art.
- Playback progress bar adapts to cover art colors.
- Option to show popup on track change.
- Background color can be matched to dominant color of the album cover.

### 🔊 Audio Device Switching
- Switch devices via:
  - Double-click on volume popup.
  - System tray icon context menu.
  - Custom hotkey (e.g., `Alt+A`).
- Choose between all connected devices or only selected ones.
- Device can be set as `Default Communication Device` too.
- Assign a input device (microphone) to each output device.

### ⚙️ General
- Fully customizable UI: screen position, opacity, duration, animation, taskbar padding.
- Auto-start on system boot.
- Works on **Windows 10 and 11** (tested on **23H2**).


## ⬇️ Installation

---

- Go to the [latest release on the Releases page](https://github.com/exviper86/poppy/releases/latest).
- Download and run Poppy.exe file
- Application is portable


## 🚀 Build

---

### Requirements
- Python 3.8+
- Windows 10 or 11

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Building an .exe
If you want to distribute a standalone executable:
```bash
pyinstaller --onefile --windowed --name Poppy --add-data "poppy/resources;resources" --icon="poppy/resources/icon.ico" poppy/main.py
```
or run build.bat


## 📄 License

---

Copyright (C) 2025 Viper

This project is licensed under the GNU General Public License v3.0 — see [LICENSE](LICENSE) for details.

>💡 Commercial use: Use in proprietary or commercial applications requires explicit written permission from the author.
Contact: [exviper86@gmail.com](mailto:exviper86@gmail.com)


## 🆘 Help & Support

---

For help, visit the in-app Help section (?) or open an issue on GitHub.

> This is my first experience with Python! 🐍
The code is not perfect and was made with AI help, so I’d really appreciate your understanding 
> and any constructive suggestions are very welcome!😊