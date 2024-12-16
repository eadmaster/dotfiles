#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: pure python alternative
#def wkt2geojson_dicts(wkt_str):

def shapely_wkt2geojson_dict(wkt_str):
	import shapely.wkt, shapely.geometry
	parsed_dicts = []
	for line in wkt_str.splitlines():
		if line.strip() == "" or line.startswith("#"):  # skip empty lines and comments
			continue
		s = shapely.wkt.loads( line ) # WKT string -> shapely object
		geojson_dict = shapely.geometry.mapping(s)  # # shapely object -> GeoJSON dict
		parsed_dicts.append({"geometry": geojson_dict})
	return(parsed_dicts)


# main program
if __name__ == "__main__":
	import sys
	import json
	
	if len(sys.argv) > 1:
		wtk_str = open(sys.argv[1], "rb").read()
	else:
		sys.stderr.write("reading from stdin...\n")
		wtk_str = sys.stdin.read()
	
	geojson_dict = shapely_wkt2geojson_dict(wtk_str)
	print(json.dumps(geojson_dict))
