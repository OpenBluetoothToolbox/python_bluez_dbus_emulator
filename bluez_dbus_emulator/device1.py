from dbus_next.service import ServiceInterface, method, dbus_property, PropertyAccess

import asyncio
import random


class Device1(ServiceInterface):
    def __init__(self, bus, parent_path, mac_address="00:00:00:00:00:00"):
        self.bus = bus
        self.path = f"{parent_path}/dev_{'_'.join(mac_address.split(':'))}"
        super().__init__("org.bluez.Device1")
        self._exported = False
        self._connected = False
        self._services_resolved = False
        self._rssi = -128
        self._address = mac_address
        self._name = f"dev_{'_'.join(mac_address.split(':'))}"
        self._services = []

        self.__task_scanning_active = False
        self.__task_connected_active = False

    async def export(self):
        if not self._exported:
            await asyncio.sleep(random.uniform(0.5, 1.5))
            self.bus.export(f"/org/bluez/{self.path}", self)
            self._exported = True

    def add_service(self, service):
        self._services.append(service)

    def run_connected_task(self):
        pass

    async def task_scanning_start(self):
        await self.export()
        self.__task_scanning_active = True
        asyncio.ensure_future(self._task_scanning_run())

    def task_scanning_stop(self):
        self.__task_scanning_active = False

    def task_connected_start(self):
        self.__task_connected_active = True
        asyncio.ensure_future(self._task_connected_run())

    def task_connected_stop(self):
        self.__task_connected_active = False

    async def _task_scanning_run(self):
        await asyncio.sleep(random.uniform(0.02, 0.2))
        # Execute scanning tasks
        await self._update_rssi(random.uniform(-90, -60))
        if self.__task_scanning_active:
            asyncio.ensure_future(self._task_scanning_run())

    async def _task_connected_run(self):
        await asyncio.sleep(0.015)
        # Execute connected tasks
        self.run_connected_task()
        if self.__task_connected_active:
            asyncio.ensure_future(self._task_connected_run())

    @method()
    async def Connect(self):
        print("Connect")
        await self._update_connected(True)
        for service in self._services:
            service.export()
        await self._update_services_resolved(True)
        self.task_connected_start()
        return

    @method()
    async def Disconnect(self):
        print("Disconnect")
        await self._update_services_resolved(False)
        self.task_connected_stop()
        await self._update_connected(False)
        return

    @dbus_property(access=PropertyAccess.READ)
    def Connected(self) -> "b":
        return self._connected

    @dbus_property(access=PropertyAccess.READ)
    def ServicesResolved(self) -> "b":
        return self._services_resolved

    @dbus_property(access=PropertyAccess.READ)
    def RSSI(self) -> "n":
        return self._rssi

    @dbus_property(access=PropertyAccess.READ)
    def Name(self) -> "s":
        return self._name

    async def _update_connected(self, new_value: bool):
        await asyncio.sleep(random.uniform(0.5, 1.5))
        self._connected = new_value
        property_changed = {"Connected": self._connected}
        self.emit_properties_changed(property_changed)
        print(f"Property changed: {property_changed}")

    async def _update_services_resolved(self, new_value: bool):
        await asyncio.sleep(random.uniform(0.0, 0.5))
        self._services_resolved = new_value
        property_changed = {"ServicesResolved": self._services_resolved}
        self.emit_properties_changed(property_changed)
        print(f"Property changed: {property_changed}")

    async def _update_rssi(self, new_value: int):
        self._rssi = int(new_value)
        property_changed = {"RSSI": self._rssi}
        self.emit_properties_changed(property_changed)
