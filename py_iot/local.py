import json
import os
from dataclasses import dataclass
from typing import Any, List

import fire
import tinytuya

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOTFILE = '%s/setup/snapshot.json' % ROOT_DIR

rainbow = {
    'red': [255, 0, 0],
    'orange': [255, 127, 0],
    'yellow': [255, 200, 0],
    'green': [0, 255, 0],
    'blue': [0, 0, 255],
    'indigo': [46, 43, 95],
    'violet': [139, 0, 255],
    'turquoise': [48, 213, 200],
    'magenta': [255, 0, 255],
    'white': [255, 255, 176],
}


@dataclass
class Device:
    ip: str
    gwId: str
    active: int
    version: str
    name: str
    key: str
    id: str
    ver: str

    @staticmethod
    def from_dict(obj: Any) -> 'Device':
        _ip = str(obj.get('ip'))
        _gwId = str(obj.get('gwId'))
        _active = int(obj.get('active'))
        _version = str(obj.get('version'))
        _name = str(obj.get('name'))
        _key = str(obj.get('key'))
        _id = str(obj.get('id'))
        _ver = str(obj.get('ver'))

        return Device(
            _ip,
            _gwId,
            _active,
            _version,
            _name,
            _key,
            _id,
            _ver,
        )


class CLI(object):
    def __init__(self):
        self.setups = read_devices_file(SNAPSHOTFILE)

    def _get_device(self, device_name: str):
        setup = filter_setup(self.setups, device_name)
        device = tinytuya.BulbDevice(setup.id, setup.ip, setup.key)
        device.set_version(3.3)
        return device

    def status(self, device):
        data = device.status()
        return data

    def show_status(self, device_name):
        device = self._get_device(device_name)
        print(f'color: {device.colour_rgb()}')
        return device.status()

    def switch(self, device_name: str):
        device = self._get_device(device_name)
        status = self.status(device).get('dps').get('20')
        resp = device.set_status(on=not status, switch=20)
        return resp

    def color(self, device_name: str, color_name: str):
        device = self._get_device(device_name)

        rgb = rainbow.get(color_name)
        resp = device.set_colour(rgb[0], rgb[1], rgb[2])
        return resp


def read_devices_file(file_name: str) -> List[Device]:
    with open(file_name) as file:
        devices = []
        snapshot = json.load(file)
        for dict_device in snapshot.get('devices'):
            devices.append(Device.from_dict(dict_device))
        return devices


def filter_setup(setup_devices: List[Device], device_name: str) -> Device:
    device = [item for item in setup_devices if item.name == device_name]
    if len(device) == 0:
        raise Exception('Setup not found!')
    return device[0]


def main():
    fire.Fire(CLI)


if __name__ == '__main__':
    main()
