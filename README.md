# DrivingApp-Service-Python

### Install requirements 
```
  pip install -r requirements.txt
 
```

### Run with Flask

```
  Windows
  set FLASK_APP=run.py

  Unix
  export FLASK_APP=run.py
```

```
  flask run
```

### Run with python

```
  python run.py
```

### Run with gunicorn 

```
  gunicorn app:app
```

## API

***POST /login*** obtain the token from keystone
```json
  {
    'email': 'email',
    'password' : 'password'
  }
```
Response  

```json
  {
    'token': '<token>'
  }
```

***GET /user/&lt;email&gt;*** get user data <br>
example : https://drivingapp-python.herokuapp.com/user/torresestradaniel@gmail.com  <br> 

***GET /alertsCampus/&lt;campus&gt;*** get the last ten alerts from the campus <br> 
example : https://drivingapp-python.herokuapp.com/alertsCampus/5a08f54972a5b81a7d040119  <br> 
***GET /alertsZone/&lt;zone&gt;*** get the last ten alerts from the zone <br>
example : https://drivingapp-python.herokuapp.com/alertsZone/5a16291509cb5f76e6b21f78  <br> 
***GET /devicesCampus/&lt;campus&gt;*** get all devices on the campus in the last 15 minutes <br>
example : https://drivingapp-python.herokuapp.com/devicesCampus/5a08f54972a5b81a7d040119  <br> 
***GET /devicesZone/&lt;zone&gt;*** get all devices on the zone  in the last 15 minutes <br>
example : https://drivingapp-python.herokuapp.com/devicesZone/5a16291509cb5f76e6b21f78  <br> 
  
