#!/usr/bin/env python3

#a script can help u to convert the lyrics file to .srt
#created by wOOL, iamwool@gmail.com
#edited by eadmaster  http://eadmaster.tk

import sys, re, os
from datetime import datetime
from datetime import timedelta

 
def lrc2srt(lrc):
	p = re.compile("[0-9]+")
	#filename = sys.argv[1]
	#interval = str(sys.argv[2])

	#lrc = open(filename)

	listtime =  []
	listlyrics = []

	for line in lrc.readlines():
		if p.match(line.split(":")[0].replace("[","")):
			listtime.append("00:" + line.split("]")[0].replace("[","")+"0")
			listlyrics.append(line.split("]")[1])
			
	#read file and delete empty&useless lines

	# detect timestamp format
	ts_fmt_str="%H:%M:%S.%f"
	#for ts_str in listtime:
	#    if not "." in ts_str:
	#        ts_fmt_str = ts_fmt_str.replace(".%f","")
	#    if len(ts_str)==4:
	#        ts_fmt_str="%M:%S"
	# end for

	o=""
	i=0
	#listtime[i].replace(".",",")+\
	while i <= listtime.__len__()-2:


		#print(listtime[i])
		#print( ts_fmt_str)
		#print(datetime.strptime("1","%S"))
		start_time = (datetime.strptime(listtime[i], ts_fmt_str)-datetime.strptime("1","%S"))

			
		if (start_time.days < 0 ):
			start_time = (datetime.strptime(listtime[i], ts_fmt_str)-datetime.strptime("0","%S"))
		#if (start_time.microseconds == 0 ):
		#	start_time = start_time+timedelta(microseconds=1) # add 1 msec to avoid empty msec field

		o = o+\
		str(i+1)+\
		"\n"+\
		"0" + str(start_time).replace("000","").replace(".",",") +\
		" --> " +\
		listtime[i+1].replace(".",",")+\
		"\n"+listlyrics[i]+\
		"\n"
		i=i+1
	# end while

	o = o + str(i+1) + "\n" + listtime[-1].replace(".",",")+ " --> " + "\n" + listlyrics[-1] + "\n"
	return o


if __name__ == "__main__":
	import argparse, sys
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', nargs='?', default="-", help="input file, default to stdin if unspecified. Supports passing urls.")
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file, default to stdout if unspecified")
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
	
	
	o = lrc2srt(infile)
	args.outfile.write(o)
