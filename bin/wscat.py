#!/usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
import _thread
import time
import sys
import ssl

if __name__ == "__main__":
	#HOSTNAME="echo.websocket.events"
	HOSTNAME="ws://localhost:9001/mqtt"  # mosquitto
	if(len(sys.argv)==2):
		HOSTNAME=sys.argv[1]

	#websocket.enableTrace(True)
	
	ws = websocket.create_connection(HOSTNAME, sslopt={"check_hostname": False, "cert_reqs": ssl.CERT_NONE})
	
	if ws.connected:
		print("connected to " + HOSTNAME + ", listening for ws msgs...")
	else:
		print("could not connect")
		sys.exit(1)
	
	#ws.recv()
	#ws.send("Hello, World")
	while(True):
		result = ws.recv()
		print(result.rstrip())
	
	ws.close()
