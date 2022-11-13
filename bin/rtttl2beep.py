#!/usr/bin/env python


# beep and tone functions
try:
	from beep import tone
except:
	def tone(freq, msec):
		beepcmd = "beep -f " + str(freq) + " -d " + str(msec)
		print(beepcmd)  # output the corresponding beep command
		import subprocess
		subprocess.call(beepcmd, shell=True)
		return


# Nokia RTTTL parser class
# original code from https://github.com/dhylands/upy-rtttl
NOTE = [
	440.0,	# A
	493.9,	# B or H
	261.6,	# C
	293.7,	# D
	329.6,	# E
	349.2,  # F
	392.0,	# G
	0.0,	# pad

	466.2,	# A#
	0.0,
	277.2,	# C#
	311.1,	# D#
	0.0,
	370.0,	# F#
	415.3,	# G#
	0.0,
]

class RTTTL:
	def __init__(self, tune):
		tune_pieces = tune.split(':')
		if len(tune_pieces) != 3:
			raise ValueError('tune should contain exactly 2 colons')
		self.tune = tune_pieces[2]
		self.tune_idx = 0
		self.parse_defaults(tune_pieces[1])

	def parse_defaults(self, defaults):
		# Example: d=4,o=5,b=140
		val = 0
		id = ' '
		for char in defaults:
			char = char.lower()
			if char.isdigit():
				val *= 10
				val += ord(char) - ord('0')
				if id == 'o':
					self.default_octave = val
				elif id == 'd':
					self.default_duration = val
				elif id == 'b':
					self.bpm = val
			elif char.isalpha():
				id = char
				val = 0
		# 240000 = 60 sec/min * 4 beats/whole-note * 1000 msec/sec
		self.msec_per_whole_note = 240000.0 / self.bpm

	def next_char(self):
		if self.tune_idx < len(self.tune):
			char = self.tune[self.tune_idx]
			self.tune_idx += 1
			if char == ',':
				char = ' '
			return char
		return '|'

	def notes(self):
		"""Generator which generates notes. Each note is a tuple where the
		   first element is the frequency (in Hz) and the second element is
		   the duration (in milliseconds).
		"""
		while True:
			# Skip blank characters and commas
			char = self.next_char()
			while char == ' ':
				char = self.next_char()

			# Parse duration, if present. A duration of 1 means a whole note.
			# A duration of 8 means 1/8 note.
			duration = 0
			while char.isdigit():
				duration *= 10
				duration += ord(char) - ord('0')
				char = self.next_char()
			if duration == 0:
				duration = self.default_duration

			if char == '|': # marker for end of tune
				return

			note = char.lower()
			if note >= 'a' and note <= 'g':
				note_idx = ord(note) - ord('a')
			elif note == 'h':
				note_idx = 1	# H is equivalent to B
			else:
				note_idx = 7	# pause
			char = self.next_char()

			# Check for sharp note
			if char == '#':
				note_idx += 8
				char = self.next_char()

			# Check for duration modifier before octave
			# The spec has the dot after the octave, but some places do it
			# the other way around.
			duration_multiplier = 1.0
			if char == '.':
				duration_multiplier = 1.5
				char = self.next_char()

			# Check for octave
			if char >= '4' and char <= '7':
				octave = ord(char) - ord('0')
				char = self.next_char()
			else:
				octave = self.default_octave

			# Check for duration modifier after octave
			if char == '.':
				duration_multiplier = 1.5
				char = self.next_char()

			freq = NOTE[note_idx] * (1 << (octave - 4))
			msec = (self.msec_per_whole_note / duration) * duration_multiplier

			#print('note ', note, 'duration', duration, 'octave', octave, 'freq', freq, 'msec', msec)

			yield freq, msec
# end of Nokia RTTTL parser class


# main program
if __name__ == "__main__":
	import sys
	import os
	PROGRAM_NAME = os.path.basename(sys.argv[0])

	# parse the args
	if(len(sys.argv)>=2):
		if(sys.argv[1]=='-h' or sys.argv[1]=='--help'):  # 
			print("usage: " + PROGRAM_NAME + " [RTTTL string|rtttl.txt]")
			exit(0)

	if(len(sys.argv)==1):
		# read from stdin
		songdata = sys.stdin.readline()
	elif( os.path.isfile(sys.argv[1]) ):
		with open(sys.argv[1]) as f:
			songdata = f.read()
	else:
		songdata = sys.argv[1]

	# play the song
	tune = RTTTL(songdata)
	for freq, msec in tune.notes():
		tone(freq, msec)

	# MEMO: clean exit done by exit handlers registered previously with atexit
