from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property, signal
from dbus_next import Variant, DBusError

import asyncio

from bluez_dbus_emulator import Application, Adapter1, Device1, GattService1, GattCharacteristic1

class NusDevice(Device1):

    call_counter = 0

    def run_connected_task(self):
        # Hack to get access to the tx characteristic.
        char_tx = self._services[0]._characteristics[0]
        char_tx.update_value(f'Count: {NusDevice.call_counter}'.encode('ascii'))
        NusDevice.call_counter += 1


async def main():
    bus = await MessageBus().connect()

    application = Application(bus)
    hci0 = Adapter1(bus, 'hci0')

    device = NusDevice(bus, hci0.path, "00:00:00:00:00:01")

    service = GattService1(bus, device.path, 0, '6e400001-b5a3-f393-e0a9-e50e24dcca9e')

    char_tx = GattCharacteristic1(bus, service.path, 0, '6e400003-b5a3-f393-e0a9-e50e24dcca9e') # Esta es la que hay que sobrecargar
    char_rx = GattCharacteristic1(bus, service.path, 1, '6e400002-b5a3-f393-e0a9-e50e24dcca9e')

    service.add_characteristic(char_tx)
    service.add_characteristic(char_rx)

    device.add_service(service)

    hci0.add_device(device)
    
    application.export()
    hci0.export()

    await bus.request_name('org.bluez')
    await bus.wait_for_disconnect()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
