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