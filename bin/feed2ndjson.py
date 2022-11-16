#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: pure python ver
#def feed2dicts(feed_str):
	
	
def feedparser_feed2dicts(feed_str):
	import datetime
	import feedparser
	parsed_dicts = []
	curr_dict = {}
	feed = feedparser.parse(feed_str)
	for entry in feed['entries']:
		#entry.published = datetime.datetime.strptime( entry.published, "%Y-%m-%dT%H:%M:%S" )
		parsed_dicts.append(entry)
	return(parsed_dicts)


# main program
if __name__ == "__main__":
	import sys
	import json
	
	if len(sys.argv) > 1:
		feed_str = open(sys.argv[1], "rb").read()
		# TODO: allow reading remote urls
	else:
		sys.stderr.write("reading from stdin...\n")
		feed_str = sys.stdin.read()

	feed_dicts = feedparser_feed2dicts(feed_str)
	for d in feed_dicts:
		print(json.dumps(d))

