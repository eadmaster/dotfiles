#!/usr/bin/python2
# -*- coding: utf-8 -*-

import ctypes
import os

if(os.name=="nt"):
	# assuming Windows-like OS
	# solution from  https://stackoverflow.com/questions/911856/detecting-idle-time-using-python
	from ctypes import Structure, windll, c_uint, sizeof, byref

	class LASTINPUTINFO(Structure):
		_fields_ = [
		 ('cbSize', c_uint),
		 ('dwTime', c_uint),
		]

	def get_xprintidle_output():
		lastInputInfo = LASTINPUTINFO()
		lastInputInfo.cbSize = sizeof(lastInputInfo)
		windll.user32.GetLastInputInfo(byref(lastInputInfo))
		millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
		return millis
else:
	# assuming Unix-like OS
	# solution from  https://stackoverflow.com/questions/5914506/in-python-on-unix-determine-if-i-am-using-my-computer-or-idle
	class XScreenSaverInfo( ctypes.Structure):
	  """ typedef struct { ... } XScreenSaverInfo; """
	  _fields_ = [('window',	  ctypes.c_ulong), # screen saver window
			('state',	ctypes.c_int),   # off,on,disabled
			('kind',	 ctypes.c_int),   # blanked,internal,external
			('since',	ctypes.c_ulong), # milliseconds
			('idle',	 ctypes.c_ulong), # milliseconds
			('event_mask',  ctypes.c_ulong)] # events

	def get_xprintidle_output():
		xlib = ctypes.cdll.LoadLibrary('libX11.so')
		display = xlib.XOpenDisplay(os.environ['DISPLAY'])
		xss = ctypes.cdll.LoadLibrary('libXss.so.1')
		xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
		xssinfo = xss.XScreenSaverAllocInfo()
		xss.XScreenSaverQueryInfo(display, xlib.XDefaultRootWindow(display), xssinfo)
		idletime = xssinfo.contents.idle
		
		# Cleaning Up
		xss.XFree(xssinfo)
		xss.XCloseDisplay(display)

		#return("%d" % xssinfo.contents.idle)
		return(idletime)


if __name__ == "__main__":
	 print(get_xprintidle_output())
