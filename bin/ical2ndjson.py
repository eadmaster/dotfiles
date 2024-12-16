#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: jcal format support? https://www.rfc-editor.org/rfc/rfc7265

def ical2dicts(ical_str):
	# derived from https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python
	parsed_dicts = []
	curr_dict = {}
	black_list = ('#', 'BEGIN:VCALENDAR', 'BEGIN:VEVENT', 'VERSION:', 'CHARSET:', 'PRODID:')
	for lineb in ical_str.splitlines():
		line = lineb.decode('utf-8')
		if line.startswith("END:"):
			parsed_dicts.append(curr_dict)
			curr_dict = {}
			continue
		elif line.strip()=="":
			continue
		elif line.startswith(black_list):
			continue
		elif line.startswith(" "): # TODO: regexpr check
			# append to prev line
			#curr_dict[k] = v + line
			continue
		# else parse current line
		try:
			k, v = line.split(":", maxsplit=1)
		except:
			continue
		# cleanup the key
		k = k.lower()
		k = k.replace(";charset=utf-8", "")
		# TODO: move ";type=" to a separate field?
		# cleanup the value
		v = v.replace(";", " ")
		v = v.strip()
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
		# switch to text file mode
		import codecs
		infile = codecs.getreader("utf-8")(infile)
	else:
		infile = open(args.infile)
		
	ical_str = infile.read()
	
	ical_dicts = ical2dicts(ical_str)
	
	import json
	for d in ical_dicts:
		args.outfile.write(json.dumps(d))
		args.outfile.write("\n")


