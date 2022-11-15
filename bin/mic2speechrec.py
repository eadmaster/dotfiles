#!/usr/bin/env python3

import os
import logging

def recognize_via_speech_recognition():
	text = ""
	
	# derived from https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
	# NOTE: this example requires PyAudio because it uses the Microphone class
	import speech_recognition as sr
	r = sr.Recognizer()
	# obtain audio from the microphone
	with sr.Microphone() as source:
		# mic calibration  https://www.codesofinterest.com/2017/03/python-speech-recognition-pocketsphinx.html
		print("Please wait. Calibrating microphone for 2s...")  
		# listen for 5 seconds and create the ambient noise energy level  
		r.adjust_for_ambient_noise(source, duration=2)  
		print("Say something!")
		audio = r.listen(source, timeout=5)
		print("Stop talking")

	# TODO: Coqui https://stt.readthedocs.io/en/latest/Python-Examples.html

	# recognize speech using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		logging.info("using Google Speech Recognition")
		text = r.recognize_google(audio)
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))

	# recognize speech using Google Cloud Speech
	GOOGLE_CLOUD_SPEECH_CREDENTIALS = os.getenv("GOOGLE_CLOUD_SPEECH_CREDENTIALS", "") # INSERT THE CONTENTS OF THE GOOGLE CLOUD SPEECH JSON CREDENTIALS FILE HERE
	if GOOGLE_CLOUD_SPEECH_CREDENTIALS:
		try:
			logging.info("using Google Cloud Speech")
			text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
		except sr.UnknownValueError:
			print("Google Cloud Speech could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Cloud Speech service; {0}".format(e))

	# recognize speech using Wit.ai
	WIT_AI_KEY = os.getenv("WIT_AI_KEY", "") # Wit.ai keys are 32-character uppercase alphanumeric strings
	if WIT_AI_KEY:
		try:
			logging.info("using Wit.ai")
			text = r.recognize_wit(audio, key=WIT_AI_KEY)
		except sr.UnknownValueError:
			print("Wit.ai could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Wit.ai service; {0}".format(e))

	# recognize speech using Microsoft Bing Voice Recognition
	BING_KEY = os.getenv("BING_KEY", "")  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
	if BING_KEY:
		try:
			logging.info("using Microsoft Bing Voice Recognition")
			text = r.recognize_bing(audio, key=BING_KEY)
		except sr.UnknownValueError:
			print("Microsoft Bing Voice Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

	# recognize speech using Microsoft Azure Speech
	AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")  # Microsoft Speech API keys 32-character lowercase hexadecimal strings
	if AZURE_SPEECH_KEY:
		try:
			logging.info("using Microsoft Azure Speech")
			text = r.recognize_azure(audio, key=AZURE_SPEECH_KEY)
		except sr.UnknownValueError:
			print("Microsoft Azure Speech could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Microsoft Azure Speech service; {0}".format(e))

	# recognize speech using Houndify
	HOUNDIFY_CLIENT_ID = os.getenv("HOUNDIFY_CLIENT_ID", "")  # Houndify client IDs are Base64-encoded strings
	HOUNDIFY_CLIENT_KEY = os.getenv("HOUNDIFY_CLIENT_KEY", "")  # Houndify client keys are Base64-encoded strings
	if HOUNDIFY_CLIENT_ID and HOUNDIFY_CLIENT_KEY:
		try:
			logging.info("using Houndify")
			text = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
		except sr.UnknownValueError:
			print("Houndify could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Houndify service; {0}".format(e))

	# recognize speech using IBM Speech to Text
	IBM_USERNAME = os.getenv("IBM_USERNAME", "")  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
	IBM_PASSWORD = os.getenv("IBM_PASSWORD", "")  # IBM Speech to Text passwords are mixed-case alphanumeric strings
	if IBM_USERNAME and IBM_PASSWORD:
		try:
			logging.info("using IBM Speech to Text")
			text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
		except sr.UnknownValueError:
			print("IBM Speech to Text could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from IBM Speech to Text service; {0}".format(e))
		
	# recognize speech using Sphinx
	try:
		logging.info("using Sphinx (local)")
		text = r.recognize_sphinx(audio)
	except sr.UnknownValueError:
		print("Sphinx could not understand audio")
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e))
	
	return(text)
# end of recognize_via_speech_recognition


def stt():
	try:
		return recognize_via_speech_recognition()
	except:
		return ""
	
	#TODO: using Plyer (apt install python3-plyer) https://github.com/kivy/plyer/
	# https://github.com/kivy/plyer/blob/master/examples/speech2text/main.py
	
	#TODO: using Conqui (maintained DeepSpeech fork, python api) https://github.com/coqui-ai/stt
	
	
# main program
if __name__ == "__main__":
	# TODO: accept audio files passed as args
	output_str = stt()
	print(output_str)