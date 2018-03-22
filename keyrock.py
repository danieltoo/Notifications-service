#Import the keystone API fiware version
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
import requests
import json
import datetime


idm = {
    "id_admin" : "idm_user",
    "password" : "idm",
    "idm_project": "idm_project",
    #"idm_host" : "localhost:35357"
    "idm_host" : "207.249.127.96:35357"
}


headers = {
	"accept": "application/json",
	"accept-encoding": "gzip, deflate",
	"accept-language": "en-US,en;q=0.8",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
	"content-type": "application/json"
}

keystone = None

def autorization():
    global keystone
    auth = v3.Password(auth_url='http://{}/v3'.format(idm["idm_host"])
,
        user_id=idm['id_admin'],
        password=idm['password'],
        project_id=idm['idm_project'])

    sess = session.Session(auth=auth)
    keystone = client.Client(session=sess)
    return keystone

def login (name ,password ,domain_id= "default" ):
	#global headers, keyrock

	payload  = {
	    "auth": {
	        "identity": {
	            "methods": [
	                "password"
	            ],
	            "password": {
	                "user": {
	                    "domain": {
	                        "id": domain_id
	                    },
	                    "name": name,
	                    "password": password
	                }
	            }
	        }
	    }
	}


	url = "http://{}/v3/auth/tokens".format(idm["idm_host"])
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	token = r.headers['X-Subject-Token']
	return token


def getUsers(username = None):
    users = []
    if username != None:
        users = keystone.users.find(username=username)
    else :
        users = keystone.users.list()
    return users
    
def sign_up(username, email, password, activate = False):
    user = keystone.user_registration.users.register_user(
        name=email,
        password=password,
        username=username,
        domain='default')
    if activate:
        user = activate_user(user.id, user.activation_key)
    return user 
def activate_user( id, activation_key = None ):
    if activation_key == None :
        activation_key = keystone.user_registration.activation_key.new_activation_key(id)
    user = keystone.user_registration.users.activate_user(
        user=id,
        activation_key=activation_key)
    return user
def delete_user(username):
    keystone.users.delete(username)
    return 




#autorization() #Autorizacion keystone

"""
# Crea usuario 
new_user = sign_up(
    username="daniel",
    email="miotrocorreo@gmail.com", 
    password="mypass")

# Crea y activa usuario 
#user = sign_up(
#    username="daniel",
#    email="miotrocorreo@gmail.com",
#    password="mypass", 
#    activate=true) 

print "Usuario creado!" + str(new_user)

users = getUsers() #Obtiene todos los usuarios

user = getUsers("daniel") #Obtiene un usuario

#activa nuevo usuario
activate_user(
    new_user.id, 
    new_user.activation_key)

#activa usuario que no cuenta con activation key
activate_user(user.id) 

delete_user(user.id) #Elimina usuario 

"""


