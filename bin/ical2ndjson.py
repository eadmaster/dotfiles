#!/usr/bin/python
# -*- coding: utf-8 -*-


# https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python

def ical2dicts(ical_str):
	parsed_dicts = []
	curr_dict = {}
	black_list = ('#', 'BEGIN:VCALENDAR', 'BEGIN:VEVENT', 'VERSION:', 'CHARSET:', 'PRODID:')
	for line in ical_str.splitlines():
		if line.startswith("END:VEVENT"):
			parsed_dicts.append(curr_dict)
			curr_dict = {}
			continue
		elif line.strip()=="":
			continue
		elif line.startswith(black_list):
			continue
		elif line.startswith(" "): # TODO: regexpr check
			# append to prev line
			curr_dict[k] = v + line
			continue
		# else parse current line
		k, v = line.split(":", maxsplit=1)
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
	import json
	import sys
	
	if len(sys.argv) > 1:
		f = open(sys.argv[1])
	else:
		sys.stderr.write("reading from stdin...\n")
		f = sys.stdin
		
	ical_str = f.read()
	ical_dicts = ical2dicts(ical_str)

	for d in ical_dicts:
		print(json.dumps(d))


