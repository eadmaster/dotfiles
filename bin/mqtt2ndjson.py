#!/usr/bin/python

import paho.mqtt.subscribe as subscribe
import json
import sys

HOSTNAME="localhost"
if(len(sys.argv)==2):
	HOSTNAME=sys.argv[1]

print("subscribing to all topics on " + HOSTNAME + " for MQTT msgs...")

while(True):
	msg = subscribe.simple("#", hostname="localhost")
	d = { "topic" : str(msg.topic), "payload" : str(msg.payload.decode()) }
	print(json.dumps(d))
