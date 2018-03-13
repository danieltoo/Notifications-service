#Import  Flask
import os
from flask import Flask, render_template,jsonify,request,abort
import json
import requests
import Orion
import keyrock
import datetime

"""
keyrock.autorization()
print keyrock.getUsers()
"""
client  = Orion.Client("130.206.113.226")

app = Flask(__name__ )


@app.route('/')
def index():
    return render_template('./index.html')  

@app.route('/login', methods=['POST']) # Realiza Login del usuario con el IDM
def login():
    if not request.json:
        abort(400)
    token  = keyrock.login(request.json['email'], request.json['password'] )
    return json.dumps({"token" : token}), 200

@app.route('/user/<email>') #Obtiene datos del usuario con el otro servicio
def getUser(email):
    r = requests.get("https://smartsdk-web-service.herokuapp.com/api/user?email={}".format(email))
    return jsonify(r.json()), 200

@app.route('/alertsCampus/<campus>') # Ultimas 10 alertas en el campus 
def alertsCampus(campus):
    #Obtener coordenadas del campus --- SOLUCION TEMPORAL FALTA HACER PETICION AL CONTEXT 
    camp = requests.get("http://driving-monitor-service.herokuapp.com/api/campus/{}".format(campus))
    location  = camp.json()["location"]
    #Conversion de las coordenadas a cadena
    location = ";".join( "{},{}".format(coords[0], coords[1])  for coords in location)
    #Request paa obtener el numero total de alertas en el campus
    reqCount = client.get("entities?id=Alert:Device_Smartphone_.*&type=Alert&options=count&georel=coveredBy&geometry=polygon&coords={}".format(location))
    count  = reqCount.headers['fiware-total-count']
    offset = 0
    print (count)
    count = int(count)
    if count > 10 :
        offset = count - 10
    #Request de alertas en el campus 
    query = "entities?id=Alert:Device_Smartphone_.*&type=Alert&options=keyValues&georel=coveredBy&geometry=polygon&coords={}&limit=10&offset={}".format(location, str(offset))
    alerts = client.get(query).json()
    #Respuesta de las alertas en el campus
    return jsonify(alerts), 200 

@app.route('/alertsZone/<zone>') # Ultimas 10 alertas en el campus 
def alertsZone(zone):
    #Obtener coordenadas del zone --- SOLUCION TEMPORAL FALTA HACER PETICION AL CONTEXT 
    zon = requests.get("http://driving-monitor-service.herokuapp.com/api/zones/{}".format(zone))
    location  = zon.json()["location"]
    #Conversion de las coordenadas a cadena
    location = ";".join( "{},{}".format(coords[0], coords[1])  for coords in location)
    #Request paa obtener el numero total de alertas en el campus
    reqCount = client.get("entities?id=Alert:Device_Smartphone_.*&type=Alert&options=count&georel=coveredBy&geometry=polygon&coords={}".format(location))
    count  = reqCount.headers['fiware-total-count']
    offset = 0
    count = int(count)
    if count > 10 :
        offset = count - 10
    #Request de alertas en el campus 
    query = "entities?id=Alert:Device_Smartphone_.*&type=Alert&options=keyValues&georel=coveredBy&geometry=polygon&coords={}&limit=10&offset={}".format(location, str(offset))
    alerts = client.get(query).json()
    #Respuesta de las alertas en el campus
    return jsonify(alerts), 200 

@app.route('/devicesCampus/<campus>') # Devices en el campus
def devicesCampus(campus):
    #Obtener coordenadas del campus --- SOLUCION TEMPORAL FALTA HACER PETICION AL CONTEXT 
    camp = requests.get("http://driving-monitor-service.herokuapp.com/api/campus/{}".format(campus))
    location  = camp.json()["location"]
    #Conversion de las coordenadas a cadena
    location = ";".join( "{},{}".format(coords[0], coords[1])  for coords in location)
    fifago = (datetime.datetime.now() - datetime.timedelta(minutes=15))
    print (fifago.isoformat())
    #Request de alertas en el campus 
    query = "entities?id=Device_Smartphone_.*&type=Device&options=keyValues&georel=coveredBy&geometry=polygon&coords={}&q=dateModified>={}".format(location, fifago.isoformat())
    devices = client.get(query).json()
    #Respuesta de las alertas en el campus
    return jsonify(devices), 200 

@app.route('/devicesZone/<zone>') # Devices en el campus
def devicesZone(zone):
    #Obtener coordenadas del zone --- SOLUCION TEMPORAL FALTA HACER PETICION AL CONTEXT 
    zon = requests.get("http://driving-monitor-service.herokuapp.com/api/zones/{}".format(zone))
    location  = zon.json()["location"]
    #Conversion de las coordenadas a cadena
    location = ";".join( "{},{}".format(coords[0], coords[1])  for coords in location)
    fifago = (datetime.datetime.now() - datetime.timedelta(minutes=15))
    print (fifago.isoformat())
    #Request de alertas en el campus 
    query = "entities?id=Device_Smartphone_.*&type=Device&options=keyValues&georel=coveredBy&geometry=polygon&coords={}&q=dateModified>={}".format(location, fifago.isoformat())
    devices = client.get(query).json()
    #Respuesta de las alertas en el campus
    return jsonify(devices), 200 


@app.route('/notify', methods=['POST'])
def notify():
    if not request.json:
        abort(400)
    else : 
        # Extraer datos de la alerta
        #Determinar el campus en el que se encuentra
        # if campus !== undefined
        #       Envía alerta a Driving Monitor Web APP
        #       Almacena alerta en la base de datos
        #       Determinar lista de dispositivos en el campus
        #       devicesList.length > 0 
        #           Determinar lista tokens de los dispositivos para enviar a Firebase
        #           tokensList.length > 0
        #               Enviar la lista de tokens a firebase 
        return jsonify({ 'ok' :  'ok'}),201



  

    

    







