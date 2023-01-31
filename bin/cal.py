#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime


from ical2ndjson import *

MY_ICAL_URL = os.getenv('MY_ICAL_URL')

if __name__ == "__main__":

	# print this month calendar  + highlight today https://stackoverflow.com/questions/66021616/highlighting-todays-date-in-python-using-calendar-py-in-command-prompt-windows
	from datetime import date
	import calendar
	import time
	import re
	now = datetime.now()
	today = date.today()
	#print(calendar.month(now.year, now.month))
	thism = calendar.month(now.year, now.month)    # current month
	date  = today.day.__str__().rjust(2)
	rday  = ('\\b' + date + '\\b').replace('\\b ', '\\s')
	rdayc = "\033[7m" + date + "\033[0m"
	#             7 Swaps foreground and background colors
	print( re.sub(rday,rdayc,thism))
		
	# read remote calendar and print this month's events
	from urllib.request import urlopen
	import ssl
	infile = urlopen(MY_ICAL_URL, context=ssl.SSLContext())
		
	ical_str = infile.read()
	ical_dicts = ical2dicts(ical_str)
	
	import json
	for d in ical_dicts:
		#print(d)
		#continue
		start_dt = None
		end_dt = None
		if "dtstart" in d:
			start_dt = datetime.strptime( d["dtstart"],  "%Y%m%dT%H%M%S" + ('Z' if d["dtstart"].endswith('Z') else ''))
		if "dtend" in d:
			end_dt = datetime.strptime( d["dtend"], "%Y%m%dT%H%M%S" + ('Z' if d["dtend"].endswith('Z') else ''))
		if "dtstart;value=date" in d:
			start_dt = datetime.strptime( d["dtstart;value=date"], "%Y%m%d" )
		if "dtend;value=date" in d:
			end_dt = datetime.strptime( d["dtend;value=date"], "%Y%m%d" )
		if not start_dt or not end_dt:
			continue
		if not (now >= start_dt and now<= end_dt):
			continue
		# else
		date_formatted = start_dt.strftime('%b %d') +"->" + end_dt.strftime('%b %d')
		summary = d["summary"]
		print(date_formatted + '  ' + summary)
		#print(d)
	