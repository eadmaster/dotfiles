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

def get_net_io_counter():
	try:
		#older psutil versions: io_counter = (psutil.network_io_counters()[2] + psutil.network_io_counters()[3])  # packets_sent + packets_recv
		#newer psutil vesrions:
		io_counter = (psutil.net_io_counters()[2] + psutil.net_io_counters()[3])  # packets_sent + packets_recv
		return(io_counter)
	except:
		return(0)

import stat
#CURRENT_DEV_MAJOR, CURRENT_DEV_MINOR = divmod(os.stat()[stat.ST_DEV], 256)
#TODO: extract CURRENT_DEV = "/dev/sda1"  https://stackoverflow.com/questions/7718411/determine-device-of-filesystem-in-python
CURRENT_DEV = "/dev/sda1"

def get_disk_io_counter():
	io_counter = 0
	try:
		if HOSTNAME=='BOSS3':
			io_counter = psutil.disk_io_counters(perdisk=True)['mmcblk0'].read_bytes +  psutil.disk_io_counters(perdisk=True)['mmcblk0'].write_bytes   # you may want to change this!
			# disable this counter
			#io_counter = 0
		elif(os.name=="nt"):
			# on windows
			io_counter = psutil.disk_io_counters(perdisk=True)['PhysicalDrive1'].read_count +  psutil.disk_io_counters(perdisk=True)['PhysicalDrive1'].write_count   # you may want to change this!
		else:
			# assuming unix-like OS
			for d in psutil.disk_io_counters(perdisk=True).keys():
				# exclude the drive this script is stored
				if( d.startswith("sd") and d != CURRENT_DEV ):
					io_counter += psutil.disk_io_counters(perdisk=True)[d].read_count +  psutil.disk_io_counters(perdisk=True)[d].write_count   # you may want to change this!
			# end for
		# ALTERNATIVE: check all devices:
		#io_counter = psutil.disk_io_counters().read_count +  psutil.disk_io_counters().write_count   # you may want to change this!
		return(io_counter)
	except:
		logging.exception("")
		return(0)


def get_cputemp():
	# MEMO: psutil.sensors_temperatures is not available in older psutil versions
	try:
		if HOSTNAME=='BOSS3':
			return(int(1000 * psutil.sensors_temperatures()['sunxi-therm-1'][0].current))
			#memo: retrurns decimals like '0.028'
		elif(os.name=="nt"):
			# use wmi+openhardwaremonitor on windows (psutil not supported)  http://stackoverflow.com/questions/3262603/accessing-cpu-temperature-in-python
			import wmi
			#w = wmi.WMI()
			#if(len(w.Win32_TemperatureProbe())!=0):
			#	return(w.Win32_TemperatureProbe()[0].CurrentReading)
			w = wmi.WMI(namespace="root\OpenHardwareMonitor")
			sensors = w.Sensor()
			for sensor in sensors:
				# filter the cpu temperature sensor
				if(sensor.SensorType==u'Temperature' and sensor.Name.startswith("CPU")):
					return(int(sensor.Value))
			# no temperature sensor found
			return(0)
		else:
			# using psutil on unix-like OSes
			return(int(psutil.sensors_temperatures()['acpitz'][0].current))
			#memo: retrurns integers like '28'
	except:
		return(0)


old_disk_io_counter = get_disk_io_counter()
old_net_io_counter = get_net_io_counter()

def get_curr_sensors_dict():

	d = {}
	
	global old_disk_io_counter
	global old_net_io_counter
	

	#cpufreq = int(psutil.cpu_freq().current)
	
	#cpu_usage = psutil.cpu_percent()
	#ALTERNATIVE: max single-core usage instead of overall
	d['cpu_usage_percent'] = int(max(psutil.cpu_percent(percpu=True)))
	
	#if( is_cpu_throttling() ):
	#	say("CPU throttling ")
	
	disk_io_counter = get_disk_io_counter()
	disk_io_counter_diff = disk_io_counter - old_disk_io_counter
	d['disk_io_counter'] = disk_io_counter_diff
	old_disk_io_counter = disk_io_counter
	
	net_io_counter = get_net_io_counter()
	net_io_counter_diff = net_io_counter - old_net_io_counter
	d['net_io_counter'] = net_io_counter_diff
	old_net_io_counter = net_io_counter

	d['mem_usage_percent'] = int(psutil.virtual_memory().percent)
	
	# TODO: add another alarm for paging file increasing (if present)
	#if(psutil.swap_memory().total != 0)...
	
	d['cpu_temp_deg'] = get_cputemp()
	
	return d


# main program
if __name__ == '__main__':

	try:

		d = get_curr_sensors_dict()
		
		# print one value per line
		for k in d:
			print(k + ": " + str(d[k]))
			
	except:
		import traceback
		traceback.print_exc(file=sys.stderr)


