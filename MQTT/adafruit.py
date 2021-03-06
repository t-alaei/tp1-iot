from umqtt import MQTTClient
import machine
import time
import math
import pycom
from temperature import get_temperature
import env

id_machine = machine.unique_id()
BROKER_ADDRESS="io.adafruit.com"
user = env.ADA_USER
password = env.ADA_PASSWORD
topic_temp = user +"/f/temp"
topic_switch = user + "/f/switch"
topic_potentio = user + "/f/potentio"


def sub_cb(topic, msg):
    pycom.heartbeat(False)

    #Renvoie la couleur vert si "ON"
    if msg == b"ON":
        pycom.rgbled(0x00ff00)
    
    #Renvoie la couleur rouge si "OFF"
    if msg == b"OFF":
        pycom.rgbled(0xff0000)

    print((topic, msg))


client = MQTTClient(id_machine, BROKER_ADDRESS, 1883, user, password)
pycom.heartbeat(False)

client.set_callback(sub_cb)
client.connect()

#Souscrit au topic switch
client.subscribe(topic_switch)

while True:
    #Check si il y a un message en attente
    client.check_msg()
    
    #Recuperation de la temperature et publication sur le topic temp
    b = str(get_temperature())
    client.publish(topic_temp, bytes(b, 'utf-8'))

    time.sleep(3)

client.disconnect()