# coding=utf-8
import os
from flask import Flask, render_template,jsonify,request,abort
from app.Client import SmartClient
from app.Functions import determinateZone
from app.Notifications import Notifications

client = SmartClient() 
noti = Notifications()

app = Flask(__name__)
@app.route('/')
def index():
    #return render_template('./index.html', name = "Your project name") 
    return jsonify( {"message" : "SmartSecurity Notifications is running"} ),200

@app.route('/notify', methods=['POST'])
def notify(): 
    print ("Alerta Recibida")
    alert = request.json["data"][0]  # Extraer datos de la alerta
    print (alert)
    zones  = client.getZones()
    inzone = determinateZone(alert["location"], zones) #Determinar el campus en el que se encuentra
    if (inzone != {} ): 
        print (inzone["idZone"])
        allTokens = client.getTokens() # Obtiene todos los tokens de dispositivos
        devicesOnZone = client.getDevicesOnZone(inzone["idZone"]) #Determinar lista de tokens de dispositivos en el campus        
        devicesNear = client.getDevicesNear(alert["location"]) # Determina tokens de dispositivos cercanos
        tokens, devices = noti.clearTokens(devicesNear, devicesOnZone, allTokens) # revisa tokens repetidos

        print (devices)
        if (len(devices) > 0):
            print("OK")
            noti.sendNotifications(alert, tokens, devices) # Envía notificacionesa dispositivos
        else :
            print("No se encontraron dispositivos en el campus o cercanos a la alerta")
    else :
        print("La alerta se generó fuera de un campus")
    return jsonify("OK"),201



  

    

    







