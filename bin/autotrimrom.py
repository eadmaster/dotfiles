#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os

MIN_TRIMMABLE_BYTES = 100

PROGRAM_NAME = os.path.basename(sys.argv[0])

if(len(sys.argv)==1 or sys.argv[1]=='-h' or sys.argv[1]=='--help' or not os.path.isfile(sys.argv[1])):
	print("usage: " + PROGRAM_NAME + " INPUT_FILE [OUTPUT FILE]")
	print("  If no output file is specified only count trimmable bytes and left the input file untouched.")
	print("  If the output file is equal to the input file, perform inplace trimming.")
	print("")
	print("Exit status is 0 if OK, 1 on error or not many trimmable bytes found.")
	exit(0)

input_file_size = os.stat(sys.argv[1]).st_size
if(input_file_size==0):
	print(PROGRAM_NAME + " fatal: empty input file, nothing to trim")
	exit(1)

input_file = None
try:
	input_file = open(sys.argv[1], "rb")
except:
	print(PROGRAM_NAME + " fatal: " + ": unable to open input file for reading: " + str(sys.exc_info()[1]))
	exit(1)

output_file = None
if(len(sys.argv)==3):
	try:
		output_file = open(sys.argv[2], "wb")
	except:
		print(PROGRAM_NAME + " fatal: " + ": unable to open output file for writing: " + str(sys.exc_info()[1]))
		exit(1)

# seek to the end of file -1 byte
input_file.seek(-1, os.SEEK_END)
LAST_BYTE = input_file.read(1)
current_byte = LAST_BYTE
trimmable_bytes_count = 0
while(current_byte==LAST_BYTE):
	trimmable_bytes_count += 1
	#DEBUG: print(hex(ord(current_byte)))
	# seek 1 byte back
	input_file.seek(-2, os.SEEK_CUR)
	current_byte = input_file.read(1)
	if(current_byte == ""):
		# EOF reached
		break
	# else continue
# end while

print(PROGRAM_NAME + " info: trimmable bytes found: " + str(trimmable_bytes_count))

if(output_file == None):
	print(PROGRAM_NAME + " info: no output file specified, exiting")
	exit(0)
# else output_file is opened

if(trimmable_bytes_count < MIN_TRIMMABLE_BYTES):
	print(PROGRAM_NAME + " info: less than " + str(MIN_TRIMMABLE_BYTES) + " found, exiting")
	exit(1)

output_file_size = (input_file_size - trimmable_bytes_count)
import shutil
try:
	# copy and truncate the inputfile
	input_file.seek(0)  # rewind input file position
	shutil.copyfileobj(input_file, output_file)
	output_file.truncate(output_file_size)
except:
	print(PROGRAM_NAME + " err: " + ": while writing output file: " + str(sys.exc_info()[1]))
	exit(1)
# else
print(PROGRAM_NAME + " info: output file written correctly")
exit(0)
