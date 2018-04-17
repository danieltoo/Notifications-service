import requests
import config

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