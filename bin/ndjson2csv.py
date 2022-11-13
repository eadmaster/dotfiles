#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os

PROGRAM_NAME = os.path.basename(sys.argv[0])

# hadle pipe closed nicely (e.g. when piping output to head)
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

input_json_str = ""

if(len(sys.argv)==1):
    # read from stdin
    input_json_str = sys.stdin.read()
else:
    # read from file
    input_json_str = open(sys.argv[1], 'r').read()
    
line_no = 0
header_fields_no = 0

for line in input_json_str.splitlines():
    line_no += 1
    if not line:
        # skip empty lines
        continue
    try:
        curr_dict = json.loads(line)
    except:
        sys.stderr.write(PROGRAM_NAME + ": err: error decoding line " + str(line_no) + " (skipped)\n")
        continue
    if line_no == 1:
        # output the csv header
        for key in curr_dict:
            sys.stdout.write(key)
            # add a comma only if not last field
            if not key==list(curr_dict.keys())[-1]:
                sys.stdout.write(",")
        # end for
        sys.stdout.write("\n")
        header_fields_no = len(curr_dict.keys())
    # end if
    # output current line values
    for key in curr_dict:
        # special null value check
        if curr_dict[key] is None:
            sys.stdout.write("null")
        else:
            sys.stdout.write(str(curr_dict[key]))
        # add a comma only if not last field
        if not key==list(curr_dict.keys())[-1]:
            sys.stdout.write(",")
        # check if more fields than the header
        if not header_fields_no == len(curr_dict.keys()):
            sys.stderr.write(PROGRAM_NAME + ": warn: line " + str(line_no) + " has more fields than the header\n")
    # end for
    sys.stdout.write("\n")
# end for
