#!/usr/bin/env python
# -*- coding: utf-8 -*-


# https://stackoverflow.com/questions/43469412/convert-html-source-code-to-json-object
# https://stackoverflow.com/questions/19712864/zconvert-an-html-file-into-a-python-dictionary


def html_to_dict_parser(html_str):
	from html.parser import HTMLParser
	class MyHTMLParser(HTMLParser):

		def __init__(self):
			HTMLParser.__init__(self)
			self.parsed_dict = []
			self.curr_tag = ""

		def handle_starttag(self, tag, attrs):
			if len(attrs)==0:
				self.curr_tag = tag
			else:
				self.parsed_dict.append({tag: attrs})

		def handle_endtag(self, tag):
			pass

		def handle_data(self, data):
			# content inside a tag
			if not data.strip():
				 return
			# else
			#self.parsed_dict.append(data)
			self.parsed_dict.append({self.curr_tag: data})
			self.curr_tag = ""

		def handle_comment(self, data):
			#self.parsed_dict.append(data)
			pass

		def handle_entityref(self, name):
			#from html.entities import name2codepoint
			#c = chr(name2codepoint[name])
			#print("Named ent:", c)
			pass

		def handle_charref(self, name):
			#if name.startswith('x'):
			#    c = chr(int(name[1:], 16))
			#else:
			#    c = chr(int(name))
			#print("Num ent  :", c)
			pass

		def handle_decl(self, data):
			#print("Decl     :", data)
			pass
	# end of MyHTMLParser
	
	parser = MyHTMLParser()
	parser.feed(str(html_str))
	parser.close()
	return(parser.parsed_dict)
	
        
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
	else:
		infile = open(args.infile)
	
	html_str = infile.read()
	
	import json
	for j in html_to_dict_parser(html_str):
		print(json.dumps(j).encode('ascii').decode('unicode-escape'))

