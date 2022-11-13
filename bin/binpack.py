#! /usr/bin/env python
# -*- coding: utf-8 -*-

''' approximate subset sum file packer
   by eadmaster
   
   released under the terms of the latest GPL license.
'''


import os
import sys
import argparse


PROGRAM_NAME = os.path.basename(sys.argv[0])
#PROGRAM_NAME = "ss"

KILOBYTE=1024
MEGABYTE=1024*1024
GIGABYTE=1024*1024*1024

FD_SIZE=1457664
CDR_SIZE=736962560
# CD_R_74_MIN=737280000
# CD_R_80_MIN=840960000
DVD_PLUS_R_SIZE=4700372992 # DVD+R
# DVD_PLUS_R_SIZE=4692377600 # DVD+R (safe value with UDF?)
DVD_MINUS_R_SIZE=4707319808 # DVD-R
DVD_PLUS_R_DL_SIZE=8547991552 # DVD+R DL
DVD_MINUS_R_DL_SIZE=8543666176 # DVD-R DL


# human filesizes perser from
# http://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/
# ALTERNATIVES: http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size

# see: http://goo.gl/kTQMs
SYMBOLS = {
    'customary'     : ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
    'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                       'zetta', 'iotta'),
    'iec'           : ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
    'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                       'zebi', 'yobi'),
}

def bytes2human(n, format='%(value).1f %(symbol)s', symbols='customary'):
    """
    Convert n bytes into a human readable string based on format.
    symbols can be either "customary", "customary_ext", "iec" or "iec_ext",
    see: http://goo.gl/kTQMs

      >>> bytes2human(0)
      '0.0 B'
      >>> bytes2human(0.9)
      '0.0 B'
      >>> bytes2human(1)
      '1.0 B'
      >>> bytes2human(1.9)
      '1.0 B'
      >>> bytes2human(1024)
      '1.0 K'
      >>> bytes2human(1048576)
      '1.0 M'
      >>> bytes2human(1099511627776127398123789121)
      '909.5 Y'

      >>> bytes2human(9856, symbols="customary")
      '9.6 K'
      >>> bytes2human(9856, symbols="customary_ext")
      '9.6 kilo'
      >>> bytes2human(9856, symbols="iec")
      '9.6 Ki'
      >>> bytes2human(9856, symbols="iec_ext")
      '9.6 kibi'

      >>> bytes2human(10000, "%(value).1f %(symbol)s/sec")
      '9.8 K/sec'

      >>> # precision can be adjusted by playing with %f operator
      >>> bytes2human(10000, format="%(value).5f %(symbol)s")
      '9.76562 K'
    """
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    symbols = SYMBOLS[symbols]
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i+1)*10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)

def human2bytes(s):
    """
    Attempts to guess the string format based on default symbols
    set and return the corresponding bytes as an integer.
    When unable to recognize the format ValueError is raised.

      >>> human2bytes('0 B')
      0
      >>> human2bytes('1 K')
      1024
      >>> human2bytes('1 M')
      1048576
      >>> human2bytes('1 Gi')
      1073741824
      >>> human2bytes('1 tera')
      1099511627776

      >>> human2bytes('0.5kilo')
      512
      >>> human2bytes('0.1  byte')
      0
      >>> human2bytes('1 k')  # k is an alias for K
      1024
      >>> human2bytes('12 foo')
      Traceback (most recent call last):
          ...
      ValueError: can't interpret '12 foo'
    """
    init = s
    num = ""
    while s and s[0:1].isdigit() or s[0:1] == '.':
        num += s[0]
        s = s[1:]
    num = float(num)
    letter = s.strip()
    for name, sset in SYMBOLS.items():
        if letter in sset:
            break
    else:
        if letter == 'k':
            # treat 'k' as an alias for 'K' as per: http://goo.gl/kTQMs
            sset = SYMBOLS['customary']
            letter = letter.upper()
        else:
            raise ValueError("can't interpret %r" % init)
    prefix = {sset[0]:1}
    for i, s in enumerate(sset[1:]):
        prefix[s] = 1 << (i+1)*10
    return int(num * prefix[letter])


