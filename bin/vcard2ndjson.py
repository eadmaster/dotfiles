#!/usr/bin/python
# -*- coding: utf-8 -*-

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
	import json
	import sys
	
	if len(sys.argv) > 1:
		f = open(sys.argv[1])
	else:
		f = sys.stdin
	vcard_str = f.read()
	vcard_dicts = vcard2dicts(vcard_str)

	for d in vcard_dicts:
		print(json.dumps(d))
