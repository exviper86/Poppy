from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QScrollArea, QWidget, QHBoxLayout, QComboBox, QVBoxLayout
from ._base_page import BasePage
from poppy.ui import LabeledSwitchTr, HotkeyCard, Binding
from poppy.config import config
from poppy.ui.fluent import Label, Font, Widget, Card, Toggle
from poppy.translations import localizer as loc, translations as trans


class AudioDeviceSelector(QWidget):
    deviceChanged = pyqtSignal(dict)

    def __init__(self, title: str):
        super().__init__()

        self._mic_text = "не менять микрофон"
        self._combo_boxes = []
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._title = Label(title, Font.subTitle())
        self._title.setContentsMargins(4, 8, 8, 8)
        main_layout.addWidget(self._title)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self._layout = QVBoxLayout()

        main_layout.addWidget(self._scroll_area)
    
    def setTitle(self, title: str):
        self._title.setText(title)

    def setMicText(self, text: str):
        self._mic_text = text
        for combo in self._combo_boxes:
            if combo.count() > 0:
                combo.setItemText(0, text)
    
    def setDevices(self, output_devices, input_devices, settings):
        old_widget = self._scroll_area.widget()
        if old_widget:
            old_widget.deleteLater()

        self._combo_boxes.clear()
        
        scroll_content = Widget()
        self._layout = QVBoxLayout(scroll_content)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._scroll_area.setWidget(scroll_content)

        # Создаём словарь для быстрого поиска по device_id
        bindings_dict = {item["id"]: item for item in settings}

        input_device_names = [d["name"] for d in input_devices]
        input_device_ids = [d["id"] for d in input_devices]

        for device in output_devices:
            card = Card()

            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(8)

            toggle = Toggle()
            item_layout.addWidget(toggle)

            label = Label(device["name"])
            item_layout.addWidget(label)
            
            item_layout.addStretch()
            
            combo_box = QComboBox()
            combo_box.addItem(self._mic_text)
            combo_box.addItems(input_device_names)
            item_layout.addWidget(combo_box)
            
            self._combo_boxes.append(combo_box)
            
            content = Widget()
            content.setLayout(item_layout)

            card.setHeader(content)

            self._layout.addWidget(card)

            # Настройка состояния чекбокса
            binding = bindings_dict.get(device["id"])
            if binding is not None:
                toggle.setChecked(bool(binding.get("on", False)))

                # Настройка комбобокса: выбираем привязанный микрофон
                mic_id = binding.get("mic")
                if mic_id is not None:
                    try:
                        # Находим индекс микрофона по его ID
                        mic_index = input_device_ids.index(mic_id)
                        combo_box.setCurrentIndex(mic_index + 1)  # +1 из-за "не менять микрофон"
                    except ValueError:
                        # Микрофон не найден в списке — оставляем "не менять"
                        combo_box.setCurrentIndex(0)
                else:
                    combo_box.setCurrentIndex(0)
            else:
                toggle.setChecked(False)
                combo_box.setCurrentIndex(0)

            # noinspection PyDefaultArgument
            def on_change(_, checkbox=toggle, combobox=combo_box, device_id=device["id"], input_ids=input_device_ids):
                is_enabled = checkbox.isChecked()
                m_id = None
                if is_enabled:
                    idx = combobox.currentIndex()
                    if idx > 0:  # не "не менять микрофон"
                        m_id = input_ids[idx - 1]
                self.deviceChanged.emit({"id": device_id, "on": is_enabled, "mic": m_id})

            # Подключаем оба события
            toggle.toggled.connect(on_change)
            combo_box.currentIndexChanged.connect(on_change)

        self._layout.addStretch()
        

