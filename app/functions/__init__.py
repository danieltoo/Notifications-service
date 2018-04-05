
import requests
import config
import json

def pointOnZone(x, y, poligono):
    i = 0
    j = len(poligono) - 1
    salida = False
    for i in range(len(poligono)):
        if (poligono[i][1] < y and poligono[j][1] >= y) or (poligono[j][1] < y and poligono[i][1] >= y):
            if poligono[i][0] + (y - poligono[i][1]) / (poligono[j][1] - poligono[i][1]) * (poligono[j][0] - poligono[i][0]) < x:
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

def getDevices(idZone) :
    devicesList = requests.get("http://{}/service/devices/zone/{}".format(config.smart,idZone))
    return devicesList.json()

def getTokens() :
    tokenDevices = requests.get("http://{}/api/device/token".format(config.smart))
    return tokenDevices.json()

def matchTokens (devicesList, tokenDevices):
    devices  = []
    for dev in devicesList :
        for token in tokenDevices:
            if(token["refDevice"] == dev["id"]):
                devices.append(token["fcmToken"])   
    return devices

def sendNotifications(alert , tokens):
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
	
    for token in tokens :
        body["to"] = token
        print(body)
        res = requests.post("http://fcm.googleapis.com/fcm/send",data=json.dumps(body),headers=headers)
        print (res)
    
    print ("Sending Notifications")
    return