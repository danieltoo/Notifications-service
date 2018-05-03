import requests
import json
import config

class SmartClient (object): 

    def getZones(self):
        zones = requests.get("http://{}/api/zone?status=1".format(config.smart))
        return zones.json()

    def getRoads(self, responsible): 
        roads = requests.get("http://{}/api/road?status=1&responsible={}".format(config.smart, responsible))
        return roads.json()

    def getRoadSegments(self, refRoad):
        roadsSegments = requests.get("http://{}/api/road?status=1&refRoad={}".format(config.smart, refRoad))
        return roadsSegments.json()

    def getDevicesNear(self, location):
        body = {
            "id" : "Device_Smartphone_.*",
            "type" : "Device",
            "georel" : "near;maxDistance:100",
            "geometry" : "point",
            "coords" : location
        }
        entities = requests.post("http://{}/service/query".format(config.smart),data=body)
        return entities.json()

    def getDevicesOnZone(self, zone):
        print("http://{}/service/devices/zone/{}".format(config.smart, zone))
        devicesList = requests.get("http://{}/service/devices/zone/{}".format(config.smart, zone))
        return devicesList.json()

    def getTokens(self):
        tokenDevices = requests.get("http://{}/api/device/token".format(config.smart))
        return tokenDevices.json()
    