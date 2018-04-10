import requests
import config
import json



def pointOnZone(x, y, polygon):
    i = 0
    j = len(polygon) - 1
    salida = False
    for i in range(len(polygon)):
        if (polygon[i][1] < y and polygon[j][1] >= y) or (polygon[j][1] < y and polygon[i][1] >= y):
            if polygon[i][0] + (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) * (polygon[j][0] - polygon[i][0]) < x:
                salida = not salida
        j = i
    return salida  

def matchTokens (devicesList, tokenDevices , preference = None):
    tokens  = []
    for dev in devicesList :
        for token in tokenDevices:
            if(token["refDevice"] == dev["id"]):
                if preference != None : 
                    if token["preferences"] == preference:
                        tokens.append(token)   
                else : 
                    tokens.append(token) 
    return tokens

def clearTokens(near, onZone):
    temp = {}
    for devNear in near :
        temp[devNear ["refDevice"]] = devNear["fcmToken"]
    for devZone in onZone : 
        temp[devZone ["refDevice"]] = devZone["fcmToken"]
    array = []
    devices = []
    for device in temp :
        array.append(temp[device])
        devices.append(device)
    return array, devices



def determinateZone (location):
    zones = requests.get("http://{}/api/zone".format(config.smart))
    inzone = {}
    for zone in zones.json():  
        loc = location.split(',')
        point = pointOnZone (float(loc[0]), float(loc[1]), zone["location"] )
        if (point) : 
            inzone = zone
            print ("Alerta sucitada en ", zone["name"])
    return inzone


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
    return matchTokens(devicesList.json() , allTokens, "All")

def getTokens() :
    tokenDevices = requests.get("http://{}/api/device/token".format(config.smart))
    return tokenDevices.json()


def sendNotifications(alert , tokens, devices):
    body = {
        "notification": {
            "title": alert["category"],
            "body": alert["description"]
        }
    }
    headers = {
        "Content-Type":"application/json",
        "Authorization":'key=' + config.fcm
    }
    print(headers)
    index = 0 
    for token in tokens :
        body["to"] = token
        res = requests.post("http://fcm.googleapis.com/fcm/send",data=json.dumps(body),headers=headers)
        print (res, devices[index])
        index += 1
    print ("Sending Notifications")
    return


