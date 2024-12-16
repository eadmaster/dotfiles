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
import dbus
import json

# listen for media player status changes and outputs synched lyrics lines
#  .lrc files must match current filename path
# (meant to be piped to an external display)

# set the default log level to DEBUG (default to WARNING, will skip INFO and DEBUG messages)
logging.getLogger().setLevel(logging.DEBUG)


EXTRACT_ALBUM_ART=True
RESIZE_ALBUM_ART_WIDTH=121  # 0=does not resize
curr_album_art_base64_str = ""

def extract_album_art2base64(file_path):
	from mutagen.id3 import ID3, APIC
	from mutagen.mp3 import MP3
	from mutagen.flac import FLAC
	from mutagen.mp4 import MP4
	from mutagen.oggvorbis import OggVorbis
	from PIL import Image
	import io
	import os

	audio = None
	image_data = None

	if file_path.lower().endswith('.mp3'):
		audio = MP3(file_path, ID3=ID3)
		for tag in audio.tags.values():
			if isinstance(tag, APIC):
				image_data = tag.data
				break
	elif file_path.lower().endswith('.flac'):
		audio = FLAC(file_path)
		if audio.pictures:
			image_data = audio.pictures[0].data
	elif file_path.lower().endswith('.m4a') or file_path.lower().endswith('.mp4'):
		audio = MP4(file_path)
		if 'covr' in audio.tags:
			image_data = audio.tags['covr'][0]
	elif file_path.lower().endswith('.ogg') or file_path.lower().endswith('.oga'):
		audio = OggVorbis(file_path)
		if 'metadata_block_picture' in audio:
			image_data = audio['metadata_block_picture'][0]

	if image_data:
		image = Image.open(io.BytesIO(image_data))
		
		if RESIZE_ALBUM_ART_WIDTH :
			# Resize to the specified width while maintaining aspect ratio
			ratio = RESIZE_ALBUM_ART_WIDTH / float(image.size[0])
			height = int(image.size[1] * ratio)
			image = image.resize((RESIZE_ALBUM_ART_WIDTH, height), Image.LANCZOS)

		# Convert to 8-bit paletted mode
		image = image.convert('P', palette=Image.ADAPTIVE)
		
		# debug: save to file
		file_name = os.path.splitext(os.path.basename(file_path))[0] + '.bmp'
		output_path = os.path.join("/r", file_name)
		image.save(output_path, format='BMP')
		print(f'Album art saved to: {output_path}')
		
		# Save to a bytes buffer
		buffer = io.BytesIO()
		image.save(buffer, format='BMP')
		buffer.seek(0)

		# Encode to base64
		import base64
		global curr_album_art_base64_str
		curr_album_art_base64_str = base64.b64encode(buffer.read()).decode('utf-8')
		logging.debug("found album art")
		return
		
	else:
		logging.debug('No album art found in the file.')
		curr_album_art_base64_str = ""
# end of extract_album_art


lrc_control_str = ''

LYRICS_DISPLAY=True
LRC_SEARCH_PATH = os.path.expandvars(os.path.expanduser("$HOME/lyrics"))
LYRICS_TIME_OFFSET=0  # show the lyrics 1 second earlier (good for karaok)

JSON_OUTPUT_MODE=False

#lrc_current_unparsed = ''
lrc_file = None
last_time_update = "00:00"
curr_song_timer = None

def update_lyrics_line(full_lrc_line):
	global last_time_update
	last_time_update = full_lrc_line[1:6]
	global lrc_control_str
	lrc_line_escaped = (full_lrc_line.split("]")[-1])
	lrc_control_str = " " + lrc_line_escaped # MEMO: "-1" gets only the last part
	#lrc_control_str = "  " + colorize_lyrics_line(lrc_line_escaped) # MEMO: "-1" gets only the last part
	#print(lrc_control_str)
	schedule_next_lyrics_line()
	# output lrc_line
	lrc_line_escaped = lrc_line_escaped.replace("\n","")
	if JSON_OUTPUT_MODE:
		print(json.dumps({"player_status" : {"lyrics_line" : lrc_line_escaped}}))
	else:
		print(lrc_line_escaped)
	sys.stdout.flush()  # needed for correct piping
