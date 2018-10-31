import gatt
from time import sleep

manager = gatt.DeviceManager(adapter_name='hci0')

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        light_service = next(
            s for s in self.services
            if s.uuid == '00001523-1212-efde-1523-785feabcd123')

        light_characteristic = next(
            c for c in light_service.characteristics
            if c.uuid == '00001525-1212-efde-1523-785feabcd123')

        
        light_characteristic.write_value([0])
        light_characteristic.read_value()
        

    def characteristic_value_updated(self, characteristic, value):
        print("Firmware version:", value)
        
    def switch(self, val):
        self.light_characteristic.write_value([val])


device = AnyDevice(mac_address='D6:43:18:ED:C3:0F', manager=manager)
device.connect()
manager.run()

while(1):
    switch(device, 0)
    sleep(1)
    switch(device, 1)
    sleep(1)


    
    