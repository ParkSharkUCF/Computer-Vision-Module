import sys
import requests

class parkApi:
    def __init__(self):
        parkApi.url = 'https://murmuring-waters-47073.herokuapp.com/'

    def createSensor(self, body):
        url = parkApi.url + 'sensor/'
        return self.post_request(url, body)

    def findSensorByID(self, id):
        url = parkApi.url + 'sensor/' + str(id)
        return self.get_request(url)

    def getAllSensors(self):
        url = parkApi.url + 'sensor/'
        return self.get_request(url)

    def updateSensorByID(self, id, body):
        url = parkApi.url +'sensor/' + str(id)
        return self.patch_request(url, body)

    def post_request(self, url, body):
        try:
            r = requests.post(url, json=body)
        except requests.exceptions.RequestException as e:
            print('ERROR: Unable to connect to ' + url)
            sys.exit(1)

        if r.status_code == 200:
            return r.json()
        else:
            print('ERROR: Bad Response: ' + str(r.status_code))
            sys.exit(1)

    def get_request(self, url):
        try:
            r = requests.get(url)
        except requests.exceptions.RequestException as e:
            print('ERROR: Unable to connect to ' + url)
            sys.exit(1)

        if r.status_code == 200:
            return r.json()
        else:
            print('ERROR: Bad Response: ' + str(r.status_code))
            sys.exit(1)

    def patch_request(self, url, body):
        try:
            r = requests.patch(url, json=body)
        except requests.exceptions.RequestException as e:
            print('ERROR: Unable to connect to ' + url)
            sys.exit(1)

        if r.status_code == 200:
            return r.json()
        else:
            print('ERROR: Bad Response: ' + str(r.status_code))
            sys.exit(1)

# create sesnor
def create_sensor(body):
    api = parkApi()
    return api.createSensor(body)

# return sensor data by ID
def retrieve_sensor(id):
    api = parkApi()
    return api.findSensorByID(id)

def retrieve_all_sensors():
    api = parkApi()
    return api.getAllSensors()

# update sensor data by ID
def update_sensor(id, body):
    api = parkApi()
    return api.updateSensorByID(id, body)
