#!/usr/bin/python
# -*- coding: utf-8 -*-

#  http://stackoverflow.com/questions/37913415/list-all-json-pointers-and-skip-common-decoding-errors

import json,sys

input_json_str = ""

if(len(sys.argv)==1):
    # read from stdin
    input_json_str = sys.stdin.read()
else:
    # read from file
    input_json_str = open(sys.argv[1], 'r').read()
    
obj=json.loads(input_json_str) # TODO: better handle decoding errors (create a custom JSONDecoder?)

#2FIX(not working with top level lists): print("fileinfo: number of top-level entries: " + str(len(obj.keys())))  # TODO: print more infos?

def myprint(d,path=""):
	if(isinstance(d, dict)):
		for k, v in d.items():
			newpath=path + "/" + k
			print(newpath)
			myprint(v,newpath)
	if(isinstance(d, list)):
		for i in range(len(d)):
			newpath=path + "/" + str(i)
			print(newpath)
			myprint(d[i],newpath)

myprint(obj)
