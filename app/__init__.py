# coding=utf-8
import os
from flask import Flask, render_template,jsonify,request,abort#
import functions
from functions import devices,notifications,roads,tokens,zones

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
    inzone = zones.determinateZone(alert["location"]) #Determinar el campus en el que se encuentra
    if (inzone != {} ): 
        print (inzone["idZone"])
        allTokens = tokens.getTokens() # Obtiene todos los tokens de dispositivos
        devicesOnZone = devices.getDevicesOnZone(inzone["idZone"], allTokens) #Determinar lista de tokens de dispositivos en el campus        
        devicesNear = devices.getDevicesNear(alert["location"] ,allTokens) # Determina tokens de dispositivos cercanos
        tokens, devices = tokens.clearTokens(devicesNear, devicesOnZone) # revisa tokens repetidos
        if (len(devices) > 0):
            notifications.sendNotifications(alert, tokens, devices) # Envía notificacionesa dispositivos
        else :
            print("No se encontraron dispositivos en el campus o cercanos a la alerta")
    else :
        print("La alerta se generó fuera de un campus")
    return jsonify("OK"),201



  

    

    







