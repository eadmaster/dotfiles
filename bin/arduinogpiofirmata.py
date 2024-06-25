#!/usr/bin/env python3

# TODO: add support for all rpio gpio args: readall  https://www.ics.com/blog/gpio-programming-using-sysfs-interface#:~:text=The%20gpio%20Utility,more%20advanced%20functions%20like%20PWM.

import sys
import argparse
parser = argparse.ArgumentParser()

# https://stackoverflow.com/questions/23304740/optional-python-arguments-without-dashes-but-with-additional-parameters
#parser.add_argument("-v", "--version", help="...", action="store_true")
parser.add_argument("--device", nargs=1, default="/dev/ttyACM0", help="...")
sp = parser.add_subparsers(dest='cmd')
spp = sp.add_parser("mode")
spp.add_argument('pin', type=int)
spp.add_argument('mode')
spp = sp.add_parser("read")
spp.add_argument('pin', type=int)
spp = sp.add_parser("write")
spp.add_argument('pin', type=int)
spp.add_argument('value', type=int)
spp = sp.add_parser("readall")
args = parser.parse_args()
#print(args)

import pyfirmata
from pyfirmata import Arduino, util
board = Arduino(args.device)
#board.iterate()

if(args.cmd == "mode"):
	pin = args.pin
	mode = args.mode
	if mode == "out":
		mode = 1
	elif mode == "in":
		mode = 0
	if not mode in [pyduino.DIGITAL_OUTPUT, pyduino.DIGITAL_INPUT]:  # pyduino.DIGITAL_PWM
		print("error: unsupported mode")
		sys.exit(1)
	# else
	print("setting mode " + str(mode) + " to pin " + str(pin))	
	board.digital[pin]._set_mode(mode)

elif(args.cmd == "read"):
	pin = args.pin
	board.digital[pin].set_active(1)
	value = board.analog[pin].read()
	print(value)

elif(args.cmd == "readall"):
	print("+------+------+------+---+")
	print("| Pin  | Name | Mode | V |")
	print("+------+------+------+---+")

	# Iterate over all pins
	for pin_number in range(len(board.digital)):
		pin = board.digital[pin_number]
		if pin.mode == pyfirmata.INPUT:
			mode="IN"
		elif pin.mode == pyfirmata.OUTPUT:
			mode="OUT"
		#elif pin.mode == pyfirmata.ANALOG:
		#elif pin.mode == pyfirmata.PWM:
		#elif pin.mode == pyfirmata.SERVO:
		else:
			mode=str(pin.mode)
		
		# TODO: fix reading current value
		val = None
		if pin.mode == pyfirmata.INPUT:
			val = pin.read()
		
		#print("+-----+------+------+---+")
		print("|  %2d  |      |  %3s  | %s |" % (pin_number, mode, val))

	# Iterate over all analog pins
	for pin_number in range(len(board.analog)):
		pin = board.analog[pin_number]
		print("|  A%d  |      |  %3s  |  %s |" % (pin_number, mode, pin.value))

	# Print the table footer
	print("+------+------+------+---+")
	
elif(args.cmd == "write"):
	pin = args.pin
	new_value = args.value  # high (1) or low (0)
	if not new_value in [0, 1]:
		print("error: unsupported vlue")
		sys.exit(1)
	# else
	print("setting value " + str(new_value) + " to pin " + str(pin))
	#board.digital[pin].set_active(1)
	board.digital[pin].set_mode(pyfirmata.OUTPUT)
	board.digital[pin].write(new_value)
	
else:
	print("unsupported cmd")

#import time
#time.sleep(1)
#board.iterate()
board.exit()