# end of update_lyrics_line

def schedule_next_lyrics_line():
	global lrc_control_str
	global last_time_update
	global curr_song_timer
	global lrc_file
	#logging.debug(lrc_file)
	#logging.debug(lrc_control_str)
	#logging.debug(last_time_update)
	#logging.debug(curr_song_timer)
	
	if(lrc_file==None):
		return
	# iterate over current lyrics file lines
	for line in lrc_file:
		if(len(line)<7):
			continue
		elif(not line.startswith('[')):
			continue
		elif(line.endswith(']')):
			# skip header lines
			continue
		# try to parse the time offset
		from datetime import datetime
		try:
			curr_line_time = datetime.strptime(line.split("]")[-2][0:6], '[%M:%S')  # TODO: better parse repeated time offsets like "[02:19.13][01:12.05][00:38.60]Come on baby, light my fire"
			# empty line test
			if(len(line.split("]")[1])==0):
				# skip empty lines
				# continue
				# keep empty lines, may be used with song sections with no vocals
				line += "  "
		except:
			# invalid line, skip to the next line
			continue
		# else the current line is valid
		# compute the timedelta
		prev_line_time = datetime.strptime(last_time_update, '%M:%S')
		time_delta = (curr_line_time - prev_line_time).total_seconds()
		if(time_delta<0):
			continue  # invalid curr_line_time
		time_delta += LYRICS_TIME_OFFSET
		if(time_delta<=0):
			time_delta = 0 # force at least 1 second
		# start a timer for the update
		# ALTERNATIVE: use "gobject.timeout_add(time_delta*1000, update_lyrics_line)"
		from threading import Timer
		curr_song_timer = Timer(time_delta, update_lyrics_line , [ line ] )
		curr_song_timer.start()
		#print("scheduled " + line + " in " + str(time_delta) + " seconds ")
		# MEMO: next line will be scheduled by update_lyrics_line
		return
	# end of for = end of file reached
	lrc_file.close()
	lrc_file = None
	lrc_control_str = " "
# end of schedule_next_lyrics_line

curr_state_str = "stopped"

def state_change_event_handler(curr_state):
	curr_state = str(curr_state)
	logging.debug("state_change_event_handler: " + curr_state)
	global lrc_control_str
	global last_time_update
	global curr_song_timer
	global curr_state_str
	curr_state_str=curr_state.lower()
	#logging.debug(last_time_update)
	if("stopped" in curr_state.lower()):
		# clear the lyrics
		lrc_control_str = ' '
		last_time_update = "00:00"
		global curr_song_timer
		if(curr_song_timer!=None):
			curr_song_timer.cancel()
			curr_song_timer=None
		if(lrc_file!=None):
			lrc_file.seek(0)  # rewind
		if JSON_OUTPUT_MODE:
			print(json.dumps({"player_status" : {"playback" : "stop"}}))
	elif("paused" in curr_state.lower()):
		#logging.debug("PAUSED_PLAYBACK")
		if(curr_song_timer!=None):
			curr_song_timer.cancel()
			curr_song_timer=None
		if JSON_OUTPUT_MODE:
			print(json.dumps({"player_status" : {"playback" : "pause"}}))
	elif("playing" in curr_state.lower()):
		# create a new timer
		schedule_next_lyrics_line()
# end of state_change_event_handler

