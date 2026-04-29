# Copyright (C) 2025 exviper86
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pycaw.constants import EDataFlow, DEVICE_STATE, ERole
from pycaw.pycaw import AudioUtilities
from .config import config

class AudioManager:

    def volume_up(self) -> int:
        volume = self._get_current_audio_interface().EndpointVolume
        step = config.volume_window.step.value
        current = int(round(volume.GetMasterVolumeLevelScalar() * 100 / step) * step)
        new = min(100, current + step)
        volume.SetMasterVolumeLevelScalar(new * 0.01, None)
        volume.SetMute(0, None)
        return new

    def volume_down(self) -> int:
        volume = self._get_current_audio_interface().EndpointVolume
        step = config.volume_window.step.value
        current = int(round(volume.GetMasterVolumeLevelScalar() * 100 / step) * step)
        new = max(0, current - step)
        volume.SetMasterVolumeLevelScalar(new * 0.01, None)
        volume.SetMute(0, None)
        return new

    def set_volume(self, value):
        volume = self._get_current_audio_interface().EndpointVolume
        value = max(0, min(value, 100))
        volume.SetMasterVolumeLevelScalar(value * 0.01, None)
        volume.SetMute(0, None)

    def get_volume(self) -> int:
        volume = self._get_current_audio_interface().EndpointVolume
        step = config.volume_window.step.value
        return int(round(volume.GetMasterVolumeLevelScalar() * 100 / step) * step)

    def get_mute(self) -> bool:
        volume = self._get_current_audio_interface().EndpointVolume
        return True if volume.GetMute() == 1 else False

    def toggle_mute(self) -> bool:
        volume = self._get_current_audio_interface().EndpointVolume
        current_mute = volume.GetMute()
        new_mute = 1 - current_mute
        volume.SetMute(new_mute, None)
        return True if new_mute == 1 else False
    
    def get_device_name(self) -> str:
        return self._get_current_audio_interface().FriendlyName

    def get_all_output_devices(self) -> list:
        devices = self._get_all_audio_interfaces()
        return [{"id": device.id, "name": device.FriendlyName} for device in devices]

    def get_all_input_devices(self) -> list:
        devices = self._get_all_audio_interfaces(False)
        return [{"id": device.id, "name": device.FriendlyName} for device in devices]

    def switch_device(self, device_id: str = None):
        devices = self.get_all_output_devices()
        if not devices:
            return
        
        device_ids = {dev["id"] for dev in devices}
        
        index = -1
        dev_id = None
        mic_id = None
        current_id = self._get_current_audio_interface().id
        
        if config.audio_switch.select.value:
            enabled_devices = []
            for device in config.audio_switch.devices.value:
                if device["on"] and device["id"] in device_ids:
                    enabled_devices.append(device)
            
            if len(enabled_devices) == 0:
                return
            
            if device_id is not None:
                for dev in enabled_devices:
                    if dev["id"] == device_id:
                        dev_id = dev["id"]
                        mic_id = dev["mic"]
                        break
            else:
                for i, device in enumerate(enabled_devices):
                    if device["id"] == current_id:
                        index = i
                        break
                index = (index + 1) % len(enabled_devices)
                dev = enabled_devices[index]
                dev_id = dev["id"]
                mic_id = dev["mic"]
        else:
            if device_id is not None:
                for dev in devices:
                    if dev["id"] == device_id:
                        dev_id = dev["id"]
                        break
            else:
                for i, device in enumerate(devices):
                    if device["id"] == current_id:
                        index = i
                        break
                index = (index + 1) % len(devices)
                dev_id = devices[index]["id"]
        
        roles = [ERole.eConsole, ERole.eCommunications] if config.audio_switch.set_communication.value else None
        if dev_id:
            AudioUtilities.SetDefaultDevice(dev_id, roles)
        if mic_id:
            AudioUtilities.SetDefaultDevice(mic_id, roles)

    def _get_current_audio_interface(self):
        return AudioUtilities.GetSpeakers()
    
    def _get_all_audio_interfaces(self, render = True):
        enum = AudioUtilities.GetDeviceEnumerator()
        collection = enum.EnumAudioEndpoints(EDataFlow.eRender.value if render else EDataFlow.eCapture.value, DEVICE_STATE.ACTIVE.value)
        devices = []
        for i in range(collection.GetCount()):
            item = collection.Item(i)
            device = AudioUtilities.CreateDevice(item)
            devices.append(device)
        return devices