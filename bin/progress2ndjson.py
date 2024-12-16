#! /usr/bin/env python3
# -*- coding: utf-8 -*-


# TODO: add android, gnome, windows support

# integrate with:
#  chrome  -> https://userbase.kde.org/Plasma-browser-integration
#  cmdline  -> https://github.com/Xfennec/progress

import json
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import sys

#print("Monitoring progress changes in the KDE taskbar...")
#sys.stdout.flush()  # needed for correct piping


def print_progress_bar(progress_percent, bar_length=40):
	#bar_length -= 4
	progress = progress_percent / 100
	block = int(round(bar_length * progress))
	progress_bar = "#" * block + "-" * (bar_length - block)
	#print("[", progress_bar, "]")
	print(progress_bar)
	#print(f"\rProgress: [{progress_bar}] {progress_percent:.2f}%", end='')

 
def handle_progress_change(bus, message, json_output=True):
	args = message.get_args_list()
	method = message.get_member()
	path = message.get_path()
	interface = message.get_interface()
	
	if len(args) <= 1:
	    return

	if str(method) == "Update":
		job_id = args[0]  # "application://org.kde.dolphin"
		application_name = job_id.replace("application://", "")
		job_info = args[1]
		progress = float(job_info.get('progress', 0.0))
		progress_percent = int(progress * 100)
		if progress_percent == 0:
			# cancelled
			return
		
		d = {
			"application" : application_name,
			"progress_percent" : progress_percent
		}
		#print(job_info)
		#print(method, args, path, interface)
		#print(args)
		
	#TODO: if str(method) == "setPercent":
	#else:
	#	print(method, args, path, interface)
		
	if json_output:
		print(json.dumps(d))
	else:
		# console pretty print
		print(d["application"], ": ", d["progress_percent"], "%")
		print_progress_bar(d["progress_percent"])
	sys.stdout.flush()  # needed for correct piping
# end of handle_progress_change

def main():
    # Initialize the D-Bus main loop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    loop = GLib.MainLoop()

    # Connect to the session bus
    session_bus = dbus.SessionBus()

    # Add a signal receiver for progress changes
    # https://stackoverflow.com/questions/23458215/how-to-create-kde-tray-notification-in-a-c-program
    #session_bus.add_match_string_non_blocking("type='signal',interface='org.kde.JobViewServer'") # ,member='setPercent'
    # https://gist.github.com/srithon/3cd297bdfdd157c0a7e00ff1aeb2690c
    # dbus-monitor
    session_bus.add_match_string_non_blocking("type='signal',path='/org/kde/notificationmanager/jobs'") # ,interface='com.canonical.Unity.LauncherEntry',member='Update'"
    # type='signal',path='/org/kde/notificationmanager/jobs',interface='org.kde.JobViewV2',member='setPercent'"
    session_bus.add_message_filter(handle_progress_change)

    try:
        loop.run()
    except KeyboardInterrupt:
        #print("Exiting...")
        pass

if __name__ == "__main__":
    main()
