import gatt
import api
from time import sleep, time

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        thresh_service = next(
            s for s in self.services
            if s.uuid == '00001523-1212-efde-1523-785feabcd123')

        thresh_characteristic = next(
            c for c in thresh_service.characteristics
            if c.uuid == '00001526-1212-efde-1523-785feabcd123')

        percent = api.getPercentFullGarage("C")
        if percent >= 0.95 and percent <= 1:
            thresh_characteristic.write_value(b'\1')
        elif percent >= 0.85 and percent < 0.95:
            thresh_characteristic.write_value(b'\2')
        elif percent >= 0.70 and percent < 0.85:
            thresh_characteristic.write_value(b'\3')
        elif percent >= 0.00 and percent < 0.70:
            thresh_characteristic.write_value(b'\4')

    def characteristic_write_value_succeeded(self, characteristic):
        print("yay")
        manager.stop()
    def characteristic_write_value_failed(error):
        print(error)
        manager.stop()



device = AnyDevice(mac_address='D6:43:18:ED:C3:0F', manager=manager)
device.connect()
manager.run()
