from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property, signal, PropertyAccess
from dbus_next import Variant, DBusError

import asyncio
import random

class GattCharacteristic1(ServiceInterface):
    def __init__(self, bus, parent_path, id_num, uuid):
        self.bus = bus
        self.path = f"{parent_path}/char{id_num:04x}"
        super().__init__('org.bluez.GattCharacteristic1')
        self._uuid = uuid
        self._value = bytes()
        self._notifying = False
        self._exported = False

    def export(self):
        if not self._exported:
            self.bus.export(f'/org/bluez/{self.path}', self)
            self._exported = True

    def update_value(self, new_value: bytes):
        self._update_value(new_value)

    @method()
    async def StartNotify(self):
        await self._update_notifying(True)
        return

    @method()
    async def StopNotify(self):
        await self._update_notifying(False)
        return

    @method()
    def ReadValue(self, options: 'a{sv}') -> 'ay':
        return self._value

    @method()
    def WriteValue(self, value: 'ay', options: 'a{sv}'):
        self._update_value(value)

    @dbus_property(access=PropertyAccess.READ)
    def Notifying(self) -> 'b':
        return self._notifying

    @dbus_property(access=PropertyAccess.READ)
    def UUID(self) -> 's':
        return self._uuid

    @dbus_property(access=PropertyAccess.READ)
    def Value(self) -> 'ay':
        return self._value

    def _update_value(self, new_value: bytes):
        self._value = new_value
        if self._notifying:
            property_changed = {'Value': self._value}
            self.emit_properties_changed(property_changed)

    async def _update_notifying(self, new_value: bool):
        await asyncio.sleep(random.uniform(0.0, 0.2))
        self._notifying = new_value
        property_changed = {'Notifying': self._notifying}
        self.emit_properties_changed(property_changed)