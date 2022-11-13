#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import sys
import os
import sys
import psutil
import logging
import subprocess
from time import sleep

# set the default log level to DEBUG (default to WARNING, will skip INFO and DEBUG messages)
logging.getLogger().setLevel(logging.DEBUG)

import socket
HOSTNAME=socket.gethostname()

from sensors import *

MQTT_ROOT_ADDR = "sensors"

def publish_to_mqtt(name, value):
	logging.debug(name + ": " + str(value))
	client.publish(HOSTNAME + "/" + MQTT_ROOT_ADDR + "/" + name, value);
	
	
# main program
if __name__ == '__main__':

	MQTT_SERVER_ADDR="localhost"
	if(len(sys.argv)==2):
		MQTT_SERVER_ADDR=sys.argv[1]

	client = mqtt.Client()
	client.connect(MQTT_SERVER_ADDR, 1883, 60)  # host, port, keepalive

	print("logging hardware sensors to MQTT server on " + HOSTNAME + "...")

	try:
		while True:

			d = get_curr_sensors_dict()
			
			# print one value per line
			for k in d:
				publish_to_mqtt(k, d[k])

			sleep(3)

		# end of while
	except:
		import traceback
		traceback.print_exc(file=sys.stderr)

	client.disconnect();
