#!/usr/bin/python3
# -*- coding: utf-8 -*-

def xml2dict(xml_str):
	import logging
	try:
		# using https://github.com/martinblech/xmltodict
		# apt install python3-xmltodict
		import xmltodict
		return(xmltodict.parse(xml_str))
	except:
		logging.exception("")
	
	# else pure python ver  https://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree#answer-10076823
	def etree_to_dict(t):
		from collections import defaultdict
		d = {t.tag: {} if t.attrib else None}
		children = list(t)
		if children:
			dd = defaultdict(list)
			for dc in map(etree_to_dict, children):
				for k, v in dc.items():
					dd[k].append(v)
			d = {t.tag: {k: v[0] if len(v) == 1 else v
						 for k, v in dd.items()}}
		if t.attrib:
			d[t.tag].update(('@' + k, v)
							for k, v in t.attrib.items())
		if t.text:
			text = t.text.strip()
			if children or t.attrib:
				if text:
					d[t.tag]['#text'] = text
			else:
				d[t.tag] = text
		return d
	from xml.etree import cElementTree as ET
	return( etree_to_dict( ET.XML(xml_str) ) )


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
		
	xml_str = infile.read()
	d = xml2dict(xml_str)
	import json
	args.outfile.write(json.dumps(d, indent=4))
	args.outfile.write("\n")
	