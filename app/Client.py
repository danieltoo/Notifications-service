import requests
import json
import config

""" This class make the request to the DrivingApp Service"""
class SmartClient (object): 

    def getZones(self):
        """ This function retrieve the zones registered """
        zones = requests.get("{}/api/zone?status=1".format(config.smart))
        return zones.json()

    def getRoads(self, responsible): 
        """ This function retrieve the roads registered """
        roads = requests.get("{}/api/road?status=1&responsible={}".format(config.smart, responsible))
        return roads.json()

    def getRoadSegments(self, refRoad):
        """ This function retrieve the road segments registered """
        roadsSegments = requests.get("{}/api/road?status=1&refRoad={}".format(config.smart, refRoad))
        return roadsSegments.json()

    def getDevicesNear(self, location):
        """ This function retrieve the devices near from the Orion"""
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
        """ This function retrieve the devices on the zone"""
        print("{}/service/devices/zone/{}".format(config.smart, zone))
        devicesList = requests.get("{}/service/devices/zone/{}".format(config.smart, zone))
        #Get all devices  
        """body = {
            "id" : "Device_Smartphone_.*",
            "type" : "Device",
            "options" : "keyValues"
        }
        devicesList = requests.post("{}/service/query".format(config.smart),data=body)
        """
        return devicesList.json()

    def getTokens(self, type = None):
        """ This function retrieve the device tokens registered"""
        tokenDevices = requests.get("{}/api/device/token?status=1".format(config.smart)).json()
        tempTokens = []
        if type != None:
            for token in tokenDevices :
                if token["preferences"] == type:
                    tempTokens.append(token)
        else :
            tempTokens = tokenDevices
        return tempTokens
    
    def query(self, _json):
        """ This function make a query request to the Orion """
        result = requests.post("{}/service/query".format(config.smart),data=json.dumps(_json))
        return result

    def getHistoryAlerts(self, idZone):
        """ This function retrieve the Alerts from the Orion """
        alerts = requests.get("{}/service/alerts/zone/history/{}?id=Alert:Device_Smartphone_.*&location=false".format(config.smart, idZone))
        return alerts.json(), alerts.headers