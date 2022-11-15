#!/usr/bin/env python3

from mic2speechrec import *
from say import *
import logging

def run_shell_command(cmd_str):
	logging.debug("executing " + cmd_str)
	import os, subprocess
	out = subprocess.call(cmd_str, shell=True)
	if ( out == 127 ):
		logging.error("command not found")
		return
		
		
# main program
if __name__ == "__main__":
	# TODO: accept audio files passed as args
	say("speak a command")
	
	command = stt() 
	
	if command == "":
		logging.error("no text recognized")
	# TODO: fuzzy command match
	
	run_shell_command(command)
