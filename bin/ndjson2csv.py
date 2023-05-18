#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os

PROGRAM_NAME = os.path.basename(sys.argv[0])

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

	input_json_str = infile.read()
	 
	line_no = 0
	header_fields_no = 0

	for line in input_json_str.splitlines():
		line_no += 1
		if not line:
			# skip empty lines
			continue
		try:
			curr_dict = json.loads(line)
		except:
			sys.stderr.write(PROGRAM_NAME + ": err: error decoding line " + str(line_no) + " (skipped)\n")
			continue
		if line_no == 1:
			# output the csv header
			for key in curr_dict:
				args.outfile.write(key)
				# add a comma only if not last field
				if not key==list(curr_dict.keys())[-1]:
					args.outfile.write(",")
			# end for
			args.outfile.write("\n")
			header_fields_no = len(curr_dict.keys())
		# end if
		# output current line values
		for key in curr_dict:
			# special null value check
			if curr_dict[key] is None:
				args.outfile.write("null")
			else:
				args.outfile.write(str(curr_dict[key]))
			# add a comma only if not last field
			if not key==list(curr_dict.keys())[-1]:
				args.outfile.write(",")
			# check if more fields than the header
			if not header_fields_no == len(curr_dict.keys()):
				sys.stderr.write(PROGRAM_NAME + ": warn: line " + str(line_no) + " has more fields than the header\n")
		# end for
		args.outfile.write("\n")
	# end for
