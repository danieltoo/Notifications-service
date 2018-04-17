import requests
from tokens import matchTokens
import config

def getDevicesNear(location, allTokens):
    body = {
        "id" : "Device_Smartphone_.*",
		"type" : "Device",
        "georel" : "near;maxDistance:1000",
        "geometry" : "point",
        "coords" : location
    }
    entities = requests.post("http://{}/service/query".format(config.smart),data=body)
    return matchTokens(entities.json() , allTokens)

def getDevicesOnZone(idZone , allTokens) :
    devicesList = requests.get("http://{}/service/devices/zone/{}".format(config.smart,idZone))
    print ("http://{}/service/devices/zone/{}".format(config.smart,idZone))
    return matchTokens(devicesList.json() , allTokens, "All")