def _to_human(s):
	''' convert "n" RAW bytes count
	   into a human-readable string
	'''
	return(bytes2human(s))


def _to_bytes(s):
	'''
		convert a human readable byte string (with suffixes "G, M, K")
		into RAW bytes count
		
		also supports special constants like fd, cd-r, dvd-r, etc.
	'''

	# convert "s" to upper case for case-insensitive string comparison
	s = s.upper()
	
	if(s=="FD"): return FD_SIZE
	elif(s=="CDR"): return CDR_SIZE
	elif(s=="CD-R"): return CDR_SIZE
	elif(s=="DVD+R"): return DVD_PLUS_R_SIZE
	elif(s=="DVD-R"): return DVD_MINUS_R_SIZE
	elif(s=="DVD+RDL"): return DVD_PLUS_R_DL_SIZE
	elif(s=="DVD-RDL"): return DVD_MINUS_R_DL_SIZE
	else: 
		if("B" not in s): s = s + " B" # if no unit specified defaults to bytes
		s = s.replace("GB","G")
		s = s.replace("MB","M")
		s = s.replace("KB","K")
		return(human2bytes(s))

ALLOC_UNIT_SIZE = 2048

def _recursive_dir_size(source):
	''' recursively compute the disk usage of a directory
	   returns no bytes used
	   http://snipplr.com/view/47686/
	'''
	total_size = os.path.getsize(source)
	for item in os.listdir(source):
		itempath = os.path.join(source, item)
		if os.path.isfile(itempath):
			real_file_size = os.path.getsize(itempath)
			#round up according to the logic allocation unit size http://stackoverflow.com/questions/8866046/python-round-up-integer-to-next-hundred
			allocated_file_size = real_file_size + ALLOC_UNIT_SIZE - 1 - ((real_file_size + ALLOC_UNIT_SIZE - 1) % ALLOC_UNIT_SIZE)
			#allocated_file_size = real_file_size
			total_size += allocated_file_size
		elif os.path.isdir(itempath):
			total_size += _recursive_dir_size(itempath)
	return(total_size)


#def _recursive_add_files(filenames, filesizes, path):
	# TODO


# if __name__ == '__main__':
parser = argparse.ArgumentParser(description="select the subset of files that have max sum")

parser.add_argument("files_list", nargs='+', default="*.*", help="list of objects to select") # mandatory arg
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity") # boolean optional arg
parser.add_argument("-s", "--size", default="DVD+R", help="bin size to fill. Supports human suffixes and string constants like CD-R, DVD-R, DVD+R (default), etc.")
parser.add_argument("-p", "--precision", help="precision (automatic if not specified)")
parser.add_argument("-e", "--exclude", help="exclude wildcard")

#parser.add_argument("-f", "--finalized", action="store_true", help="reserve extra space required for the leadout|disk finalization (default off)")
parser.add_argument("-u", "--udf", action="store_true", default=False, help="compute extra space required by the UDF filesystem (default off)")

group = parser.add_mutually_exclusive_group()
group.add_argument("-n", action="store_true", help="don't recurse into directories. Treat subdirs as single files (default)") # boolean optional arg
group.add_argument("-r", "--recursive", action="store_true", help="recurse into directories") # boolean optional arg
group.add_argument("-i", "--ignore", action="store_true", help="skip directories") # boolean optional arg

args = parser.parse_args()

#args = vars(args)
#print(type(args))

if(args.verbose):
	print(PROGRAM_NAME+": verbose mode enabled")

#NO? if(os.name=='posix'):
#NO? 	filenames = args.files_list
# NOTE: on unix globbing can be disabled (eg. with the "noglobe" bash option)
# else we need to expand the wildcards
import glob
filenames = []
for f in args.files_list:
	filenames.extend(glob.glob(f))

filesizes = []
N=0 # files count

import fnmatch
#ALTERNATIVE: using glob + list diff

