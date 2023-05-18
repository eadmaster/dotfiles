#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
PROGRAM_NAME = os.path.basename(sys.argv[0])

import csv
DEFAULT_CSV_DIALECT = csv.excel_tab  # fallback to this if autodetection fails

def csv2dict(csv_str):
	from io import StringIO
	input_csv_file = StringIO(csv_str)

	input_csv_header = input_csv_file.read(1024)
	input_csv_file.seek(0)

	# try to guess the formatting parameters
	try:
		csv_sniffer = csv.Sniffer().sniff(input_csv_header)
		if not csv.Sniffer().has_header(input_csv_header):
			sys.stderr.write(PROGRAM_NAME + ": err: csv missing header line\n")
			sys.exit(1)
	except:
		csv_sniffer = DEFAULT_CSV_DIALECT

	csv_rows_reader = csv.DictReader(input_csv_file, dialect=csv_sniffer) # rows are parsed as a list of strings
	sys.stderr.write(PROGRAM_NAME + ": info: detected delimiter: + " + csv_sniffer.delimiter + "\n")

	# iterate over the splitted rows
	output_dicts = []
	for curr_row in csv_rows_reader:
		output_dicts.append(dict(curr_row))
	
	return output_dicts


# main program
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
	
	csv_str = infile.read()

	csv_dicts = csv2dict(csv_str)
	
	import json
	for d in csv_dicts:
		args.outfile.write(json.dumps(d))
		args.outfile.write("\n")
