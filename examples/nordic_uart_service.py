import asyncio
import dbus_next
from dbus_next.aio import MessageBus
from bluez_dbus_emulator import Emulator, Adapter1, Device1, GattService1, GattCharacteristic1


class NusDevice(Device1):

    call_counter = 0

    def run_connected_task(self):
        """
        At every connection interval, this method is called to perform an update of
        the TX characteristic.
        """
        # Hack to get access to the tx characteristic.
        char_tx = self._services[0]._characteristics[0]
        char_tx.update_value(f"Count: {NusDevice.call_counter}".encode("ascii"))
        NusDevice.call_counter += 1


async def main():

    # NOTE: The SYSTEM bus can also be used, however this is only possible when
    #       the bluetooth service is not running and the script is executed with
    #       root privileges.
    bus = await MessageBus(bus_type=dbus_next.BusType.SESSION).connect()
  
    emulator = Emulator(bus)

    # Set up the BLE adapter, that is able to communicate with a BLE device containing
    # the Nordic UART service.
    hci0 = Adapter1(bus, "hci0")
    device = NusDevice(bus, hci0.path, "00:00:00:00:00:01")
    service = GattService1(bus, device.path, 0, "6e400001-b5a3-f393-e0a9-e50e24dcca9e")
    char_tx = GattCharacteristic1(bus, service.path, 0, "6e400003-b5a3-f393-e0a9-e50e24dcca9e")
    char_rx = GattCharacteristic1(bus, service.path, 1, "6e400002-b5a3-f393-e0a9-e50e24dcca9e")

    service.add_characteristic(char_tx)
    service.add_characteristic(char_rx)
    device.add_service(service)
    hci0.add_device(device)

    emulator.export()
    hci0.export()

    await bus.request_name("org.bluez")
    await bus.wait_for_disconnect()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
