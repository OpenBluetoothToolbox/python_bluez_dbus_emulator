from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property, signal, PropertyAccess
from dbus_next import Variant, DBusError

import asyncio
import random

class GattService1(ServiceInterface):
    def __init__(self, bus, parent_path, id_num, uuid):
        self.bus = bus
        self.path = f"{parent_path}/service{id_num:04x}"
        super().__init__('org.bluez.GattService1')
        self._uuid = uuid
        self._exported = False
        self._characteristics = []

    def export(self):
        if not self._exported:
            self.bus.export(f'/org/bluez/{self.path}', self)
            for char in self._characteristics:
                char.export()
            self._exported = True
    
    def add_characteristic(self, characteristic):
        self._characteristics.append(characteristic)

    @dbus_property(access=PropertyAccess.READ)
    def UUID(self) -> 's':
        return self._uuid