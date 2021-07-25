from dbus_next.service import ServiceInterface, method


class Emulator(ServiceInterface):
    """
    Entry point for the bluez dbus emulator. Provides programmatic
    control of the async application.
    """

    def __init__(self, bus):
        self.bus = bus
        super().__init__("emulator.bluez_dbus")

    def export(self):
        self.bus.export("/", self)

    @method()
    def Exit(self):
        """
        Finishes the emulation session by disconnecting from dbus.
        """
        self.bus.disconnect()
