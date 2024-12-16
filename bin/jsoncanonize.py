#!/usr/bin/env python
# -*- coding: utf-8 -*-

# RFC-8785 JSON Canonicalization Scheme (JCS)
# https://rubydoc.info/gems/json-canonicalization/file/README.md

import sys, json

input_dict_str = sys.stdin.read()
input_dict = json.loads(input_dict_str)

json.dump(input_dict, sys.stdout, indent=None, sort_keys=True, separators=(",", ":"))

print("") # empty line
