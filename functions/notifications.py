import config
import requests
import json

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