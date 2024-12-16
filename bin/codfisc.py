#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pprint
import sys
import datetime

# pip install python-codicefiscale
from codicefiscale import codicefiscale

if __name__ == '__main__':
	# WIP argparse
	#import argparse, sys
	#parser = argparse.ArgumentParser()
	#subparsers = parser.add_subparsers()
	#encode_parser = subparsers.add_parser('encode')
	#encode_parser.add_argument("surname")
	#encode_parser.add_argument("name")
	#encode_parser.add_argument("sex")
	#encode_parser.add_argument("birthdate")
	#encode_parser.add_argument("birthplace")
	#decode_parser = subparsers.add_parser('decode')
	#decode_parser.add_argument("code")
	#args = parser.parse_args()
	
	if(len(sys.argv)==6):
		# encode mode
		try:
			surname=sys.argv[1]
			name=sys.argv[2]
			birthdate=sys.argv[3]  # ='03/04/1985'
			sex=sys.argv[4]
			birthplace=sys.argv[5]
			code = codicefiscale.encode(surname, name, sex, birthdate, birthplace)
			print(code)
		except:
			print("codicefiscale error: "+sys.exc_info()[1].args[0])
			exit(1)
		exit(0)
	
	elif(len(sys.argv)==2):
		# decode mode
		code=sys.argv[1]
		
		# check if well-formed
		if not codicefiscale.is_valid(code):
			print("codfisc: code is NOT valid")
			exit(1)
		pprint.pprint(codicefiscale.decode(code))
		exit(0)


	#else print usage
	print("usage: codfisc CODE|[SURNAME NAME DD/MM/YYYY SEX MUNICIPALITY]")
	exit(0)
