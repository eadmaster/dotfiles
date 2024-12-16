#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

def ini2dict(ini_str):
	# derived from https://stackoverflow.com/questions/1773793/convert-configparser-items-to-dictionary
	import sys
	if sys.version_info[0] <= 2:
		from ConfigParser import (ConfigParser)
	else:
		from configparser import (ConfigParser)
	cfg = ConfigParser()
	cfg.read_string(ini_str)
	d = {}
	for section_name in cfg.sections():
		d[section_name] = dict(cfg[section_name])
		d[section_name].pop("python_version", None)
	return(d)

    
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

	input_ini_str = infile.read()
	d = ini2dict(input_ini_str)
	args.outfile.write(json.dumps(d))
