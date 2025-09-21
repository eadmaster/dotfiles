#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


# based on https://www.reddit.com/r/Gameboy/comments/hcq2g6/ezflash_omega_cheat_system_tutorial/


def ezcht2retroarch(input_cht_file_str, output_file):
	cheat_counter = 0
	
	for line in input_cht_file_str.splitlines():
		if line.strip() == "" or line.startswith("#"):
			# keep empty lines and comments
			output_file.write(line)
			continue
			
		if line.startswith("[GameInfo"):
			# assume it's the last block
			break

		if line.startswith("["):
			code_description = line.split("[")[1].split("]")[0]
			output_file.write("")
		
		if line.startswith("ON="):
			code_value = line.split("=")[1]
			commas_sep_count = code_value.count(",")
			if commas_sep_count<1 or commas_sep_count>2:
				print("unsupported code (skipped): " + line)
				continue
			# else
			if commas_sep_count==1:
				address, value = code_value.split(",")
				code_size = 3 # assume 8-bit
			elif commas_sep_count==2:
				address, value_type, value = code_value.split(",")
				if value_type=="F":
					code_size = 3 # assume 8-bit
				elif value_type=="8":
					# assume 16-bit
					code_size = 4
				elif value_type=="80":
					# assume 32-bit
					code_size = 5
				else:
					print("unsupported code size, assume 8-bit: " + value_type)
					code_size = 3 # assume 8-bit
					#continue					
			
			# output curr code
			output_file.write("\n")
			
			output_file.write("cheat%d_desc = \"%s\"\n" % (cheat_counter, code_description))
	
			output_file.write("cheat%d_address = \"%d\"\n" % (cheat_counter, int(address, 16) - 0x40000)) #  0x2000000 + 
			output_file.write("cheat%d_value = \"%d\"\n" % (cheat_counter, int(value, 16)))
			output_file.write("cheat%d_memory_search_size = \"%d\"\n" % (cheat_counter, code_size))
			output_file.write("cheat%d_cheat_type = \"1\"\n" % (cheat_counter))
			output_file.write("cheat%d_handler = \"1\"\n" % (cheat_counter))
			output_file.write("cheat%d_enable = false\n" % (cheat_counter))
			output_file.write("# original code: %s\n" % (line))  # debug
			
			cheat_counter += 1
		# end if new code
	# end for lines
	
	# print the correct cheats counter
	output_file.write("\n")
	output_file.write("cheats = \"%d\"\n" % (cheat_counter))
	output_file.close()
# end of ezcht2retroarch()


if __name__ == "__main__":
	import argparse, sys
	parser = argparse.ArgumentParser(description='converts .cht cheat tables from Native/Emulator-handled to Retroarch-handled format')
	parser.add_argument('infile', nargs='?', default="-", help="input file, defaults to stdin if unspecified. Supports passing urls.")
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file, defaults to stdout if unspecified")
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

	input_cht_file_str = infile.read()
	
	ezcht2retroarch(input_cht_file_str, args.outfile)
