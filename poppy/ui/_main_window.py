from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout
from poppy.ui.fluent import Label, FluentMainWindow, NavigationView, Font
from poppy.translations import localizer as loc, translations as trans
from poppy.ui.fluent import NavigationViewItem
from poppy.ui.pages import GeneralPage, KeyboardPage, VolumePage, MultimediaPage, HelpPage, AudioSwitchPage, LayoutSwitchPage
from poppy.ui.pages import AboutPage
from poppy.utils import Utils

class MainWindow(FluentMainWindow):
    def __init__(self):        
        super().__init__()

        self.resize(800, 564)
        
        self._init()

        self._update_text()
        loc.language_changed.connect(self._update_text)
        
        self.destroyed.connect(lambda: loc.language_changed.disconnect(self._update_text))
    
    def _init(self):
        self._navigation = NavigationView()
        self._navigation.setIconSize(QSize(20, 20))
        
        self._header = Label("Header", Font.header())
        self._header.setContentsMargins(4, -8, 8, 16)
        self._navigation.setHeader(self._header)
        self._navigation.selectedItemChanged.connect(lambda i: self._header.setText(i.text().strip()))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        layout.addWidget(self._navigation)

        self._keyboard = NavigationViewItem(KeyboardPage, "Клавиатура", QIcon(Utils.load_icon("icons/keyboard.png")))
        self._navigation.addItem(self._keyboard)

        self._volume = NavigationViewItem(VolumePage, "Громкость", QIcon(Utils.load_icon("icons/volume.png")))
        self._navigation.addItem(self._volume)

        self._multimedia = NavigationViewItem(MultimediaPage, "Мультимедиа", QIcon(Utils.load_icon("icons/multimedia.png")))
        self._navigation.addItem(self._multimedia)
        
        self._general = NavigationViewItem(GeneralPage, "Общие настройки", QIcon(Utils.load_icon("icons/settings.png")))
        self._navigation.addItem(self._general)

        self._audio_switch = NavigationViewItem(AudioSwitchPage, "Аудио устройства", QIcon(Utils.load_icon("icons/audio_switch.png")))
        self._navigation.addItem(self._audio_switch)

        self._layout_switch = NavigationViewItem(LayoutSwitchPage, "Переключение раскладки", QIcon(Utils.load_icon("icons/layout_switch.png")))
        self._navigation.addItem(self._layout_switch)
        
        self._help = NavigationViewItem(HelpPage, "Справка", QIcon(Utils.load_icon("icons/help.png")))
        self._navigation.addFooterItem(self._help)
         
        self._about = NavigationViewItem(AboutPage, "О приложении", QIcon(Utils.load_icon("icons/info.png")))
        self._navigation.addFooterItem(self._about)

    def _update_text(self):
        self._keyboard.setText(f"  {loc.tr(trans.keyboard_group)}")
        self._volume.setText(f"  {loc.tr(trans.volume_group)}")
        self._multimedia.setText(f"  {loc.tr(trans.media_group)}")
        self._general.setText(f"  {loc.tr(trans.general_group)}")
        self._audio_switch.setText(f"  {loc.tr(trans.audio_switch_group)}")
        self._layout_switch.setText(f"  {loc.tr(trans.layout_switch_group)}")
        self._help.setText(f"  {loc.tr(trans.help_title)}")
        self._about.setText(f"  {loc.tr(trans.about_title)}")
        
        selected_item = self._navigation.selectedItem()
        if selected_item:
            self._header.setText(selected_item.text().strip())
        
        
        
