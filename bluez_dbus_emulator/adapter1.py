from dbus_next.service import ServiceInterface, method, dbus_property, PropertyAccess

import asyncio
import random


class Adapter1(ServiceInterface):
    def __init__(self, bus, path):
        self.bus = bus
        self.path = path
        super().__init__("org.bluez.Adapter1")
        self._discovering = False
        self._address = "00:00:00:00:00:00"

        self._devices = []

    def export(self):
        self.bus.export(f"/org/bluez/{self.path}", self)

    def add_device(self, device):
        self._devices.append(device)

    @method()
    def SetDiscoveryFilter(self, properties: "a{sv}"):
        return

    @method()
    async def StartDiscovery(self):
        print("StartDiscovery")
        await self._update_discoverying(True)
        for device in self._devices:
            await device.task_scanning_start()
        return

    @method()
    async def StopDiscovery(self):
        print("StopDiscovery")
        await self._update_discoverying(False)
        for device in self._devices:
            device.task_scanning_stop()
        return

    @dbus_property(access=PropertyAccess.READ)
    def Discovering(self) -> "b":
        return self._discovering

    async def _update_discoverying(self, new_value: bool):
        await asyncio.sleep(random.uniform(0.5, 1.5))
        self._discovering = new_value
        self.emit_properties_changed({"Discovering": self._discovering})
        print(f"Property changed: {self._discovering}")
