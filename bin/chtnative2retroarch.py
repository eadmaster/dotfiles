#!/usr/bin/python
# -*- coding: utf-8 -*-


if __name__ == "__main__":
	import sys
	import json
	
	# usage: python chtnative2retroarch.py "My Native cheat table.cht" > "My Retroarch cheat table.cht"
	
	input_cht_file_str = open(sys.argv[1], "r").read()
	
	input_sys_str = None
	if len(sys.argv) > 2:
		# optional: specify the system
		input_sys_str = sys.argv[2]
	
	
	cheat_counter = 0
	
	for line in input_cht_file_str.splitlines():
		if line.strip() == "" or line.startswith("#"):
			# keep empty lines and comments
			print(line)
			continue

		if "=" in line:
			line_desc, line_value = line.split("=")
			line_desc = line_desc.strip()
			line_value = line_value.strip()
			line_value = line_value.strip("\"")
			
		if line.startswith("cheats ") or line_desc.endswith("_enable"):
			# skip cheat counter
			continue
			
		if line_desc.endswith("_desc"):
			code_description = line_value.strip("\"")
			print("")
			print("cheat%d_desc = \"%s\"" % (cheat_counter, code_description))
		
		if line_desc.endswith("_code"):
			# perform conversion
			multicode_delim = "+"
			if ";" in line_value:
				multicode_delim = ";"
			for i, code in enumerate(line_value.split(multicode_delim)):
				address, value = code.split(" ")  # TODO: handle codes using "+" as separator
				
				address = address[2:]  # cut 1st 2 digits , used to identify GS code type 
				
				if input_sys_str in ["sat", "ss", "saturn"]:
					# need to apply a custom offset, tested with libretro-yabause only
					address = address[1:]
					address = "1" + address
		
				# TODO: properly parse code type, depends on system https://macrox.gshi.org/The%20Hacking%20Text.htm#playstation_code_types
				
				if i>0:
					# repeat the description
					print("")
					print("cheat%d_desc = \"%s (part %d)\"" % (cheat_counter, code_description, i+1))
				
				print("cheat%d_address = \"%d\"" % (cheat_counter, int(address, 16)))
				print("cheat%d_value = \"%d\"" % (cheat_counter, int(value, 16)))
				print("cheat%d_cheat_type = \"1\"" % (cheat_counter))
				print("cheat%d_handler = \"1\"" % (cheat_counter))
				print("cheat%d_enable = false" % (cheat_counter))
			
				if len(value)==4 and value.startswith("00"):
					# assume 8-bit
					print("cheat%d_memory_search_size = \"3\"" % (cheat_counter))
				elif len(value)==4:
					# assume 16-bit
					print("cheat%d_memory_search_size = \"4\"" % (cheat_counter))
				else:
					# assume 32-bit
					print("cheat%d_memory_search_size = \"5\"" % (cheat_counter))
				cheat_counter += 1
		# end if new code
	# end for lines
	
	# print the correct cheats counter
	print("")
	print("cheats = \"%d\"" % (cheat_counter))
	

		