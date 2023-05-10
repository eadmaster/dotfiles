#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def chtnative2retroarch(input_cht_file_str, input_sys_str, output_file):
	cheat_counter = 0
	
	for line in input_cht_file_str.splitlines():
		if line.strip() == "" or line.startswith("#"):
			# keep empty lines and comments
			output_file.write(line)
			continue

		if "=" in line:
			line_key, line_value = line.split("=", maxsplit=1)
			line_key = line_key.strip()
			line_value = line_value.strip()
			line_value = line_value.strip("\"")
		else:
			# malformed line?
			continue
			
		if line.startswith("cheats ") or line_key.endswith("_enable"):
			# skip cheat counter
			continue
			
		if line_key.endswith("_desc"):
			code_description = line_value.strip("\"")
			output_file.write("")
		
		if line_key.endswith("_code"):
			# detect code format
			
			multicode_delim = "+"
			# detect ";" as multicode separator (e.g. cheat6_code = "80010AB4 0701;50000F02 0000")
			if ";" in line_value:
				multicode_delim = ";"
				
			# detect "+" as code/value separator and reformat the line (e.g. cheat6_code = "80010AB4+0701+50000F02+0000+800108B4+0303+50001802+0000+80010A84+0001")
			if not " " in line_value and "+" in line_value:
				# replace "+" -> " ", even occurrences only  https://stackoverflow.com/questions/74770647/replace-character-in-python-string-every-even-or-odd-occurrence
				pieces = line_value.split("+")
				line_value = '+'.join(' '.join(pieces[i:i+2]) for i in range(0, len(pieces), 2))
			
			for i, code in enumerate(line_value.split(multicode_delim)):
				
				try:
					address, value = code.split(" ")
				except:
					sys.stderr.write("err: could not parse this line (skipped): %s\n" % line)
					continue
				
				if "?" in value or "X" in value:
					sys.stderr.write("err: modifier values are not supported, manually edit this code (skipped): %s\n" % line)
					continue
					
				address = address[2:]  # cut 1st 2 digits , used to identify GS code type 
				
				if input_sys_str in ["sat", "ss", "saturn"]:
					# need to apply a custom offset (don't ask me why :-), tested with libretro-yabause only atm
					address = address[1:]
					address = "1" + address
		
				# TODO: properly parse code type, depends on system https://macrox.gshi.org/The%20Hacking%20Text.htm#playstation_code_types
				
				output_file.write("\n")
				
				if i==0:
					output_file.write("cheat%d_desc = \"%s\"\n" % (cheat_counter, code_description))
				else:
					# append the part number to the description
					output_file.write("cheat%d_desc = \"%s (part %d)\"\n" % (cheat_counter, code_description, i+1))
		
				output_file.write("cheat%d_address = \"%d\"\n" % (cheat_counter, int(address, 16)))
				output_file.write("cheat%d_value = \"%d\"\n" % (cheat_counter, int(value, 16)))
				output_file.write("cheat%d_cheat_type = \"1\"\n" % (cheat_counter))
				output_file.write("cheat%d_handler = \"1\"\n" % (cheat_counter))
				output_file.write("cheat%d_enable = false\n" % (cheat_counter))
			
				#if len(value)==4 and value.startswith("00"):
				#	# assume 8-bit
				#	output_file.write("cheat%d_memory_search_size = \"3\"\n" % (cheat_counter))
				if len(value)==4:
					# assume 16-bit
					output_file.write("cheat%d_memory_search_size = \"4\"\n" % (cheat_counter))
				else:
					# assume 32-bit
					output_file.write("cheat%d_memory_search_size = \"5\"\n" % (cheat_counter))
				
				cheat_counter += 1
		# end if new code
	# end for lines
	
	# print the correct cheats counter
	output_file.write("\n")
	output_file.write("cheats = \"%d\"\n" % (cheat_counter))
	output_file.close()
# end of chtnative2retroarch()


if __name__ == "__main__":
	import argparse, sys
	parser = argparse.ArgumentParser(description='converts .cht cheat tables from Native/Emulator-handled to Retroarch-handled format')
	parser.add_argument('infile', nargs='?', default="-", help="input file, defaults to stdin if unspecified. Supports passing urls.")
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file, defaults to stdout if unspecified")
	parser.add_argument("-s", "--system", default=None, help="perform system-specific conversions (currently only saturn is supported)")
	args = parser.parse_args()

	if args.infile == "-":
		infile = sys.stdin
		sys.stderr.write("reading from stdin...\n")
	elif args.infile.startswith(("http://", "ftp://", "https://")):  # TODO: proper URL validation
		from urllib.request import urlopen
		infile = urlopen(args.infile)
	else:
		infile = open(args.infile)

	input_cht_file_str = infile.read()
	if type(input_cht_file_str)==bytes:
		input_cht_file_str = input_cht_file_str.decode('utf-8')
	
	input_sys_str = args.system
	
	chtnative2retroarch(input_cht_file_str, input_sys_str, args.outfile)
