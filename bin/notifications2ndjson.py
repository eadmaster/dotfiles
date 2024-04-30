#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import json


# register a system notifications listener
# and prints them on stdout as json


if(os.name=="nt"):
	# assuming Windows-like OS
	# TODO: monitor system notifications   https://stackoverflow.com/questions/35775912/how-can-i-use-python-2-7-to-read-windows-notifications
	#TODO: http://timgolden.me.uk/python/win32_how_do_i/track-session-events.html
	#TODO: http://timgolden.me.uk/python/win32_how_do_i/detect-device-insertion.html
	# from xprintidle import get_xprintidle_output
	# if ( get_xprintidle_output() >= IDLE_TIME_MILLIS ):
	#import requests
	#requests.post('https://api.pushjet.io/message', data={ 'message': "[" + HOSTNAME + "] " + text, 'level': 5, 'secret': '414bcab91c51a269746089f11596fd31' }).json()
	pass

else:
	# assuming Unix-like OS
	# dbus notifications listener, original code from http://askubuntu.com/questions/89279/listening-to-incoming-libnotify-notifications-using-dbus
	def handle_notification(bus, message):
		# TODO: parse as a dict
		m = message.get_args_list()
		if( len(m)<=1 ):
			return
			
		d = dict(
			sender = str(m[0]),
			icon = str(m[2]),
			title = str(m[3]),
			text = str(m[4])
		)
		
		print(json.dumps(d))
	# end of handle_notification
	

	def handle_notification2(proxy, *args, **kwargs):
		notification = args[0]
		print(json.dumps(notification))
		summary = notification.get('summary')
		body = notification.get('body')

		print(f"Summary: {summary}")
		print(f"Body: {body}")


	import dbus
	from dbus.mainloop.glib import DBusGMainLoop
	DBusGMainLoop(set_as_default=True)
	bus = dbus.SessionBus()
	bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
	bus.add_message_filter(handle_notification)
	
	# WIP: read as a dict
	#bus.add_signal_receiver(handle_notification2, dbus_interface="org.freedesktop.Notifications", signal_name="Notify")
	                    
	# main loop
	from gi.repository import GLib
	GLib.MainLoop().run()
# end of Unix-like event listener

