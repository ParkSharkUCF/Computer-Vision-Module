import gatt
import api
from time import sleep, time

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        id_service = next(
            s for s in self.services
            if s.uuid == '00001523-1212-efde-1523-785feabcd123')

        id_characteristic = next(
            c for c in id_service.characteristics
            if c.uuid == '00001524-1212-efde-1523-785feabcd123')


        id_characteristic.write_value(b'\3')

    def characteristic_write_value_succeeded(self, characteristic):
        print("yay")
        manager.stop()
    def characteristic_write_value_failed(error):
        print(error)
        manager.stop()


device = AnyDevice(mac_address='D1:C6:CC:9D:30:72', manager=manager)
device.connect()
manager.run()
