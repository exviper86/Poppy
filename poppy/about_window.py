# about_window.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from translations import localizer as loc, translations as trans
from version import __version__


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О приложении")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 10, 20, 20)

        # Иконка + заголовок
        header_layout = QHBoxLayout()

        title_label = QLabel("<h2>Poppy</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        #header_layout.addStretch()
        layout.addLayout(header_layout)

        # Описание
        self.desc = QLabel()
        self.setFixedWidth(420)
        self.desc.setWordWrap(True)
        self.desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.desc)
        layout.addSpacing(10)

        # Версия
        self.version_label = QLabel(f"Версия: {__version__}")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.version_label)

        # Автор
        author_label = QLabel("© exviper86, 2025")
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)

        # Лицензия
        gpl_url = "https://www.gnu.org/licenses/gpl-3.0.html"
        self.license_label = QLabel(
            f'<a href="{gpl_url}" style="text-decoration: none; color: #0078d7;">GNU General Public License v3.0</a>'
        )
        self.license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.license_label.setOpenExternalLinks(True)
        layout.addWidget(self.license_label)
        
        # Ссылка на GitHub (замените URL на свой)
        github_url = "https://github.com/exviper86/poppy"
        link_label = QLabel(
            f'<a href="{github_url}" style="text-decoration: none; color: #0078d7;">{github_url}</a>'
        )
        link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        link_label.setOpenExternalLinks(True)
        layout.addWidget(link_label)

        self.setLayout(layout)

        self._update_text()
        loc.language_changed.connect(self._update_text)
        
    def _update_text(self):
        self.setWindowTitle(loc.tr(trans.about_title))
        self.desc.setText(loc.tr(trans.about_info))
        self.version_label.setText(f"{loc.tr(trans.about_version)} {__version__}")
        