#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

PROGRAM_NAME = os.path.basename(sys.argv[0])

def levenshtein_distance(str1, str2):
	# source: https://rosettacode.org/wiki/Levenshtein_distance#Python
	# returns: distance integer
	m = len(str1)
	n = len(str2)
	d = [[i] for i in range(1, m + 1)]   # d matrix rows
	d.insert(0, list(range(0, n + 1)))   # d matrix columns
	for j in range(1, n + 1):
		for i in range(1, m + 1):
			if str1[i - 1] == str2[j - 1]:   # Python (string) is 0-based
				substitutionCost = 0
			else:
				substitutionCost = 1
			d[i].insert(j, min(d[i - 1][j] + 1,
							   d[i][j - 1] + 1,
							   d[i - 1][j - 1] + substitutionCost))
	return d[-1][-1]

def soundex_american(word):
	# source: https://rosettacode.org/wiki/Soundex#Python
	# returns: encoded string
	from itertools import groupby
	codes = ("bfpv","cgjkqsxz", "dt", "l", "mn", "r")
	soundDict = dict((ch, str(ix+1)) for ix,cod in enumerate(codes) for ch in cod)
	cmap2 = lambda kar: soundDict.get(kar, '9')
	sdx =  ''.join(cmap2(kar) for kar in word.lower())
	sdx2 = word[0].upper() + ''.join(k for k,g in list(groupby(sdx))[1:] if k!='9')
	sdx3 = sdx2[0:4].ljust(4,'0')
	return sdx3

def gestalt_distance_ratio(str1, str2):
	# source: https://stackoverflow.com/a/46125447/791229
	# https://github.com/seatgeek/fuzzywuzzy/issues/128
	# returns: ratio as a float between 0 and 1
	from difflib import SequenceMatcher
	s = SequenceMatcher(None, str1, str2)
	return(s.ratio())
		
		
# main program
if __name__ == "__main__":
	
	if(len(sys.argv) < 3 or sys.argv[1] in ['-h', '--help']):
		print("usage: " + PROGRAM_NAME + " STRING1 STRING2")
		sys.exit(1)
	
	s1 = sys.argv[1]
	s2 = sys.argv[2]
	
	print("levenshtein_distance:")
	print(levenshtein_distance(s1, s2))

	print("gestalt_distance_ratio:")
	print(gestalt_distance_ratio(s1, s2))
	
	s1_soundex = ""
	s2_soundex = ""
	for word in s1.split(" "):
		s1_soundex += (soundex_american(word) + " ")
	for word in s2.split(" "):
		s2_soundex += (soundex_american(word) + " ")
	print("soundex encodings:")
	print(s1_soundex)
	print(s2_soundex)
	
	import nltk
	print("nltk edit_distance:")
	print(nltk.edit_distance(s1, s2))
	print("nltk jaccard_distance:")  # ignore repeated letters
	print(nltk.jaccard_distance(set(s1), set(s2)))
	print("nltk masi_distance:")  # ignore repeated letters
	print(nltk.masi_distance(set(s1), set(s2)))
	#print("nltk jaro_similarity:")
	#print(nltk.jaro_similarity(s1, s2))