def song_change_event_event_handler(title):
	title = str(title)
	logging.debug("song_change_event_event_handler: " + title)
	global lrc_control_str
	lrc_control_str = ""
	global lrc_file
	if(lrc_file!=None):
		lrc_file.close()
		lrc_file = None
	global curr_song_timer
	if(curr_song_timer!=None):
		curr_song_timer.cancel()
		curr_song_timer=None
	
	lrc_file_path = ""
	if title.startswith("file://"):
		# handle local lrc file
		lrc_file_path = title.replace("file://", "")
		import os, urllib.parse
		lrc_file_path = os.path.splitext(urllib.parse.unquote(lrc_file_path))[0] + ".lrc"
		#logging.debug(lrc_file_path)
	else:
		# look in the cache (for streaming media)
		global player_props
		metadata = player_props.Get("org.mpris.MediaPlayer2.Player", "Metadata", dbus_interface="org.freedesktop.DBus.Properties")
		title = metadata.get("xesam:title", "")
		if(title == ''):
			# title is required
			return
		artist = metadata.get("xesam:artist", [""])[0]
		#title = artist + " - " + title
		
		if(title.lower().endswith(".mp3")):
			# strip the extension
			title = title[:-4]
		# remove some chars in the title
		title = title.replace("  ", " - ")
		title = title.replace(",", "")
		
		# then look for the lrc file
		logging.debug("looking for lrc file: "  + title.lower()+'.lrc')
		import os
		lrc_file_path = ""
		for f in os.listdir(LRC_SEARCH_PATH):
			f_lower = f.lower()
			if (f_lower == title.lower()+'.lrc'):
				lrc_file_path = LRC_SEARCH_PATH + "/" + f
				break
			if (f_lower.endswith(" - " + title.lower()+'.lrc')):
				lrc_file_path = LRC_SEARCH_PATH + "/" + f
				break
		# try again with fnmatch
		title = title.split("(")[0].strip()  # strip parenthesis after the title 
		import fnmatch
		for f in os.listdir(LRC_SEARCH_PATH):
			f_lower = f.lower()
			if fnmatch.fnmatch(f_lower, '*'+title.lower()+'*.lrc'):
				lrc_file_path = LRC_SEARCH_PATH + "/" + f
				break
		if(lrc_file_path == ""):
			# no lrc file found 
			logging.debug("lyrics not found: " + title)
			return
	# else
	try:
		lrc_file = open(lrc_file_path, 'r')
		logging.debug("opened lrc file:" + lrc_file_path)
	except:
		logging.debug("lyrics not found: " + lrc_file_path)
	
	# display the title before the 1st lyrics line
	#lrc_control_str = title
	
	# read and extract album art from the file tags if present
	if title.startswith("file://"):
		# handle local lrc file
		title = title.replace("file://", "")
		import os, urllib.parse
		audio_file_path = urllib.parse.unquote(title)
		extract_album_art2base64(audio_file_path)
	return
# end of song_change_event_event_handler


# TODO: UPNP
UPNP_LISTENING=False  # WIP
UPNP_NET_INTERFACE="lo"  # network interface or IP to look for UPNP DLNA services (will detect current playing song from these)

# code derived from https://github.com/andyhelp/gupnp-python/blob/master/demo-events.py
curr_upnp_device = None
curr_upnp_services = []
curr_song_title = ""