# iterate over input filenames and read filesizes
for f in filenames:
	if(args.exclude and fnmatch.fnmatch(os.path.basename(f), args.exclude)):
		if(args.verbose): print(PROGRAM_NAME+": "+f+ " matches exclude wildcard (skipped)")
		filenames.remove(f)
		continue
	
	if(os.path.isdir(f)):
		if(args.ignore):
			if(args.verbose): print(PROGRAM_NAME+": directory " + f+ " skipped")
			filenames.remove(f)
			continue
		elif(args.recursive):
			print(PROGRAM_NAME+": RECURSE OPTION NOT YET IMPLEMENTED")
			exit(1)
			#_recursive_add_files(filenames, filesizes, f):
		else:
			try:
				filesizes.insert(N, _recursive_dir_size(f))
			except:
				print(PROGRAM_NAME+": error reading directory size: "+f+" (skipped)")
				filenames.remove(f)
				continue
	else:
		# f is a simple file
		try:
			filesizes.insert(N, os.path.getsize(f))
		except:
			print(PROGRAM_NAME+": error reading file size: "+f+" (skipped)")
			filenames.remove(f)
			continue
	
	N += 1 # increase file count
	# endfor

W = DVD_PLUS_R_SIZE  # capacity in bytes. default=DVD+R size
if(args.size):
	try:
		W = _to_bytes(args.size)
	except:
		print(PROGRAM_NAME+": error parsing the size string: " + str(sys.exc_info()[1]))
		pass # W stay unchaged?

if(args.udf):
	# descrease fixed reserved space for UDF?
	W = W - 7995392

P = MEGABYTE # precision in bytes. default=1MB
# auto-set precision
if W<=10*P:
	if(W>=10*GIGABYTE): P=GIGABYTE
	elif(W>=10*MEGABYTE): P=MEGABYTE
	elif(W>=10*KILOBYTE): P=KILOBYTE
	else: P=1

if(args.precision):
	try:
		P = _to_bytes(args.precision)
	except:
		print(PROGRAM_NAME+": error parsing the precision string: " + str(sys.exc_info()[1]))
		pass # P stay unchaged?

if(args.verbose):
	print(PROGRAM_NAME+": capacity set as " + _to_human(W))
	print(PROGRAM_NAME+": precision set as " + _to_human(P))
	print(PROGRAM_NAME+": "+str(N)+ " objects read, starting selection...")

# apply precision to binsize and filesizes
if P!=1:
	W /= P
	#import math
	for i in range(0, N): 
		#filesizes[i] = round((filesizes[i]/P))
		#filesizes[i] = int(math.ceil((filesizes[i]/P)))
		if(filesizes[i]/P==0):
			filesizes[i] = 1
		else:
			filesizes[i] = int(filesizes[i]/P)

# initalize the DP matrix to 0s
M = [[0 for i in range(W)] for j in range(N)]

# DP search algorithm
for i in range(1, N):
	for w in range(1, W):
		if filesizes[i]>w:
			M[i][w] = M[i-1][w]
		else:
			M[i][w] = max( M[i-1][w], ( filesizes[i] + M[i-1][w-filesizes[i]]) )

if(args.verbose):
	print(PROGRAM_NAME+": done.")
	print(PROGRAM_NAME+": selected items:")

i=N-1
w=W-1
selected_count = 0
while(i>0):
	if( M[i][w]==M[i-1][w]):
		# item discarded
		i -= 1
	else:
		# item selected
		sys.stdout.write(filenames[i])
		if(args.verbose):
			print(" (~" + _to_human(filesizes[i]*P) + ")")
		else:
			print("")
		w -= filesizes[i]
		i -= 1
		selected_count += 1
	#endwhile

if(args.verbose):
	if(selected_count==0):
		print("none")
	else:
		print(PROGRAM_NAME+": total selected files size: "+ _to_human( M[N-1][W-1]*P ))
		print(PROGRAM_NAME+": wasted space: " + _to_human( (W-M[N-1][W-1])*P ) )
	#endif

exit(0)
