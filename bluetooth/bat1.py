import gatt
import api
from time import sleep, time

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        bat_service = next(
            s for s in self.services
            if s.uuid == '00001523-1212-efde-1523-785feabcd123')

        bat_characteristic = next(
            c for c in bat_service.characteristics
            if c.uuid == '00001527-1212-efde-1523-785feabcd123')


        bat_characteristic.read_value()


    def characteristic_value_updated(self, characteristic, value):
        print("printy print:", (value[0]))
        res = api.update_sensor("3C", {'batLevel': value[0]});
        manager.stop()


device = AnyDevice(mac_address='D6:43:18:ED:C3:0F', manager=manager)
device.connect()
manager.run()