def upnp_event_listening_thread():
         
    def upnp_event_cb( serviceProxy, variable, value, user_data ):
        #print "Event CB called from ", serviceProxy.get_url_base().get_host(), serviceProxy.get_service_type()
        #print "  serviceProxy=%s" %serviceProxy
        #print "  variable=%s" %variable
        #print "  value=%s" %value
        #print "  user_data=%s" %user_data
        #print "----"
        # parse the xml response
        import xml.etree.ElementTree as ET
        root = ET.fromstring(value)
        try:
            position_tag = root.find('.//{urn:schemas-upnp-org:metadata-1-0/AVT/}RelativeTimePosition')
            global last_time_update
            last_time_update = position_tag.attrib['val'][2:7]
            #DEBUG: print("position_tag found:" + str(last_time_update))
        except:
            pass
        try:
            metadata_tag = root.find('.//{urn:schemas-upnp-org:metadata-1-0/AVT/}CurrentTrackMetaData')
            # 2FIX: title extraction not working with Neutron player
            if(metadata_tag!=None):
                metadata_xml = metadata_tag.attrib['val']
                metadata_xml_root = ET.fromstring(metadata_xml)
                metadata_xml_title = metadata_xml_root.find('.//{http://purl.org/dc/elements/1.1/}title').text
                global curr_song_title
                if(metadata_xml_title != curr_song_title):
                    if(" - " in metadata_xml_title):  # quickfix for wrong titles passed by BubbleUpnp, you may want to disable this
                        song_change_event_event_handler(metadata_xml_title)
                        curr_song_title = metadata_xml_title
        except:
            pass
        try:
            state_tag = root.find('.//{urn:schemas-upnp-org:metadata-1-0/AVT/}TransportState')
            if(state_tag!=None):
                new_state = state_tag.attrib['val']
                state_change_event_handler(new_state)
                #DEBUG: print("state_tag found:" + str(new_state))
        except:
            pass
        # end of upnp_event_cb

    def device_available(cp, device):
        global curr_upnp_device, curr_upnp_services
        if(not (device.get_friendly_name()=="\"OrangePi\"" or device.get_friendly_name()=="OrangePi")):
            return
        curr_device = device
        for service in device.list_services():
            curr_upnp_services.append(service)
            print("Subscribing to ", service.get_url_base().get_host(), device.get_friendly_name(), service.get_service_type())
            service.add_notify("LastChange", str, upnp_event_cb, None)
            #service.add_notify("AbsoluteTimePosition", str, upnp_event_cb, None)
            #service.add_notify("RelativeTimePosition", str, upnp_event_cb, None)
            service.set_subscribed(True)

    def device_unavailable(cp, device):
        print("No DLna server found/connection lost?")
        #sys.exit(1)
        
    from gi.repository import GLib, GUPnP, GSSDP, GObject
    GObject.threads_init()
    ctx = GUPnP.Context(interface=UPNP_NET_INTERFACE)
    ctx.init(None)
    cp  = GUPnP.ControlPoint(client=ctx, target="upnp:rootdevice")
    cp.connect("device-proxy-available", device_available)
    cp.connect("device-proxy-unavailable", device_unavailable)
    GSSDP.ResourceBrowser.set_active(cp, True)
    GObject.MainLoop().run()
# end of upnp_event_listening_thread


# unused:
def mpris_media_player_status_dict():
    # single call
    try:
        session_bus = dbus.SessionBus()
        player_name = "vlc" # TODO: try more
        player_bus = session_bus.get_object(f'org.mpris.MediaPlayer2.{player_name}', '/org/mpris/MediaPlayer2')
        player_interface = dbus.Interface(player_bus, 'org.freedesktop.DBus.Properties')
        metadata = player_interface.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        import json
        metadata_json_str = json.dumps(metadata, indent=2)
        return json.loads(metadata_json_str)
    except dbus.exceptions.DBusException:
        print("not running")
        running = False
        sys.exit(1)

	
