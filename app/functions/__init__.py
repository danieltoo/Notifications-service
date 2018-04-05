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

def getDevicesNear(location):
    body = {
        "id" : "Device_Smartphone_.*",
		"type" : "Device",
        "georel" : "near;maxDistance:1000",
        "geometry" : "point",
        "coords" : location
    }
    entities = requests.post("http://{}/service/query".format(config.smart),data=body)
    return  entities.json()


def getDevicesOnZone(idZone) :
    devicesList = requests.get("http://{}/service/devices/zone/{}".format(config.smart,idZone))
    return devicesList.json()

def getTokens() :
    tokenDevices = requests.get("http://{}/api/device/token".format(config.smart))
    return tokenDevices.json()

def matchTokens (devicesList, tokenDevices):
    tokens  = []
    devices = []
    for dev in devicesList :
        for token in tokenDevices:
            if(token["refDevice"] == dev["id"]):
                tokens.append(token["fcmToken"])   
                devices.append(dev["id"])
    return devices ,tokens

def sendNotifications(alert , tokens, devList):
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
    index =  0
    for token in tokens :
        body["to"] = token
        res = requests.post("http://fcm.googleapis.com/fcm/send",data=json.dumps(body),headers=headers)
        print (res, devList[index])
        index += 1
    
    print ("Sending Notifications")
    return


