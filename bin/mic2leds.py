#!/usr/bin/python3
# -*- coding: utf-8 -*-

# audio visualization script by eadmaster
# http://eadmaster.altervista.org/pub/index.php?page=electr#audioleds

# TODO: try porting  https://github.com/scottlawsonbc/audio-reactive-led-strip
#   https://github.com/justcallmekoko/Arduino-FastLED-Music-Visualizer
# TODO: try  https://ledfx.readthedocs.io/en/latest/directing_audio.html
#   -> mv mic2leds.py audio2leds.py
#WANTED: pulseaudio builtin spectrogram
#	https://askubuntu.com/questions/1139445/real-time-audio-visualization-program-to-use-with-any-sound-source
#	https://github.com/vsergeev/audioprism
#	https://github.com/hannesha/GLMViz

	

import alsaaudio
import audioop
import serial
import sys
import math
import string
import os
from time import sleep


import socket
HOSTNAME=socket.gethostname()

# rpi/orangepi mode (control a few LEDs directly via GPIO pins)
WIRINGPI_MODE=False
RGB_HUE_LED=False
if(WIRINGPI_MODE):
	# init leds using wiringPi
	import wiringpi
	wiringpi.wiringPiSetup()
	blue_led = 1
	red_led = 16
	yellow_led = 0
	wiringpi.pinMode(blue_led, wiringpi.OUTPUT)
	wiringpi.pinMode(red_led, wiringpi.OUTPUT)
	wiringpi.pinMode(yellow_led, wiringpi.OUTPUT)
	#if(RGB_HUE_LED):
	#	rgb_red = ?
	#	rgb_green = ?
	#	rgb_blue = ?
	#	wiringpi.pinMode(rgb_red, wiringpi.OUTPUT)
	#	wiringpi.pinMode(rgb_blue, wiringpi.OUTPUT)
	#	wiringpi.pinMode(rgb_green, wiringpi.OUTPUT)
# end of orangepi mode initialization

# detect if a led matrix is connected via a CH340-based Arduino
LED_MATRIX_CONNECTED=True
#lrc_control_str = ''
#if(os.path.exists("/dev/ttyUSB0")):
if LED_MATRIX_CONNECTED:
	# init serial connection
	import serial
	if os.path.exists('/dev/ttyUSB0'):
		tamino_ser = serial.Serial('/dev/ttyUSB0', 115200)
	elif os.path.exists('/dev/ttyACM0'):
		tamino_ser = serial.Serial('/dev/ttyACM0', 115200)
	else:
		print("serial port for led matrix not found")
		exit(1)
	#tamino_ser.write("00000000000lyrics here 2\n")
	tamino_control_str_old = ""
	tamino_player_str_old = ""
	tamino_album_art_str_old = ""
LYRICS_DISPLAY=True
LRC_SEARCH_PATH = os.path.expandvars(os.path.expanduser("$HOME/lyrics"))
LYRICS_TIME_OFFSET=0  # show the lyrics 1 second earlier (good for karaok)

UPNP_LISTENING=False
UPNP_NET_INTERFACE="lo"  # network interface or IP to look for UPNP DLNA services (will detect current playing song from these)
#UPNP_NET_INTERFACE="wlan0"
#UPNP_NET_INTERFACE="192.168.1.133"
OSD_LYRICS = False   # show the current lyrics line via OSD (osdlyrics-like). Must have osd_cat from xosd-bin installed
OSD_LYRICS_MAX_CHARS_PER_LINE = 1920/96  # (current screen width)/(current font width)
OSD_LYRICS_FONT = "-misc-fixed-medium-r-*--96-*-*-*-c-*-*-*"
#lrc_control_str=""
#LYRICS_WEB_SERVICE=True  # show the current lyrics via a web service
if(LYRICS_DISPLAY):
	import threading
	
	if UPNP_LISTENING:
		# start the upnp events listening thread
		
		threading.Thread(target=upnp_event_listening_thread).start()
	else:
		# listen via d-bus
		from mediaplayerstatus2lrc import *
		threading.Thread(target=dbus_event_listening_thread).start()


LED_STRIP_CONNECTED=False
LED_STRIP_NO_PIXELS=18
LED_STRIP_USE_BOBLIGHT=False
LED_STRIP_BOBLIGHT_SERVER_ADDR="127.0.0.1"
LED_STRIP_BOBLIGHT_SERVER_PORT=19333

