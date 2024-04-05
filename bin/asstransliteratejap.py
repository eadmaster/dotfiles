#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import string

# using https://github.com/polm/cutlet
import cutlet

PROGRAM_NAME = os.path.basename(sys.argv[0])

	
def init_jap_trans():
	katsu = cutlet.Cutlet()
	katsu.use_foreign_spelling = True  # detect english words
	return katsu


def jap_trans_old(trans_obj, line_text):
	#s = trans_obj.romaji(line_text, capitalize=False)
	
	line_text = cutlet.normalize_text(line_text)
	
	s = ""
	for tok in trans_obj.tagger(line_text):
		#if not tok.feature.pron:
		if not tok.feature.kana:
			continue
		if(tok.char_type == 5 or tok.surface.isascii() ):
			s += tok.surface.upper() + " "
		else:
			s += tok.feature.kana + " "
		#print(dir(tok))
		
		#print(tok.surface)

	print(s)

	return s.strip()
	

def jap_trans(katsu, line_text):
	# remove time tags
	import re
	line_text_no_tags = re.sub("\{.*?\}","", line_text)
		
	# derived from https://github.com/polm/cutlet/issues/46
	words = katsu.tagger(cutlet.normalize_text(line_text_no_tags))
	toks = katsu.romaji_tokens(words)
	for tok, word in zip(toks, words):
		#print(word.surface, tok.surface, sep="\t")
		line_text = line_text.replace(word.surface, tok.surface, 1)
	
	return line_text
	
	
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

	input_ass_str = infile.read()
	
	args.outfile.write("[by:eadmaster (automatic transliteration, may contain errors)]\n\n")
	 
	line_no = 0
	header_fields_no = 0
	
	trans_obj = init_jap_trans()

	for line in input_ass_str.splitlines():
		line_no += 1
		if not line.startswith("Dialogue:"):
			# keep unchanged
			print(line)
			continue
		
		# TODO: handle commas in the text?
		splitted_line = line.split(",")
		line_text = splitted_line[-1]
		
		line_text = jap_trans(trans_obj, line_text)
		
		args.outfile.write( ",".join(splitted_line[:-1]) + "," + line_text + "\n")
	# end for



