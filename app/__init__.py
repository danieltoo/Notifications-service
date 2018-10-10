# coding=utf-8
import os
from flask import Flask, render_template,jsonify,request,abort,redirect,g,url_for
from flask_socketio import SocketIO, send, emit
from functools import wraps
import crypt
import random
import datetime
import config
import json
from app.Client import SmartClient
from app.Functions import determinateZone
from app.Notifications import Notifications
from flask_cors import CORS
from crate import client as crate

connection = crate.connect("http://35.196.174.137:4200")

client = SmartClient() 
noti = Notifications()
app = Flask(__name__,static_url_path='/static')
CORS(app)
socketio = SocketIO(app)

globalCode = crypt.crypt(config.username, config.password)

@socketio.on('registre')
def test_registre(body, methods=['GET', 'POST']):
    print("New Code" , body["code"])
    code = body["code"]
    if (body["username"] == config.username and body["password"] == config.password) :
        emit(code, globalCode)
    else :
        emit(code, False)
    return 

@app.route('/')
def index():
    return render_template('./index.html') 

@app.route('/notify', methods=['POST'])
def notify():  
    print ("Alerta Recibida")
    alert = request.json["data"][0]  # Extraer datos de la alerta
    socketio.emit('alert:' + globalCode, alert, broadcast=True)  #Envía todas las alertas
    print(alert)
    zones  = client.getZones()
    inzone = determinateZone(alert["location"], zones) #Determinar el campus en el que se encuentra

    if (inzone != {} ): 
        socketio.emit('alert:' + inzone["idZone"], alert, broadcast=True) #Envía alertas de zona 
        allTokens = []
        devicesNear = []
        tokens = []
        devices = []
        devicesOnZone = client.getDevicesOnZone(inzone["idZone"]) #Determinar lista  de dispositivos en el campus        

        if alert["alertSource"].find("Device_Smartphone_") != -1: #Determinar si la alerta es de Smartphone
            allTokens = client.getTokens()
            devicesNear = client.getDevicesNear(alert["location"]) # Determina tokens de dispositivos cercanos
        else:
            allTokens = client.getTokens("All")
        tokens, devices = noti.clearTokens(alert["alertSource"], devicesNear, devicesOnZone, allTokens)
        if (len(devices) > 0):
            noti.sendNotifications(alert, tokens, devices) # Envía notificacionesa dispositivos
        else :
            print("No se encontraron dispositivos en el campus o cercanos a la alerta")
        
    else :
        print("La alerta se generó fuera de un campus")
    return jsonify("OK"),201

@app.route('/alerts/count/zone', methods=['GET'])
def alertsCountZone():
    cursor = connection.cursor()
    cursor.execute("select etbuilding.entity_id, etbuilding.owner , count(*)  as total from etalert, etbuilding where within(etalert.location, etbuilding.location) GROUP BY etbuilding.entity_id, etbuilding.owner")
    result = cursor.fetchall()
    jsonResult = {}
    return json.dumps(result), 200

@app.route('/alerts/count/category', methods=['GET'])
def alertsCountCategory():
    cursor = connection.cursor()
    cursor.execute("select count(*), etalert.category from etalert group by etalert.category")
    result = cursor.fetchall()
    return json.dumps(result), 200

@app.route('/alerts/count/subcategory', methods=['GET'])
def alertsCountSubategory():
    cursor = connection.cursor()
    cursor.execute("select count(*), etalert.subcategory from etalert group by etalert.subcategory")
    result = cursor.fetchall()
    return json.dumps(result), 200

@app.route('/alerts/count/severity', methods=['GET'])
def alertsCountSeverity():
    cursor = connection.cursor()
    cursor.execute("select count(*), etalert.severity from etalert group by etalert.severity")
    result = cursor.fetchall()
    jsonResult = {}
    for item in result:
        jsonResult[item[1]] = item[0]
    return json.dumps(jsonResult), 200

@app.route('/alerts/count/context/zone', methods=['GET'])
def alertsCountContextZone():
    zones  = client.getZones()
    data = []
    for zone in zones :
        alerts, headers = client.getHistoryAlerts(zone["idZone"])
        print( headers['Fiware-Total-Count'])
        data.append([zone["idZone"], zone["name"] , int(headers['Fiware-Total-Count'])])
    return json.dumps(data), 200    



    



