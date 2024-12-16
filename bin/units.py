#!/usr/bin/python
# -*- coding: utf-8 -*-


def sympy_units_conversion(v_str, u1_str, u2_str):
	# https://stackoverflow.com/questions/1025145/units-conversion-in-python
	# https://superuser.com/questions/134661/quick-unit-aware-calculator
	# https://python.plainenglish.io/unit-conversion-in-python-3ee480d4b19c
	import sympy
	from sympy.physics import units
	from sympy.physics.units import convert_to
	u1 = getattr(units, u1_str) # units.find_unit(u1_str)
	u2 = getattr(units, u2_str)
	v = float(v_str)
	out = convert_to(v * u1, u2)
	return(out)

def scipy_units_conversion(v_str, u1_str, u2_str):
	from scipy import constants
	u1 = getattr(constants, u1_str)
	u2 = getattr(constants, u2_str)
	v = float(v_str)
	return(v*u1/u2)

	
if __name__ == "__main__":
	import sys
	import logging
	import os

	PROGRAM_NAME = os.path.basename(sys.argv[0])

	if(len(sys.argv) < 3 or sys.argv[1] in ['-h', '--help']):
		print("usage: " + PROGRAM_NAME + " val unit1 unit2")
		sys.exit(1)
	
	v_str = sys.argv[1]
	u1_str = sys.argv[2]
	u2_str = sys.argv[3]
		
	print("sympy output:")
	print(sympy_units_conversion(v_str, u1_str, u2_str))
	
	#print("scipy output:")  # missing meters, sub-units?
	#print(scipy_units_conversion(v_str, u1_str, u2_str))
	
	# TODO: pure python alt.

