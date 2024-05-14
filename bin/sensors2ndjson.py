#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sys
import os
import sys
import psutil
import logging
import subprocess
import json
from time import sleep

# set the default log level to DEBUG (default to WARNING, will skip INFO and DEBUG messages)
logging.getLogger().setLevel(logging.DEBUG)

import socket
HOSTNAME = socket.gethostname()

from sensors import *


# main program
if __name__ == '__main__':

	try:
		while True:

			d = get_curr_sensors_dict()

			print(json.dumps(d))
			sys.stdout.flush()  # needed for correct piping
			
			sleep(3)

		# end of while
	except:
		import traceback
		traceback.print_exc(file=sys.stderr)


