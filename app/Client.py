import requests
import json
import config

class SmartClient (object): 

    def getZones(self):
<<<<<<< HEAD
        zones = requests.get("http://{}/api/zone?status=1".format(config.smart))
        print zones
=======
        zones = requests.get("{}/api/zone?status=1".format(config.smart))
>>>>>>> master
        return zones.json()

    def getRoads(self, responsible): 
        roads = requests.get("{}/api/road?status=1&responsible={}".format(config.smart, responsible))
        return roads.json()

    def getRoadSegments(self, refRoad):
        roadsSegments = requests.get("{}/api/road?status=1&refRoad={}".format(config.smart, refRoad))
        return roadsSegments.json()

    def getDevicesNear(self, location):
        body = {
            "id" : "Device_Smartphone_.*",
            "type" : "Device",
            "georel" : "near;maxDistance:100",
            "geometry" : "point",
            "coords" : location
        }
        entities = requests.post("{}/service/query".format(config.smart),data=body)
        return entities.json()

    def getDevicesOnZone(self, zone):
<<<<<<< HEAD
        print("http://{}/service/devices/zone/{}".format(config.smart, zone))
        devicesList = requests.get("http://{}/service/devices/zone/{}".format(config.smart, zone))
=======
        print("{}/service/devices/zone/{}".format(config.smart, zone))
        devicesList = requests.get("{}/service/devices/zone/{}".format(config.smart, zone))
>>>>>>> master
        #Get all devices  
        """body = {
            "id" : "Device_Smartphone_.*",
            "type" : "Device",
            "options" : "keyValues"
        }
<<<<<<< HEAD
        devicesList = requests.post("http://{}/service/query".format(config.smart),data=body)
=======
        devicesList = requests.post("{}/service/query".format(config.smart),data=body)
>>>>>>> master
        """
        return devicesList.json()

    def getTokens(self, type = None):
        tokenDevices = requests.get("{}/api/device/token?status=1".format(config.smart)).json()
        tempTokens = []
        if type != None:
            for token in tokenDevices :
                if token["preferences"] == type:
                    tempTokens.append(token)
        else :
            tempTokens = tokenDevices
        return tempTokens
    
    def createSuscription(self):
        pass
    
    def query(self, _json):
        result = requests.post("{}/service/query".format(config.smart),data=json.dumps(_json))
        return result

    def getHistoryAlerts(self, idZone):
        alerts = requests.get("{}/service/alerts/zone/history/{}?id=Alert:Device_Smartphone_.*&location=false".format(config.smart, idZone))
        return alerts.json(), alerts.headers