#!/usr/bin/env python


USE_EXTERNAL_SPEAKERS=False
INTERNAL_SPEAKER_USING_BEEP_CMD = True
INTERNAL_SPEAKER_USING_DEV_CONSOLE = False

# use internal speaker on some PCs
# ~ import socket
# ~ HOSTNAME=socket.gethostname()
# ~ if(HOSTNAME=='BOSS2'):
	# ~ USE_EXTERNAL_SPEAKERS=False
	# ~ INTERNAL_SPEAKER_USING_DEV_CONSOLE = False


import os

_tone_fd = None
stream = None

def tone(freq, msec):
	#print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
	beepcmd = "beep -f " + str(freq) + " -d " + str(msec)
	# TODO: truncate freq with many digits for better compatibility?
	print(beepcmd)  # output the corresponding beep command
	sec = (msec / 1000.0) # lenght in seconds (float)
	if(USE_EXTERNAL_SPEAKERS):
		# code from  https://askubuntu.com/questions/202355/how-to-play-a-fixed-frequency-sound-using-python
		# WANTED: alternative method using ossaudiodev or audiodev (removed in Python 3.x)
		if(not stream):  # lazy init stream
			import pyaudio
			p = pyaudio.PyAudio()
			stream = p.open(format=p.get_format_from_width(1), channels=1, rate=44100, output=1)
			import atexit
			atexit.register(stream.close)
			atexit.register(p.terminate)
		# end if
		import math
		BITRATE = 44100
		NUMBEROFFRAMES = int(BITRATE * sec)
		RESTFRAMES = NUMBEROFFRAMES % BITRATE
		WAVEDATA = ''  
		if(freq!=0):  # prevent division by 0
			for x in xrange(NUMBEROFFRAMES):
				WAVEDATA += chr(int(math.sin(x / ((BITRATE / freq) / math.pi)) * 127 + 128))
		#fill remainder of frameset with silence
		for x in xrange(RESTFRAMES): 
			WAVEDATA += chr(128)
		stream.write(WAVEDATA)
		return
	# end of USE_EXTERNAL_SPEAKERS
	# else use the internal PC speaker
	import os
	if(os.name=="nt"):
		try:
			import winsound
			winsound.Beep(freq, sec)
		except:
			pass
		else:
			# no exception
			return
	else:
		# assuming Unix-like OS
		import time
		try:
			if(INTERNAL_SPEAKER_USING_DEV_CONSOLE):
				# old method using fcntl (more portable but req. root priviledges) https://gist.github.com/shimarin/2358720
				if not _tone_fd:  # lazy init
					_tone_fd = os.open("/dev/console", os.O_WRONLY)
				# end if
				KIOCSOUND = 0x4B2F
				CLOCK_TICK_RATE = 1193180
				import fcntl
				if(freq != 0 ): # prevent division by 0
					fcntl.ioctl(_tone_fd, KIOCSOUND, int(CLOCK_TICK_RATE / freq))
				time.sleep(sec)
				# TODO: more accurate with nanosleep? https://stackoverflow.com/questions/1211806/python-high-precision-time-sleep
				fcntl.ioctl(_tone_fd, KIOCSOUND, 0) # turn the speaker off
			elif(INTERNAL_SPEAKER_USING_BEEP_CMD):
				# alternative using the beep command (slower)
				import subprocess
				subprocess.call(beepcmd, shell=True)
				return
			else:
				# new method using Linux evdev API https://gist.github.com/zed/9af4ebc7136348721677a35d7fd8cc84
				#traceback.print_exc(file=sys.stderr)
				if not _tone_fd:  # lazy init
					# works with every user in the "input" group
					_tone_fd = os.open("/dev/input/by-path/platform-pcspkr-event-spkr", os.O_WRONLY)
					import atexit
					atexit.register(tone, 0, 1)  # make sure the speaker is left turned off when finished
					atexit.register(os.close, _tone_fd)
				# end if
				EV_SND = 0x12  # linux/input-event-codes.h
				SND_TONE = 0x2  # ditto
				import ctypes
				time_t = suseconds_t = ctypes.c_long
				class Timeval(ctypes.Structure):
					_fields_ = [('tv_sec', time_t),	   # seconds
								('tv_usec', suseconds_t)] # microseconds
				class InputEvent(ctypes.Structure):
					_fields_ = [('time', Timeval),
								('type', ctypes.c_uint16),
								('code', ctypes.c_uint16),
								('value', ctypes.c_int32)]
				import math
				fsec, isec = math.modf(time.time())  # current time
				ev = InputEvent(time=Timeval(tv_sec=int(isec), tv_usec=int(fsec * 1000000)),
								type=EV_SND,
								code=SND_TONE,
								value=int(freq))
				os.write(_tone_fd, ev)  # start beep
				time.sleep(sec)
				ev.value = 0  # stop
				os.write(_tone_fd, ev)
				return
		except:
			pass
		else:
			# no exception
			return
# end of tone() function


def beep_cmd(args):
	if(len(args)==0):
		args="-f 450 -d 500"
	# else parse the cmdline args
	# TODO: use argparse
	freq = 0
	msec = 0
	repetitions = 1
	for a in args.split("-"):
		#print(a)
		if(a==''):
			continue
		elif(a.startswith('f')):
			freq = int(a.split(" ")[1])
		elif(a.startswith('d') or a.startswith('l')):
			msec = int(a.split(" ")[1])
		elif(a.startswith('r')):
			repetitions = int(a.split(" ")[1])
		elif(a.startswith('n')):
			for i in range(repetitions):
				tone(freq, msec)
			repetitions = 1
			freq = 0
			msec = 0
	if(freq!=0 and msec!=0):
		for i in range(repetitions):
			tone(freq, msec)
# end of beep_cmd


# main program
if __name__ == "__main__":
	import sys
	beep_cmd(' '.join(sys.argv[1:]))


