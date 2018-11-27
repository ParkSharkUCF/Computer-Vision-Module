import pygatt
import api

from time import sleep,time

print("Starting...")

# defines
ADDR_TYPE = pygatt.BLEAddressType.random

SENSOR1_MAC = 'D6:43:18:ED:C3:0F'
SENSOR1_SENSORID = '2C'
SENSOR1_SPOTID = 4
SENSOR2_MAC = 'D1:C6:CC:9D:30:72'
SENSOR2_SENSORID = '3C'
SENSOR2_SPOTID = 5
SENSOR3_MAC = 'D1:48:F2:47:A4:06'
SENSOR3_SENSORID = '4C'
SENSOR3_SPOTID = 6

CHAR_SENSORID_RW = '00001524-1212-efde-1523-785feabcd123'
CHAR_PARKSTATUS_R = '00001525-1212-efde-1523-785feabcd123'
CHAR_SLEEPINTERVAL_RW = '00001526-1212-efde-1523-785feabcd123'
CHAR_BATTERYALERT_R = '00001527-1212-efde-1523-785feabcd123'

# init bluetooth adapter
print("Init adapter")
adapter = pygatt.GATTToolBackend()
adapter.start()

# connect to sensors
print("Connecting to Sensor 1")
try:
	sensor1 = adapter.connect(SENSOR1_MAC, timeout=2, address_type = ADDR_TYPE)
	print("Connected")
except:
	sensor1 = None
	print("Cannot connect to Sensor 1.")

print("Connecting to Sensor 2")
try:
	sensor2 = adapter.connect(SENSOR2_MAC, timeout=2, address_type = ADDR_TYPE)
	print("Connected")
except:
	sensor2 = None
	print("Cannot connect to Sensor 2.")

print("Connecting to Sensor 3")
try:
	sensor3 = adapter.connect(SENSOR3_MAC, timeout=2, address_type = ADDR_TYPE)
	print("Connected")
except:
	sensor3 = None
	print("Cannot connect to Sensor 3.")

# ---Get Characteristics---
def update_spotstatus_1(handle, val):
	print("Sensor 1 says Parking Spot Status: " + val.hex() )
	res = api.update_sensor(SENSOR1_SENSORID, {'cars': val[0], 'lastUpdated': time(), 'spots': [{'spotID': SENSOR1_SPOTID, 'occupied': val[0]}]})


def update_spotstatus_2(handle, val):
        print("Sensor 2 says Parking Spot Status: " + val.hex() )
        res = api.update_sensor(SENSOR2_SENSORID, {'cars': val[0], 'lastUpdated': time(), 'spots': [{'spotID': SENSOR2_SPOTID, 'occupied': val[0]}]})


def update_spotstatus_3(handle, val):
        print("Sensor 3 says Parking Spot Status: " + val.hex() )
        res = api.update_sensor(SENSOR3_SENSORID, {'cars': val[0], 'lastUpdated': time(), 'spots': [{'spotID': SENSOR3_SPOTID, 'occupied': val[0]}]})


print("Registering Notification callback functions")
if sensor1 is not None:
	sensor1.subscribe(CHAR_PARKSTATUS_R, callback=update_spotstatus_1)
if sensor2 is not None:	
	sensor2.subscribe(CHAR_PARKSTATUS_R, callback=update_spotstatus_2)
if sensor3 is not None:
	sensor3.subscribe(CHAR_PARKSTATUS_R, callback=update_spotstatus_3)

print("Running...")

while(1):
	sleep(1)


