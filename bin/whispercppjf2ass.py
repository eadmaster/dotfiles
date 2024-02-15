#!/usr/bin/python
# -*- coding: utf-8 -*-

#  http://stackoverflow.com/questions/37913415/list-all-json-pointers-and-skip-common-decoding-errors

import json,sys, codecs



if __name__ == "__main__":
	import argparse, sys
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', nargs='?', default="-", help="input file, default to stdin if unspecified. Supports passing urls.")
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file, default to stdout if unspecified")
	args = parser.parse_args()

	if args.infile == "-":
		infile = sys.stdin
		sys.stderr.write("reading from stdin...\n")
	elif args.infile.startswith(("http://", "ftp://", "https://")):  # TODO: proper URL validation
		from urllib.request import urlopen
		infile = urlopen(args.infile)
		# switch to text file mode
		import codecs
		infile = codecs.getreader("utf-8")(infile)
	else:
		infile = open(args.infile)
		#infile = codecs.getreader("utf-8")(infile)

	input_json_str = infile.read()
	
		
	parsed_json = json.loads(input_json_str) # TODO: better handle decoding errors (create a custom JSONDecoder?)

	#2FIX(not working with top level lists): print("fileinfo: number of top-level entries: " + str(len(obj.keys())))  # TODO: print more infos?
	
	# header
	args.outfile.write("[Script Info]\n")
	args.outfile.write("Converted using wisper.cpp\n")
	args.outfile.write("Title: \n")
	args.outfile.write("ScriptType: v4.00+\n")
	args.outfile.write("WrapStyle: 0\n")
	args.outfile.write("ScaledBorderAndShadow: yes\n")
	args.outfile.write("Collisions: Normal\n")
	args.outfile.write("\n")
	args.outfile.write("[V4+ Styles]\n")
	args.outfile.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
	args.outfile.write("Style: Default,Arial,24,&H00FFFFFF,&H000088EF,&H00000000,&H00666666,-1,0,0,0,100,100,0,0,1,1.5,0,8,0,0,20,1\n")
	args.outfile.write("\n")
	args.outfile.write("[Events]\n")
	args.outfile.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
	
	lines = parsed_json["transcription"]
	for l in lines:
		full_line = l["text"].strip()
		if full_line == "â":
			continue
		
		tokens_list = l["tokens"]
		from_ts = l["timestamps"]["from"]
		from_ts = from_ts[1:-1]
		to_ts = l["timestamps"]["to"]
		to_ts = to_ts[1:-1]
		
		# Dialogue: 1,0:00:00.00,0:00:03.45,Default,,0,0,0,fx,{\k32\fad(300,200)}{\k25}You {\k37}think {\k18}I'm {\k12}an {\k25}ig{\k18}no{\k31}rant {\k18}sav{\k88}age
		
		args.outfile.write("Dialogue: 1,")
		
		args.outfile.write(from_ts.replace(",", "."))
		args.outfile.write(",")
		args.outfile.write(to_ts.replace(",", "."))
		
		args.outfile.write(",Default,,0,0,0,fx,")
		
		#args.outfile.write(full_line)
		#print(full_line)
		for t in tokens_list:
			token_text = t["text"].strip()
			
			if ord(token_text[0]) > 127:
				# not ascii
				continue
			if token_text in [ "ª", "â" ] or token_text.startswith(("[", "âª")):
				continue
			
			duration = int(abs(t["offsets"]["to"] - t["offsets"]["from"]) / 10)
			args.outfile.write("{\k" + str(duration) + "}" + token_text + " ")
		
		args.outfile.write("\n")
		
