#!/usr/bin/python
# -*- coding: utf-8 -*-


# TODO: https://stackoverflow.com/questions/51382409/programmatically-render-geojson-to-image-file
# https://medium.com/@h4k1m0u/plot-a-geojson-map-using-geopandas-be89e7a0b93b



def shapely_geojson2map(geojson_str):
	from shapely.geometry import mapping, shape
	# GeoJSON dict -> shapely object
	geojson_dict = json.loads(geojson_str)
	s = shape(geojson_dict)
	# "s" will be istantiated as the matching object
	import matplotlib.pyplot as plt
	# TODO: load earth map
	x,y = s.exterior.xy
	plt.plot(x,y)
	#plt.plot(*poly.exterior.xy) # more concise
	plt.show()
	return()


# main program
if __name__ == "__main__":
	import sys
	import json
	
	if len(sys.argv) > 1:
		geojson_str = open(sys.argv[1], "rb").read()
	else:
		sys.stderr.write("reading from stdin...\n")
		geojson_str = sys.stdin.read()
	
	shapely_geojson2map(geojson_str)

