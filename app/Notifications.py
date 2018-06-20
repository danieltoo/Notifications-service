import requests
import json
import config 

class Notifications (object) : 

    def matchTokens (self, devicesList, tokenDevices , preference = None):
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

    def clearTokens(self, near, onZone, allTokens):
        near = self.matchTokens(near, allTokens)
        onZone = self.matchTokens(onZone, allTokens, "All")
        temp = {}
        print("DEVICES ON ZONE")
        for devNear in near :
            temp[devNear ["refDevice"]] = devNear["fcmToken"]
            print(devNear["refDevice"])
        print("DEVICES NEAR")
        for devZone in onZone : 
            temp[devZone ["refDevice"]] = devZone["fcmToken"]
            print(devZone["refDevice"])

        array = []
        devices = []
        for device in temp :
            array.append(temp[device])
            devices.append(device)

        return array, devices

    def sendNotifications(self, alert , tokens, devices):
        body = {
            "notification": {
                "title": alert["subCategory"],
                "body": alert["description"],
                "color": '#6563A4'
            },
            "data": {
            "alert" : alert
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