# detect if a led strip is connected
# MEMO: the arduino must be running http://eadmaster.altervista.org/pub/prj/electr/rgb_strip_serial.ino
# MEMO: remember to increase the serial buffer size >90 in /usr/share/arduino/hardware/arduino/cores/arduino/HardwareSerial.cpp
#if(os.path.exists('/dev/ttyACM0')):
if LED_STRIP_CONNECTED:
	if(LED_STRIP_USE_BOBLIGHT):
		import pyboblight
		bob = pyboblight.BobCLient(host=LED_STRIP_BOBLIGHT_SERVER_ADDR, port=LED_STRIP_BOBLIGHT_SERVER_PORT)
		bob_right_leds = sorted(({k:v for k,v in bob.lights.iteritems() if k.startswith("Right")}).values(), key=lambda x: x.name)
		bob_left_leds = sorted(({k:v for k,v in bob.lights.iteritems() if k.startswith("Left")}).values(), key=lambda x: x.name)
		bob_top_leds = sorted(({k:v for k,v in bob.lights.iteritems() if k.startswith("Top")}).values(), key=lambda x: x.name)
	else:
		import serial
		arduino_ser = serial.Serial('/dev/ttyACM0', 115200)
		#sleep(5)
		#arduino_ser.write("0\n")
		arduino_control_str_old = ""

 
#def turnoff_all_leds():
#	if(WIRINGPI_MODE):
#		wiringpi.digitalWrite(blue_led, 0)
#		wiringpi.digitalWrite(red_led, 0)
#		wiringpi.digitalWrite(yellow_led, 0)
#		if(RGB_HUE_LED):
#			wiringpi.digitalWrite(rgb_red, 1)
#			wiringpi.digitalWrite(rgb_blue, 1)
#			wiringpi.digitalWrite(rgb_green, 1)
#	#if LED_STRIP_CONNECTED:
#	#	ser.write('0\n')

# parse args
import sys
PROGRAM_NAME = os.path.basename(sys.argv[0])
if(len(sys.argv)>=2):
	if(sys.argv[1]=='-h' or sys.argv[1]=='--help'):  # 
		print("usage: " + PROGRAM_NAME + " [audiofile]")
		print("if no audiofile is specified will read the microphone")
		exit(0)
	# else
	# local file playback mode (code derived from https://raw.githubusercontent.com/larsimmisch/pyalsaaudio/master/playwav.py )
	import wave
	f = wave.open(sys.argv[0], 'rb')
	# 2FIX: "wave.Error: file does not start with RIFF id"
	device = alsaaudio.PCM(device='default')
	device.setchannels(f.getnchannels())
	device.setrate(f.getframerate())
	# 8bit is unsigned in wav files
	if f.getsampwidth() == 1:
		device.setformat(alsaaudio.PCM_FORMAT_U8)
	# Otherwise we assume signed data, little endian
	elif f.getsampwidth() == 2:
		device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	elif f.getsampwidth() == 3:
		device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
	elif f.getsampwidth() == 4:
		device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
	else:
		#raise ValueError('Unsupported format')
		print('Unsupported format')
	periodsize = f.getframerate() / 8
	device.setperiodsize(periodsize)
    
else:
	# initialize the microphone input
	#original code from https://blog.blinkenlight.net/experiments/basic-effects/vu-meter/
	# TODO: rewrite using pulseaudio http://freshfoo.com/posts/pulseaudio_monitoring/
	input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NORMAL, 'pulse')  # PCM_NONBLOCK
	#input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
	#CHUNK = 320
	CHUNK = 1000
	#CHUNK = 4000
	SAMPLE_RATE = 32000  # MEMO: 8000 is ok for vumeter only
	input.setchannels(1) # Mono
	input.setrate(SAMPLE_RATE)
	input.setformat(alsaaudio.PCM_FORMAT_S16_LE)  # 16 bit little endian
	input.setperiodsize(CHUNK)

spectrum_matrix    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
spectrum_power     = []
#OLD: spectrum_weighting = [1, 1, 2, 4, 8, 8, 8, 8, 16, 16, 16]
spectrum_weighting = [1, 1, 2, 2, 4, 8, 8, 32, 32, 64, 64]

