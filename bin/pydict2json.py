#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json, ast

input_dict_str = sys.stdin.read()
input_dict = ast.literal_eval(input_dict_str)

json.dump(input_dict, sys.stdout, indent=4)

print("") # empty line
