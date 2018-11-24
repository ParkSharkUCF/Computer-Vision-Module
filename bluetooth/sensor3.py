import gatt
import api
from time import sleep, time

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        spot_service = next(
            s for s in self.services
            if s.uuid == '00001523-1212-efde-1523-785feabcd123')

        spot_characteristic = next(
            c for c in spot_service.characteristics
            if c.uuid == '00001527-1212-efde-1523-785feabcd123')

        
        spot_characteristic.read_value()
        

    def characteristic_value_updated(self, characteristic, value):
        print("printy print:", (value[0]))
        print(value[1])
        print(value[2])
        print(value[3])
        #res = api.update_sensor("4C", {'cars': value[0], 'lastUpdated': time()}) 
        manager.stop()        


device = AnyDevice(mac_address='D1:48:F2:47:A4:06', manager=manager)
device.connect()
manager.run()

    
    
