#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pykakasi
import sys
import os

PROGRAM_NAME = os.path.basename(sys.argv[0])



def init_jap_trans_old():
	# using pykakasi  https://github.com/miurahr/pykakasi
	import pykakasi
	kakasi = pykakasi.kakasi()
	kakasi.setMode("H","a") # Hiragana to ascii, default: no conversion
	kakasi.setMode("K","a") # Katakana to ascii, default: no conversion
	kakasi.setMode("J","a") # Japanese to ascii, default: no conversion
	kakasi.setMode("r","Hepburn") # default: use Hepburn Roman table
	kakasi.setMode("s", True) # add space, default: no separator
	kakasi_conv = kakasi.getConverter()
	return kakasi_conv


def jap_trans_old(trans_obj, line_text):
	s = trans_obj.do(line_text)
	return s
	
def init_jap_trans():
	# using https://github.com/polm/cutlet
	import cutlet
	katsu = cutlet.Cutlet()
	katsu.use_foreign_spelling = True  # detect english words
	# TODO: uppercase: https://github.com/polm/cutlet/discussions/38
	return katsu


def jap_trans(trans_obj, line_text):
	s = trans_obj.romaji(line_text, capitalize=False)
	return s
	
	
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
	 
	line_no = 0
	header_fields_no = 0
	
	trans_obj = init_jap_trans()

	for line in input_lrc_str.splitlines():
		line_no += 1
		if not "]" in line:
			# skip empty lines
			#sys.stderr.write(PROGRAM_NAME + ": warn: line " + str(line_no) + " has more fields than the header\n")
			continue
		ts, line_text = line.split("]")
		
		line_text = jap_trans(trans_obj, line_text)
		line_text = line_text.strip()
		
		print( ts + "]" + line_text)
	# end for



