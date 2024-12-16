#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

PROGRAM_NAME = os.path.basename(sys.argv[0])

import socket
HOSTNAME=socket.gethostname()  # default name used if unspecified

def resolve_with_slimdns(hostname):
	# pip install https://github.com/nickovs/slimDNS
	from slimDNS import SlimDNSServer
	#server = SlimDNSServer("127.0.0.1", "localhost")
	local_addr = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])  # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib#answer-1267524
	server = SlimDNSServer(local_addr, "test")
	host_address_bytes = server.resolve_mdns_address(hostname)
	return(host_address_bytes)
    
    
def resolve_with_zeroconf(hostname):
	# derived from https://github.com/python-zeroconf/python-zeroconf/blob/master/examples/resolver.py
	# TODO: https://github.com/python-zeroconf/python-zeroconf/issues/129
	TYPE = '_test._tcp.local.'

	#logging.basicConfig(level=logging.DEBUG)
	#logging.getLogger('zeroconf').setLevel(logging.DEBUG)

	zeroconf = Zeroconf()
	print(zeroconf.get_service_info(TYPE, hostname + '.' + TYPE))

	zeroconf.close()
        
        

if __name__ == "__main__":
	
	if(len(sys.argv) == 0 or sys.argv[1] in ['-h', '--help']):
		print("usage: " + PROGRAM_NAME + " HOSTNAME")
		sys.exit(1)
	
	hostname = sys.argv[1]

	# try with system resolver first
	try:
		import socket
		r = socket.gethostbyname(hostname[0:-1])
		print(r)
	except:
		pass

	try:
		r = resolve_with_zeroconf(hostname)
		print(r)
	except:
		pass

	try:
		r = resolve_with_slimdns(hostname)
		print(r)
	except:
		pass