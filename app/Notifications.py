import requests
import json
import config 

""" This class work the device tokens and send the notifications"""
class Notifications (object) : 

    def matchTokens (self, devicesList, tokenDevices):
        """ This function match the device with its token"""
        tokens  = []
        for dev in devicesList :
            for token in tokenDevices:
                if(token["refDevice"] == dev["id"]):
                    tokens.append(token) 
        return tokens

    def clearTokens(self, alertSource, near, onZone, allTokens):
        """ This function delete repeated devices tokens"""
        near = self.matchTokens(near, allTokens)
        onZone = self.matchTokens(onZone, allTokens)

        temp = {}
        for devNear in near :
            temp[devNear ["refDevice"]] = devNear["fcmToken"]

        for devZone in onZone : 
            temp[devZone ["refDevice"]] = devZone["fcmToken"]

        array = []
        devices = []
        for device in temp :
            if (device != alertSource) :
                array.append(temp[device])
                devices.append(device)
                

        return array, devices

    def sendNotifications(self, alert , tokens, devices):
        """ This function Send the notifications """

        # Add the color depending the severity
        color = ""
        if(alert["severity"] == "informational"):
            color = "#3498db"
        if(alert["severity"] == "low"):
            color = "#2c3e50"
        if(alert["severity"] == "medium"):
            color = "#f1c40f"
        if(alert["severity"] == "high"):
            color = "#e67e22"
        if(alert["severity"] == "critical"):
            color = "#c0392b"

        # Make the notification
        body = {
            "notification": {
                "title": alert["category"],
                "body": alert["subCategory"],
                "color": color

            },
            "data": {
                "alert" : alert
            },
            "ttl": 3600
        }
        headers = {
            "Content-Type":"application/json",
            "Authorization":'key=' + config.fcm
        }
        
        index = 0 
        devices_notificated  = []
        # Send the notification to each device 
        for token in tokens :
            body["to"] = token
            res = requests.post("http://fcm.googleapis.com/fcm/send",data=json.dumps(body),headers=headers)
            #print (res, devices[index])
            devices_notificated.append(devices[index])
            index += 1
        return devices_notificated
