#! /usr/bin/env python
# -*- coding: utf-8 -*-

# convert pec codelist.inf to the PCSXR cheat format
# download the latest codelist.inf from http://www.psxdatacenter.com/

import sys
import os

#PROGRAM_NAME = sys.argv[0]
PROGRAM_NAME = "pec2pcsxr"

#args checking
if(len(sys.argv)==1 or sys.argv[1]=='-h' or sys.argv[1]=='--help' or not os.path.isfile(sys.argv[1])):
	print("usage: " + PROGRAM_NAME + " /path/to/codelist.inf " + "[gamename|SLXX-XXXXX]")
	print("WARNING: if no gamename|code is specified then all cheats are converted!")
	exit(1)
if( sys.argv[1] ):
	inputfile = sys.argv[1]
else:
	inputfile = 'codelist.inf'
	
try:
	codelist_file = open(inputfile, 'r')
except:
	print(PROGRAM_NAME + "error: unable to open input file")
	sys.exit(1)
	
matches = 0

for line in codelist_file:
	if line.startswith(';'): continue
	if line.startswith('#'):
		try:
			current_cheat_file.close()
		except:
			# the first time no file is opened
			pass

		# parse the line
		try:
			gamename = line.split("#")[1]
			gamecode = line.split("#")[2]
		except:
			continue
			#pass
			#print("error in line:")
			#print(line)
		
		if( len(sys.argv)>=3 and (not gamecode==sys.argv[2]+"\n") and (not sys.argv[2].lower() in gamename.lower())):
			continue
		# else
		matches += 1
		
		# 2FIX: if the gamecode contains 2 "-" or 2 "#" is meant for 2 discs -> create 2 files
		
		# reformat the gamecode "SXXX-XXXXX" -> "SXXX_XXX.XX"
		gamecode = gamecode.replace("-","_")
		gamecode = gamecode[0:8] + "." + gamecode[8:]
		gamecode = gamecode.replace('\r','')
		gamecode = gamecode.replace('\n','')
		gamecode = gamecode.replace('\t','')
		gamecode = gamecode.replace('/','_')
		gamecode = gamecode.rstrip() # strip other whitespace chars
		gamename = gamename.rstrip() # strip other whitespace chars
		#DEBUG: print(gamecode)
		#DEBUG: continue
		
		if(len(gamecode)==0):
			print(PROGRAM_NAME +" error: missing gamecode for "+ gamename +" (skipped)")
			continue # NOTE: since the file is not opened the following write attempts will fail
			
		# open the file for writing
		if(os.path.isfile(gamecode +".cht")):
			print(PROGRAM_NAME +" warning: file already exist "+ gamecode +".cht (appending to it)")
		try:
			current_cheat_file = open(gamecode +".cht","a")
		except:
			print(PROGRAM_NAME + " error: unable to create cheat file \"" + gamecode+".cht"+"\" :" + str(sys.exc_info()[1]))
		
		print(PROGRAM_NAME +" found: "+ gamename+" -> "+gamecode+".cht")
		
		# write an header
		current_cheat_file.write("; cheats for "+gamename+" ("+gamecode+")\n; converted with "+PROGRAM_NAME+" by eadmaster\n")
		
		continue

	line = line.rstrip() # strip other whitespace chars
	
	if line.startswith('\"'):
		line = line.replace('\"',"[", 1)
		line = line + "]"
	elif line.startswith('.'):
		#it's a comment of the prev code -> move up?
		line = line.replace('.',"; ", 1)
		# TODO: check long comments parsing
	elif line.startswith('&'):
		# special comments for notes -> convert to comments
		line = line.replace('&',"; ", 1)
		line = line + ":"
	elif line.startswith('%'):
		# references to comments -> convert to comments
		line = line.replace('%',"; see ", 1)
	# elif line.startswith(u'§'): not working?
	elif line.startswith('\xA7'): # MEMO: ISO-8859 encoding
		# jocker commands -> convert to regular codes 
		# see also http://pec.duttke.de/kmjkfaq.php
		#line = line.replace(u"§","\"", 1)
		line = line.replace("\xA7","[", 1)
		line = "\n" + line + "]"
	#elif line.startswith('$'):
		# Modifier Codes are not supported currently -> convert to comments?
	#	line = "; " + line
		
	# append to current cheat file
	try:
		current_cheat_file.write(line+'\n')
	except:
		pass
		
	# endfor

codelist_file.close()

if(matches == 0):
	print(PROGRAM_NAME +": no matching game found!")
