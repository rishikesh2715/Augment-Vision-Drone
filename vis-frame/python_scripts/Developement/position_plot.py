# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:22:20 2020

@author: Lars
"""

import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt

longtitude=[]
lattitude=[]
    
# MQTT    
MQTT_SERVER = "192.168.0.214"
MQTT_PATH = "data/gps/#"

count = 1 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("position visualization script connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    # get your data
    
    #print(msg.topic)
    #print(type(msg.topic))
    #print(type(msg.payload))
    #print((msg.payload))
    #var = msg.topic.replace("/",".")
    #print(var)
    #isinstance(var, str)
    
    #print(msg.topic == 'data/gps/lat')

    if msg.topic == 'data/gps/lon':
        longtitude.append(float(msg.payload))

    if msg.topic == 'data/gps/lat':
        lattitude.append(float(msg.payload))
        
    if len(longtitude) == len(lattitude):
        fig = plt.figure(figsize=(15, 10))
        plt.ioff()
        plt.plot(longtitude, lattitude, label='position', color = 'r')
        plt.close(fig)
        fig.savefig("openmct_v1_0\example\imagery\DG_800_Position.jpg")
        
        
    
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()