from struct import unpack
import numpy as np

def spectrum_power_index(val):
    return int(2 * CHUNK * val / SAMPLE_RATE)

def spectrum_compute_fft(data):      
    global spectrum_matrix
    data = unpack("%dh" % (len(data) / 2), data)
    data = np.array(data, dtype='h')

    fourier = np.fft.rfft(data)
    fourier = np.delete(fourier, len(fourier) - 1)

    spectrum_power = np.abs(fourier)
    
    # split our frequency spectrum up into 11 bands to display 
    # code from https://learn.pimoroni.com/tutorial/sandyj/scroll-phat-spectrum-analyser
    spectrum_matrix[0] = int(np.mean(spectrum_power[spectrum_power_index(0)    :spectrum_power_index(156) :1]))
    spectrum_matrix[1] = int(np.mean(spectrum_power[spectrum_power_index(156)  :spectrum_power_index(313) :1]))
    spectrum_matrix[2] = int(np.mean(spectrum_power[spectrum_power_index(313)  :spectrum_power_index(625) :1]))
    spectrum_matrix[3] = int(np.mean(spectrum_power[spectrum_power_index(625)  :spectrum_power_index(1000) :1]))
    spectrum_matrix[4] = int(np.mean(spectrum_power[spectrum_power_index(1000) :spectrum_power_index(2000) :1]))
    spectrum_matrix[5] = int(np.mean(spectrum_power[spectrum_power_index(2000) :spectrum_power_index(3000) :1]))
    spectrum_matrix[6] = int(np.mean(spectrum_power[spectrum_power_index(3000) :spectrum_power_index(4000) :1]))
    spectrum_matrix[7] = int(np.mean(spectrum_power[spectrum_power_index(4000) :spectrum_power_index(5000) :1]))
    spectrum_matrix[8] = int(np.mean(spectrum_power[spectrum_power_index(5000) :spectrum_power_index(6000) :1]))
    spectrum_matrix[9] = int(np.mean(spectrum_power[spectrum_power_index(6000) :spectrum_power_index(7000) :1]))
    spectrum_matrix[10] = int(np.mean(spectrum_power[spectrum_power_index(7000):spectrum_power_index(8000) :1]))
        
    spectrum_matrix = np.divide(np.multiply(spectrum_matrix, spectrum_weighting), 50000)
    spectrum_matrix = spectrum_matrix.clip(0, 9)  # trim values bigger than 9
    #spectrum_matrix = spectrum_matrix.clip(0, 8)
    #spectrum_matrix = [float(m) for m in spectrum_matrix]
    
    # ALTERNATIVE: https://www.raspberrypi.org/forums/viewtopic.php?t=35838&p=454041
    # Find amplitude
    #power = np.log10(np.abs(fourier))**2
    # Araange array into 8 rows for the 8 bars on LED matrix
    #power = np.reshape(power,(4,CHUNK/4))
    #spectrum_matrix= np.int_(np.average(power,axis=1)/4)

    return spectrum_matrix
# end of spectrum_compute_fft
   

lo  = 2000
hi = 32000
log_lo = math.log(lo)
log_hi = math.log(hi)
di=dict(zip(string.ascii_letters,[ord(c)%32 for c in string.ascii_letters]))
v=0

print ("Press CTRL+C to exit")


def cleanup_lrc_line(s):
	r = s.strip()
	r = r.replace("  ", " ")
	return r


#main loop

import mediaplayerstatus2lrc

