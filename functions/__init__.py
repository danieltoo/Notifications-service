import json
import math
import requests
import config

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

def getTokens() :
    tokenDevices = requests.get("http://{}/api/device/token".format(config.smart))
    return tokenDevices.json()
    
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
def distance(start, end):
    rlat0 = math.radians(start[0])
    rlng0 = math.radians(start[1])
    rlat1 = math.radians(end[0])
    rlng1 = math.radians(end[1])
    latDelta = rlat1 - rlat0
    lonDelta = rlng1 - rlng0
    distance = 6371000 * 2 * math.asin(
        math.sqrt(
            math.cos(rlat0) * math.cos(rlat1) * math.pow(math.sin(lonDelta / 2), 2) +
            math.pow(math.sin(latDelta / 2), 2)
        )
    )
    return distance 

def inRoad (start, end, point, width):
    width = width / 2
    area  = (distance(start, end) * width) / 2
    a = distance (start, point)
    b = distance (point, end)
    c = distance (start, end)
    s = (( a + b + c ) / 2)
    ap = math.sqrt(
        (s * (s - a ) ) * ( ( s - b ) * ( s - c ) )
    )
    if (ap < area) : 
        return True 
    else: 
        return False

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




def sendNotifications(alert , tokens, devices):
    body = {
        "notification": {
            "title": alert["subCategory"],
            "body": alert["description"]
        },
        "data": {
           "location" : alert["location"]
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
    return




   

