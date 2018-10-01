FROM python:2.7
#FROM python-flask
RUN mkdir /src
WORKDIR /src
#ADD *.py *.pyc /code/
#ADD SmartSecurity-Notifications/ /src/
COPY . /src
RUN pip install -r requirements.txt
#EXPOSE 3001
CMD python run.py

#docker run -ti --env="CONTEXT=130.206.113.226" --env="SMART_SERVICE=smartsecurity-webservice.herokuapp.com" --env="FCM_SERVER_TOKEN=OK" --env="PASSWORD=SM2" --env="USER_NAME=daniel" -p 3001:3001 todaniels/smartsecurity-notifications
