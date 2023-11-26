#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import string

PROGRAM_NAME = os.path.basename(sys.argv[0])

	
def init_jap_trans():
	# using https://github.com/polm/cutlet
	import cutlet
	katsu = cutlet.Cutlet()
	katsu.use_foreign_spelling = True  # detect english words
	return katsu


def jap_trans(trans_obj, line_text):
	#s = trans_obj.romaji(line_text, capitalize=False)
	s = ""
	for tok in trans_obj.tagger(line_text):
		if(tok.char_type == 5 or tok.surface.isascii() ):
			s += tok.surface.upper() + " "
		else:
			s += tok.surface + " "
	line_text = s
	
	s = ""
	tokens = trans_obj.romaji_tokens(trans_obj.tagger(line_text), capitalize=False)
	for tok in tokens:
		
		#if tok.surface in string.punctuation:
		#	# remove last char
		#	s = s[:-1]
		
		# uppercase foreign tokens https://github.com/polm/cutlet/discussions/38
		if tok.foreign:  # tok.surface.isascii() or 
			s += tok.surface.upper()
		else:
			s += tok.surface
		
		if tok.space:
			# a space should follow
			s += " "

	return s.strip()
	
	
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

	input_lrc_str = infile.read()
	
	print("[by:eadmaster (automatic transliteration, may contain errors)]")
	print("")
	 
	line_no = 0
	header_fields_no = 0
	
	trans_obj = init_jap_trans()

	for line in input_lrc_str.splitlines():
		line_no += 1
		if not "]" in line:
			# skip empty lines
			#sys.stderr.write(PROGRAM_NAME + ": warn: line " + str(line_no) + " has more fields than the header\n")
			continue
		ts, line_text = line.split("]", maxsplit=1)
		
		# skip meta tag lines
		if( any(i in line_text for i in ["作词", "作曲"]) ):
			continue

		line_text = jap_trans(trans_obj, line_text)
		line_text = line_text.strip()
		
		print( ts + "]" + line_text)
	# end for



