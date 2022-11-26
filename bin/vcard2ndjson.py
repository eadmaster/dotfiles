#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: jCard format support? https://datatracker.ietf.org/doc/rfc7095/

def vcard2dicts(vcard_str):
	parsed_dicts = []
	curr_dict = {}
	black_list = ('#', 'BEGIN:', 'VERSION', 'CHARSET')
	for line in vcard_str.splitlines():
		if line.startswith("END:"):
			parsed_dicts.append(curr_dict)
			curr_dict = {}
			continue
		elif line.strip()=="":
			continue
		elif line.startswith(black_list):
			continue
		# else parse current line
		k, v = line.split(":", maxsplit=1)
		# cleanup the value
		v = v.replace(";", " ")
		v = v.strip()
		# cleanup the key
		k = k.lower()
		k = k.replace(";charset=utf-8", "")
		# TODO: move ";type=" to a separate field?

		# add current value
		curr_dict[k] = v
	# end for
	return parsed_dicts


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
	else:
		infile = open(args.infile)
		
	vcard_str = infile.read()
	vcard_dicts = vcard2dicts(vcard_str)

	for d in vcard_dicts:
		args.outfile.write(json.dumps(d))
		args.outfile.write("\n")