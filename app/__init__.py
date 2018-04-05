# coding=utf-8
import os
from flask import Flask, render_template,jsonify,request,abort
import json
import requests
import Orion
import datetime
import functions

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('./index.html', name = "Your project name")  

@app.route('/notify', methods=['POST'])
def notify():
    print ("Alerta Recibida")
    alert = request.json["data"][0]  # Extraer datos de la alerta
    inzone = functions.determinateZone(alert["location"]) #Determinar el campus en el que se encuentra
    if (inzone != {} ):
        print (inzone["idZone"])
        devices = functions.getDevices("Zone_1522797798943") #Determinar lista de dispositivos en el campus
        if (len(devices) > 0):
            tokens = functions.getTokens() # Obtiene todos los tokens de dispositivos
            tokensDevices = functions.matchTokens(devices, tokens ) # Relaciona tokens con dispostivos
            if (len(tokensDevices) > 0):
                functions.sendNotifications(alert,tokensDevices) # Envía notificacionesa dispositivos
            else : 
                print("No se encontraron tokens de dispositivos que coicidan")
        else :
            print("No se encontraron dispositivos en el campus")
    else :
        print("La alerta se generó fuera de un campus")
    return jsonify("OK"),201



  

    

    