class AudioSwitchPage(BasePage):
    def __init__(self):
        super().__init__()

    def _create_content(self, layout: QVBoxLayout):
        self._title = Label("Настройки переключения аудиоустройств", Font.subTitle())
        self._title.setContentsMargins(4, 8, 8, 8)
        layout.addWidget(self._title)
        
        self._double_click_label = Label("По двойному клику на окне громкости")
        self._double_click_labeled = LabeledSwitchTr()
        self._double_click_card = Card(self._double_click_label, self._double_click_labeled)
        layout.addWidget(self._double_click_card)

        self._tray_label = Label("В системном трее")
        self._tray_labeled = LabeledSwitchTr()
        self._tray_card = Card(self._tray_label, self._tray_labeled)
        layout.addWidget(self._tray_card)

        self._tray_full_name_label = Label("Полное имя устройства в системном трее")
        self._tray_full_name_labeled = LabeledSwitchTr()
        self._tray_full_name_card = Card(self._tray_full_name_label, self._tray_full_name_labeled)
        self._tray_full_name_card.setIdent(1)
        layout.addWidget(self._tray_full_name_card)

        self._hotkey_label = Label("Cочетанием клавиш")
        self._hotkey_labeled = LabeledSwitchTr()
        self._hotkey_card = Card(self._hotkey_label, self._hotkey_labeled)
        layout.addWidget(self._hotkey_card)

        self._hotkey_value_card = HotkeyCard()
        self._hotkey_value_card.setIdent(1)
        self._hotkey_value_card.hotkeyEdit().setFixedWidth(self._input_width)
        layout.addWidget(self._hotkey_value_card)

        self._set_communication_label = Label("Установливать и как устройство связи")
        self._set_communication_labeled = LabeledSwitchTr()
        self._set_communication_card = Card(self._set_communication_label, self._set_communication_labeled)
        layout.addWidget(self._set_communication_card)

        self._select_audio_label = Label("Только среди выбранных устройств")
        self._select_audio_labeled = LabeledSwitchTr()
        self._select_audio_card = Card(self._select_audio_label, self._select_audio_labeled)
        layout.addWidget(self._select_audio_card)

        # Выбор устройств
        self._audio_selector = AudioDeviceSelector("Выбор устройств для переключения")
        layout.addWidget(self._audio_selector, stretch=True)

        self.link_switch(self._tray_labeled.switch(), self._tray_full_name_card)
        self.link_switch(self._hotkey_labeled.switch(), self._hotkey_value_card)
        self.link_switch(self._select_audio_labeled.switch(), self._audio_selector)

    def _bind(self):
        Binding.bool(self._double_click_labeled.switch(), config.audio_switch.double_tap)
        Binding.bool(self._tray_labeled.switch(), config.audio_switch.tray)
        Binding.bool(self._tray_full_name_labeled.switch(), config.audio_switch.tray_full_name)
        Binding.bool(self._hotkey_labeled.switch(), config.audio_switch.hotkey)
        Binding.str(self._hotkey_value_card.hotkeyEdit(), config.audio_switch.hotkey_value)
        Binding.bool(self._set_communication_labeled.switch(), config.audio_switch.set_communication)
        Binding.bool(self._select_audio_labeled.switch(), config.audio_switch.select)

        from poppy.app import App
        self._audio_selector.setDevices(
            App.instance().audio_manager.get_all_output_devices(),
            App.instance().audio_manager.get_all_input_devices(),
            config.audio_switch.devices.value
        )
        self._audio_selector.deviceChanged.connect(config.audio_switch.devices.save_device)

    def _update_text(self):
        self._title.setText(loc.tr(trans.audio_switch_title))
        self._double_click_label.setText(loc.tr(trans.audio_switch_double_click))
        self._tray_label.setText(loc.tr(trans.audio_switch_tray))
        self._tray_full_name_label.setText(loc.tr(trans.audio_switch_tray_full_name))
        self._hotkey_label.setText(loc.tr(trans.audio_switch_hotkey))
        self._set_communication_label.setText(loc.tr(trans.audio_switch_set_communication))
        self._select_audio_label.setText(loc.tr(trans.audio_switch_select_audio))
        self._audio_selector.setTitle(loc.tr(trans.audio_switch_devices_select))
        self._audio_selector.setMicText(loc.tr(trans.audio_switch_default_mic))
