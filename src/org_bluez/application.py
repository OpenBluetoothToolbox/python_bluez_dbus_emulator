
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property, signal
from dbus_next import Variant, DBusError

class Application(ServiceInterface):
    def __init__(self, bus):
        self.bus = bus
        super().__init__('test.application')

    def export(self):
        self.bus.export('/', self)

    @method()
    def Exit(self):
        self.bus.disconnect()