def dbus_event_listening_thread():
	import dbus
	import dbus.mainloop.glib
	from gi.repository import GLib

	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	
	# global vars
	session_bus = None
	main_loop = None
	player_props = None

	def print_song_metadata():
		global player_props
		metadata = player_props.Get("org.mpris.MediaPlayer2.Player", "Metadata", dbus_interface="org.freedesktop.DBus.Properties")
		title = metadata.get("xesam:title", "Unknown Title")
		artist = metadata.get("xesam:artist", ["Unknown Artist"])[0]
		album = metadata.get("xesam:album", "Unknown Album")
		global curr_song_title
		curr_song_title = title
		print("playing:", title, "by", artist, "from ", album)
	
	def seconds_to_lrc_time(seconds):
		from time import gmtime
		from time import strftime
		# NOTE: The following resets if it goes over 23:59:59!
		return strftime("%M:%S", gmtime(int(seconds)))
		# Result: '02:05'
	
	def on_status_changed(interface, changed, invalidated):
		if not interface == "org.mpris.MediaPlayer2.Player":
			return
		
		global player_props
		
		if "Metadata" in changed:
			logging.debug("changed metadata")
			metadata = player_props.Get("org.mpris.MediaPlayer2.Player", "Metadata", dbus_interface="org.freedesktop.DBus.Properties")
			#logging.debug(metadata)
			url = ""
			try:
				url = metadata['xesam:url']
			except:
				pass
			song_change_event_event_handler(url)
			print_song_metadata()
		if "PlaybackStatus" in changed:
			playback_status = player_props.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus", dbus_interface="org.freedesktop.DBus.Properties")
			#logging.debug("changed playback_status: " + playback_status)
			state_change_event_handler(playback_status)
		#if "Position" in changed:
		#	position = player_props.Get("org.mpris.MediaPlayer2.Player", "Position", dbus_interface="org.freedesktop.DBus.Properties")
		#	position_secs = position / 1000000  # Convert microseconds to seconds
		#	logging.debug("changed position: " + str(position_secs))
		#	global last_time_update
		#	last_time_update = seconds_to_lrc_time(position_secs)
	# end on_status_changed

	def on_seeked(time):
		position_secs  = time / 1000000
		logging.debug("Seeked to: " + str(position_secs))
		if JSON_OUTPUT_MODE:
			print(json.dumps({"player_status" : {"seek" : position_secs}}))
		global last_time_update
		last_time_update = seconds_to_lrc_time(position_secs)
		global curr_song_timer
		if curr_song_timer!=None:
			curr_song_timer.cancel()
			curr_song_timer=None
		global lrc_file
		if(lrc_file!=None):
			lrc_file.seek(0) # rewind (needed if seeking back)
		schedule_next_lyrics_line()
		#state_change_event_handler("paused")  # cancel current timer			
		#playback_status = player_props.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus", dbus_interface="org.freedesktop.DBus.Properties")
		#logging.debug("changed playback_status: " + playback_status)
		#state_change_event_handler(playback_status)
	
	def on_name_owner_changed(name, old_owner, new_owner):
		if not new_owner:  # Player closed
			logging.debug("Player closed or stopped.")
			state_change_event_handler("stopped")
			# reinit
			global main_loop
			main_loop.quit()
			global session_bus
			session_bus.close()
			sleep(5)
			wait_for_player_loop()
			#sys.exit(1)
			# TODO: sleep and wait for another player

	def find_media_players(session_bus):
		players = []
		for service in session_bus.list_names():
			# skip Chrome/Chromium and other browsers
			if "browser" in service.lower():
				continue
			if "chrom" in service.lower():
				continue
			if service.startswith("org.mpris.MediaPlayer2."):
				players.append(service)
		return players

	def wait_for_player_loop():
		global session_bus
		session_bus = dbus.SessionBus()
		players = None
		while not players:
			players = find_media_players(session_bus)
			#print("players:", players)
			
			if not players:
				logging.error("No MPRIS-compliant media players found.")
				# retry later
				sleep(5)
				continue
			# else
			
			player_name = players[0]  # get the 1st player found
			player_obj = session_bus.get_object(player_name, "/org/mpris/MediaPlayer2")
			global player_props
			player_props = dbus.Interface(player_obj, dbus_interface="org.freedesktop.DBus.Properties")
			player_iface = dbus.Interface(player_obj, dbus_interface="org.mpris.MediaPlayer2.Player")
			
			# init
			metadata = player_props.Get("org.mpris.MediaPlayer2.Player", "Metadata", dbus_interface="org.freedesktop.DBus.Properties")	
			print_song_metadata()
			#global last_time_update
			try:
				#print(metadata)
				url = metadata['xesam:url']
				print_song_metadata()
				song_change_event_event_handler(url)
				position = player_props.Get("org.mpris.MediaPlayer2.Player", "Position", dbus_interface="org.freedesktop.DBus.Properties")
				position_secs  = position / 1000000
				last_time_update = seconds_to_lrc_time(position_secs)
				playback_status = player_props.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus", dbus_interface="org.freedesktop.DBus.Properties")
				state_change_event_handler(playback_status)
			except:
				logging.exception("")
			
			player_props.connect_to_signal("PropertiesChanged", on_status_changed)
			player_iface.connect_to_signal("Seeked", on_seeked)
			
			global main_loop
			main_loop = GLib.MainLoop()
			session_bus.add_signal_receiver(on_name_owner_changed, signal_name="NameOwnerChanged", dbus_interface="org.freedesktop.DBus")

			main_loop.run()
	# end wait_for_player_loop
	
	wait_for_player_loop()
# end of dbus_event_listening_thread

	
# main program
if __name__ == '__main__':

	import threading
	if UPNP_LISTENING:
		# start the upnp events listening thread
		threading.Thread(target=upnp_event_listening_thread).start()
		
	else:
		# check local player via d-bus
		threading.Thread(target=dbus_event_listening_thread).start()


