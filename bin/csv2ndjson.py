#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json, os
import csv

PROGRAM_NAME = os.path.basename(sys.argv[0])
DEFAULT_CSV_DIALECT = csv.excel_tab  # fallback to this if autodetection fails

# hadle pipe closed nicely (e.g. when piping output to head)
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

input_csv_file = None

if(len(sys.argv)==1):
    # read from stdin
    #input_csv_file = sys.stdin  # cannot seek
    from io import StringIO
    input_csv_file = StringIO(sys.stdin.read())
else:
    # read from file
    input_csv_file = open(sys.argv[1], 'r')

input_csv_header = input_csv_file.read(1024)
input_csv_file.seek(0)  # 2FIX: not working from stdin?

# try to guess the formatting parameters
try:
	csv_sniffer = csv.Sniffer().sniff(input_csv_header)
	if not csv.Sniffer().has_header(input_csv_header):
		sys.stderr.write(PROGRAM_NAME + ": err: csv missing header line\n")
		sys.exit(1)
except:
    csv_sniffer = DEFAULT_CSV_DIALECT

csv_rows_reader = csv.DictReader(input_csv_file, dialect=csv_sniffer) # rows are parsed as a list of strings
sys.stderr.write(PROGRAM_NAME + ": info: detected delimiter: + " + csv_sniffer.delimiter + "\n")

#print("{[")

# iterate over the splitted rows
for curr_row in csv_rows_reader:
	print(json.dumps(curr_row)) # , indent=4

#sys.stdout.write(json.dumps(curr_row)) # overwrite last row
#print(" ]}")
print("")
