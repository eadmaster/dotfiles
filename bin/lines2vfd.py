#!/usr/bin/env python
# -*- coding: utf-8 -*-

# derived from https://github.com/cnorlander/USB2VFD-Deck/


import serial
import time
import pytz
from datetime import datetime, timezone
from zoneinfo import ZoneInfo



def serial_connect(serial_port):
    serial_conn = None
    while True:
        exception_tossed = False
        try:
            serial_conn = serial.Serial(
                port=serial_port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
        except serial.serialutil.SerialException as e:
            exception_tossed = True
        if not exception_tossed:
            return serial_conn
        print("Connection Failed... Waiting to try again...")
        time.sleep(5)

class SerialVFD:
	GO_HOME = bytearray.fromhex("fe48")
	GO_LINE_2 = bytearray.fromhex("fe470102")
	SET_BRIGHTNESS = bytearray.fromhex("fe99")
	SET_BRIGHTNESS_LOW = bytearray.fromhex("fe990a")
	MAX_FRAME_RATE = 10

	def __init__(self, serial_port, nc_message: str = "DISCONNECTED"):
		self.serial_port = serial_port
		self.serial_conn = serial_connect(serial_port)
		self.last_frame_time = time.time()
		self.nc_message = nc_message

	def push_frame(self, line_1_byte_array: bytearray, line_2_byte_array: bytearray):
		now = time.time()
		time_delta = now - self.last_frame_time
		self.last_frame_time = now
		frame_limit = 1.0 / SerialVFD.MAX_FRAME_RATE
		if time_delta >= frame_limit:
			try:
				self.serial_conn.write(SerialVFD.GO_HOME)
				self.serial_conn.write(line_1_byte_array)
				self.serial_conn.write(SerialVFD.GO_LINE_2)
				self.serial_conn.write(line_2_byte_array)
			except serial.serialutil.SerialException as e:
				self.serial_conn = serial_connect(self.serial_port)

	def set_brightness(self, value):
		# value range 0-255
		if not value >= 0 or not value <= 255:
			return
		try:
			#self.serial_conn.write(SerialVFD.SET_BRIGHTNESS)
			#self.serial_conn.write(bytearray(value.to_bytes(1, byteorder='big')))
			#time.sleep(1)
			self.serial_conn.write(bytes([0xfe,0x99,0x64]))
		except serial.serialutil.SerialException as e:
			self.serial_conn = serial_connect(self.serial_port)



def rotate_long_message(message, message_max_length: int = 40):
    return message[1:] + message[0]

class MessageFormatter:
    def __init__(self, scroll_speed: float, req_line_length: int = 40):
        self.scroll_speed = scroll_speed
        self.req_line_length = req_line_length

    def enforce_line_length(self, line: str) -> str:
        if len(line) < self.req_line_length:
            line = line + (" " * (self.req_line_length - len(line)))
        return line[0:self.req_line_length]

    def format_line(self, line) -> bytearray:
        line_set_length = self.enforce_line_length(line)
        line_byte_array = bytearray()
        line_byte_array.extend(map(ord, line_set_length))
        return line_byte_array


import sys


line_1_message = "lines2vfd"
line_2_message = "init OK"



import threading

formatter = MessageFormatter(scroll_speed=0.1)

    
def refresh_screen_thread_main():
	global line_1_message
	global line_2_message
	
	vfd = SerialVFD('/dev/ttyUSB0')
	time.sleep(0.5)
	vfd.set_brightness(10)
	time.sleep(0.5)
	
	while True:
		
		line_1_byte_array = formatter.format_line(line_1_message)
		line_2_byte_array = formatter.format_line(line_2_message)
		vfd.push_frame(line_1_byte_array, line_2_byte_array)
		
		if(len(line_1_message)>40):
			line_1_message = rotate_long_message(line_1_message)
		if(len(line_2_message)>40):
			line_2_message = rotate_long_message(line_2_message)
		time.sleep(0.1)


def main():

	global line_1_message
	global line_2_message

	#local_timezone = pytz.timezone("America/Los_Angeles")
	#line_1_message = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890@#$%^&*()_-+={}[]:;?/>|!@#$%^&*()_-+={}[]:;?/><|.,`~"

	refresh_screen_thread = threading.Thread(target=refresh_screen_thread_main, args=[])
	refresh_screen_thread.start()

	while True:

		#sys.stdin.flush()
		curr_line_1_message = sys.stdin.readline()
		if curr_line_1_message:
			line_1_message = curr_line_1_message
			print(line_1_message)
		curr_line_2_message = sys.stdin.readline()
		if curr_line_2_message:
			line_2_message = curr_line_2_message
			print(line_2_message)
		



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()