try:
	while True:
		if(len(sys.argv)>=2):
			# wave file mode
			data = f.readframes(periodsize)
			device.write(data)
			datalen = periodsize
		else:
			# microphone mode
			#data_in.pause(0) # Resume capture
			datalen, data = input.read()
			#data_in.pause(1) # Pause capture whilst RPi processes data

		if( datalen > 0 ):
			# transform data to logarithmic scale
			vu = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)
			l = (chr(ord('a')+min(max(int(vu*20),0),19)))
			prev_v = v
			v = di[l]
			#DEBUG: print(v)
			if(WIRINGPI_MODE and v!=prev_v):
				#if(v<2):
				#	turnoff_all_leds()
				if(v>=2):
					wiringpi.digitalWrite(blue_led, 1)
				else:
					wiringpi.digitalWrite(blue_led, 0)
				if(v>=8):
					wiringpi.digitalWrite(red_led, 1)
				else:
					wiringpi.digitalWrite(red_led, 0)
				if(v>=10):
					wiringpi.digitalWrite(yellow_led, 1)
				else:
					wiringpi.digitalWrite(yellow_led, 0)
				# rgb led control
				if(RGB_HUE_LED):
				#TODO: softPWM mode?
				#TODO: re-check else | re-enable turnoff_all_leds()
				#redVal = (v >> 2) & 0xE0; # Values 0, 32, 64, 96 ... 224
				#grnVal = (v << 1) & 0x78; # Values 0, 16, 32, 48 ... 240
				#bluVal = (v << 5) & 0xE0; # Values 0, 32, 64, 96 ... 224
				#print(redVal)
				#print(grnVal)
				#print(bluVal)
					if(v<2):
						# turn off
						wiringpi.digitalWrite(rgb_red, 1)
						wiringpi.digitalWrite(rgb_blue, 1)
						wiringpi.digitalWrite(rgb_green, 1)
					if(v>=2):
						# green
						wiringpi.digitalWrite(rgb_green, 0)
					if(v>=5):
						# yellow
						wiringpi.digitalWrite(rgb_red, 0)
					else:
						wiringpi.digitalWrite(rgb_red, 1)
					if(v>=8):
						# pink
						wiringpi.digitalWrite(rgb_green, 1)
						wiringpi.digitalWrite(rgb_blue, 0)
					else:
						wiringpi.digitalWrite(rgb_green, 0)
						wiringpi.digitalWrite(rgb_blue, 1)
					if(v>=11):
						# red
						wiringpi.digitalWrite(rgb_blue, 1)
					else:
						wiringpi.digitalWrite(rgb_blue, 0)
			# end of WIRINGPI_MODE
			
			if(LED_STRIP_CONNECTED or LED_MATRIX_CONNECTED):
				# compute the spectrum
				spectrum_matrix = spectrum_compute_fft(data)
				#print(spectrum_matrix)

			# led strip vumeter mode
			#v = int(v/1.5) # reduce the current value a bit
			if(LED_STRIP_CONNECTED):
				if LED_STRIP_USE_BOBLIGHT:
					# update the led strip via boblight
					def matrix_value_to_color(v):
						if(v==1):
							# black/turn off
							return([0,0,0])
						elif(v>=7):
							# red
							return([255,0,0])
						elif(v>=5):
							# yellow
							return([255,255,0])
						elif(v>=3):
							# green
							return([0,255,0])
						elif(v>=1):
							# blue
							return([0,0,255])
						else:
							return([0,0,0])
					
					sorted_leds = bob_right_leds + bob_top_leds
					i=0
					for x in (spectrum_matrix[0:10]):
						sorted_leds[i].set_color(*matrix_value_to_color(x))
						i += 1
					i=0
					for x in (spectrum_matrix[0:5][::-1]):  # reversed array
						bob_left_leds[i].set_color(*matrix_value_to_color(x))
						i += 1
					bob.update()

				else:
					# update the led strip via serial
					arduino_control_str = ""
					for i in range(0): # DISABLED
					#for i in range(30):
						#if(v==0):
						if(v==1):
							# black/turn off
							arduino_control_str += chr(0) + chr(0) + chr(0)
						elif(v>=7):
							# red
							arduino_control_str += chr(150) + chr(0) + chr(0)
						elif(v>=5):
							# yellow
							arduino_control_str += chr(150) + chr(150) + chr(0)
						elif(v>=3):
							# green
							arduino_control_str += chr(0) + chr(150) + chr(0)
						elif(v>=1):
							# blue
							arduino_control_str += chr(0) + chr(0) + chr(150)
						else:
							arduino_control_str += chr(0) + chr(0) + chr(0)
					# ALTERNATIVE: led strip spectrogram mode
					for x in (spectrum_matrix[0:10]):
					#for x in []:  # DISABLED
						#if(v==0):
						if(x<=1):
							# black/turn off
							arduino_control_str += chr(0) + chr(0) + chr(0)
							arduino_control_str += chr(0) + chr(0) + chr(0)
						elif(x>=7):
							# red
							arduino_control_str += chr(150) + chr(0) + chr(0)
							arduino_control_str += chr(150) + chr(0) + chr(0)
						elif(x>=5):
							# yellow
							arduino_control_str += chr(150) + chr(150) + chr(0)
							arduino_control_str += chr(150) + chr(150) + chr(0)
						elif(x>=3):
							# green
							arduino_control_str += chr(0) + chr(150) + chr(0)
							arduino_control_str += chr(0) + chr(150) + chr(0)
						elif(x>=2):
							# blue
							arduino_control_str += chr(0) + chr(0) + chr(150)
							arduino_control_str += chr(0) + chr(0) + chr(150)
					# repeat the right part on the left
					for x in (spectrum_matrix[0:5][::-1]):  # reversed array
						if(x<=1):
							# black/turn off
							arduino_control_str += chr(0) + chr(0) + chr(0)
							arduino_control_str += chr(0) + chr(0) + chr(0)
						elif(x>=7):
							# red
							arduino_control_str += chr(150) + chr(0) + chr(0)
							arduino_control_str += chr(150) + chr(0) + chr(0)
						elif(x>=5):
							# yellow
							arduino_control_str += chr(150) + chr(150) + chr(0)
							arduino_control_str += chr(150) + chr(150) + chr(0)
						elif(x>=3):
							# green
							arduino_control_str += chr(0) + chr(150) + chr(0)
							arduino_control_str += chr(0) + chr(150) + chr(0)
						elif(x>=2):
							# blue
							arduino_control_str += chr(0) + chr(0) + chr(150)
							arduino_control_str += chr(0) + chr(0) + chr(150)
					
					#DEBUG: print(len(arduino_control_str))
					# TODO: slower updates?
					#import time
					#if((int(time.time()) % 2) and
					# optimization to avoid retransfering the same string
					if(arduino_control_str_old != arduino_control_str):
						arduino_ser.write(arduino_control_str)
						arduino_control_str_old = arduino_control_str
					# else skip the update
			# end LED_STRIP_CONNECTED
			
			if(LED_MATRIX_CONNECTED):
				# update the rgb matrix
				#for i in range(3):
				#	if(i==0):
				#		continue
				#	for j in range(spectrum_matrix[i-1]):
				#		arduino_control_str[4+(i-1)*16+j]='|'
				tamino_control_str = (''.join('%d' %x for x in spectrum_matrix))
				# append the lyrics line (will be buffered by the arduino after sending)
				#global lrc_control_str
				if(mediaplayerstatus2lrc.lrc_control_str!=""):
					tamino_control_str += cleanup_lrc_line(mediaplayerstatus2lrc.lrc_control_str)
					mediaplayerstatus2lrc.lrc_control_str = "" # the line will be buffered on the arduino
				# MEMO: arduino default serial buffer size is 64-bytes
				# truncate the string if necessary
				#if(len(tamino_control_str)>=64):
				#	tamino_control_str = tamino_control_str[0:63]
				if(tamino_control_str_old != tamino_control_str):
					tamino_ser.write((tamino_control_str+'\n').encode())
					tamino_control_str_old = tamino_control_str
					print(tamino_control_str)
				# also output media plyer state
				#print(mediaplayerstatus2lrc.last_time_update)
				#print(mediaplayerstatus2lrc.curr_state_str)
				player_state_str = mediaplayerstatus2lrc.curr_state_str
				if(tamino_player_str_old != player_state_str):
					tamino_ser.write((player_state_str+'\n').encode())
					tamino_player_str_old = player_state_str
					print(player_state_str)
				if True:
					album_art_str = mediaplayerstatus2lrc.curr_album_art_base64_str
					if ( tamino_album_art_str_old != album_art_str):
						tamino_ser.write(("BMP: "+album_art_str+'\n').encode())
						tamino_album_art_str_old = album_art_str
						print(album_art_str)
				# else skip the update
				# end LED_STRIP_CONNECTED
				
		#sleep(0.005)
		sleep(0.01)
		#turnoff_all_leds()

		# end of main loop
except:
	import traceback
	traceback.print_exc(file=sys.stdout)
	#continue
finally:
	#turnoff_all_leds()
	if LED_STRIP_CONNECTED:
		if LED_STRIP_USE_BOBLIGHT:
			bob.disconnect()
		else:
			arduino_ser.close()
	if LED_MATRIX_CONNECTED:
		tamino_ser.close()

