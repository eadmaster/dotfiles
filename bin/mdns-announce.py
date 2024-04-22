#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import socket

PROGRAM_NAME = os.path.basename(sys.argv[0])



def announce_forever_with_zeroconf(hostname):
	# https://github.com/python-zeroconf/python-zeroconf/blob/master/examples/registration.py
	# https://github.com/Winand/zeroconf-local-hostnames

	from zeroconf import Zeroconf, ServiceInfo
	zeroconf = Zeroconf()

	ip = socket.gethostbyname(socket.gethostname())

	service_info = ServiceInfo(
		"_http._tcp.local.",
		hostname + "._http._tcp.local.",
		addresses=[socket.inet_aton(ip)],
		port=80,  # customize
		properties={},
		server=hostname+".local"
	)
      
	zeroconf.register_service(service_info)

	print("announcing %s.local with python-zeroconf, CTRL-C to stop..." % hostname)
	import time
	
	try:
		while True:
			time.sleep(10)
	except KeyboardInterrupt:
		pass
	finally:
		# Unregister the service when the script is interrupted
		zeroconf.unregister_service(service_info)
		zeroconf.close()
		os._exit(0)


def announce_forever_with_slimdns(hostname):
	# pip install https://github.com/nickovs/slimDNS
	from slimDNS import SlimDNSServer
	#local_addr = socket.gethostbyname(HOSTNAME)
	local_addr = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])  # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib#answer-1267524
	print("announcing " + local_addr + " as " + hostname + ".local with slimDNS, CTRL-C to stop")
	server = SlimDNSServer(local_addr, hostname)
	server.run_forever()



if __name__ == "__main__":
	
	if(len(sys.argv) == 0 or sys.argv[1] in ['-h', '--help']):
		print("usage: " + PROGRAM_NAME + " [HOSTNAME]")
		sys.exit(1)
	
	hostname = sys.argv[1]
	
	#import socket
	#HOSTNAME=socket.gethostname()  # default name used if unspecified
	
	try:
		announce_forever_with_zeroconf(hostname)
	except:
		logging.exception("")
		
	try:
		announce_forever_with_slimdns(hostname)
	except:
		logging.exception("")
