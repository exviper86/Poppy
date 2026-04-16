from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout
from poppy.ui.fluent import Label, Font
from ._base_page import BasePage
from poppy.app_info import app_name, app_version
from poppy.translations import localizer as loc, translations as trans

class AboutPage(BasePage):
    def __init__(self):
        super().__init__()
        
    def _create_content(self, layout: QVBoxLayout):
        layout.setSpacing(0)
        
        # Заголовок
        title_label = Label(app_name, Font.title())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(16)
        
        # Описание
        self.desc = Label()
        self.desc.setWordWrap(True)
        self.desc.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.desc, stretch=True)

        layout.addSpacing(16)
        
        # Версия
        self.version_label = Label(f"Версия: {app_version}")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.version_label)

        layout.addSpacing(8)
        
        # Автор
        author_label = Label("© exviper86, 2025")
        author_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(author_label)

        layout.addSpacing(8)
        
        # Лицензия
        gpl_url = "https://www.gnu.org/licenses/gpl-3.0.html"
        self.license_label = Label(
            f'<a href="{gpl_url}" style="text-decoration: none; color: #0078d7;">GNU General Public License v3.0</a>'
        )
        self.license_label.setOpenExternalLinks(True)
        self.license_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.license_label)

        layout.addSpacing(8)
        
        # Ссылка на GitHub (замените URL на свой)
        github_url = "https://github.com/exviper86/poppy"
        link_label = Label(f'<a href="{github_url}" style="text-decoration: none; color: #0078d7;">{github_url}</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(link_label)

    def _update_text(self):
        self.setWindowTitle(loc.tr(trans.about_title))
        self.desc.setText(loc.tr(trans.about_info))
        self.version_label.setText(f"{loc.tr(trans.about_version)} {app_version}")