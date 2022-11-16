#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

# set the default log level to DEBUG (default to WARNING, will skip INFO and DEBUG messages)
#logging.getLogger().setLevel(logging.DEBUG)

def say(message):
	# using Speech Dispatcher (apt install python3-speechd) https://github.com/brailcom/speechd/blob/master/doc/speech-dispatcher.html#Python-API
	try:
		import speechd
		client = speechd.SSIPClient('test')
		#client.set_output_module('festival')
		client.set_output_module('pico-generic')
		#client.set_language('en-US')
		client.set_punctuation(speechd.PunctuationMode.SOME)
		logging.debug("using speechd + pico-generic")
		client.speak(message)
		client.close()
		return
	except:
		pass

	# using Plyer (apt install python3-plyer) https://github.com/kivy/plyer/
	try:
		from plyer import tts
		tts.speak(self.ids.notification_text.text)
		return
	except:
		pass

	# using pyttsx3 (only espeak on linux) https://github.com/nateshmbhat/pyttsx3
	try:
		import pyttsx3
		engine = pyttsx3.init()
		logging.debug("using pyttsx3")
		engine.say(message)
		engine.runAndWait()
		return
	except:
		pass

	# Windows-only alternative using SAPI
	import os
	if(os.name=="nt"):
		try:
			import win32com.client
			speaker = win32com.client.Dispatch("SAPI.SpVoice")
			logging.debug("using Windows SAPI")
			speaker.Speak(message)
			return
		except:
			pass
	
	# TODO: google translate service
	
	# WANTED: pure python single file tts :
	#  NO? http://microbit-micropython.readthedocs.io/en/latest/speech.html
	
	# else try with some shell commands
	import os, subprocess
	out = subprocess.call("say \'" + message + "\'", shell=True)  # MEMO: available on MacOSX
	if ( out == 0 ):
		logging.debug("using say shell command")
		return
	
	out = subprocess.call("flite -voice slt -t \'" + message + "\'", shell=True)
	if ( out == 0 ):
		logging.debug("using flite shell command")
		return
	
	out = subprocess.call("espeak -v f3 \'" + message + "\'", shell=True)
	return
# end of say function


# main program
if __name__ == "__main__":
	
	import sys
	if len(sys.argv) > 1:
		msg = ' '.join(sys.argv[1:])
	else:
		msg = sys.stdin.read()
	# TODO: add more switches via argparse + clone https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man1/say.1.html
	
	say(msg)

