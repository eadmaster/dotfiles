#!/usr/bin/python
# -*- coding: utf-8 -*-

# listen for media player status changes and outputs jsons on the console
# (meant to be piped and read)

# TODO: add windows support via SystemMediaTransportControls (SMTC) https://stackoverflow.com/questions/65011660/how-can-i-get-the-title-of-the-currently-playing-media-in-windows-10-with-python
# https://www.autohotkey.com/boards/viewtopic.php?t=102100

# TODO: rewrite as reusable code -> import in mediaplayerstatus2lrc.py

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

# set the default log level to DEBUG (default to WARNING, will skip INFO and DEBUG messages)
logging.getLogger().setLevel(logging.DEBUG)

UPNP_LISTENING=False
UPNP_NET_INTERFACE="lo"  # network interface or IP to look for UPNP DLNA services (will detect current playing song from these)

# code derived from https://github.com/andyhelp/gupnp-python/blob/master/demo-events.py
curr_upnp_device = None
curr_upnp_services = []
curr_song_title = ""

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

def upnp_event_listening_thread():
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



# main program
if __name__ == '__main__':

    if UPNP_LISTENING:
        # start the upnp events listening thread
        import threading
        upnp_event_listener = threading.Thread(target=upnp_event_listening_thread).start()
    else:
        # https://stackoverflow.com/questions/3919735/how-to-continuously-monitor-rhythmbox-for-track-change-using-python
                
        import dbus
        import dbus.mainloop.glib
        from gi.repository import GLib

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        session_bus = dbus.SessionBus()
        
        def find_media_players(session_bus):
            players = []
            for service in session_bus.list_names():
                if service.startswith("org.mpris.MediaPlayer2."):
                    players.append(service)
            return players

        players = find_media_players(session_bus)
        if not players:
            print("No MPRIS-compliant media players found.")
            exit()
            
        player_name = players[0]
        player_obj = session_bus.get_object(player_name, "/org/mpris/MediaPlayer2")
        player_props = dbus.Interface(player_obj, dbus_interface="org.freedesktop.DBus.Properties")
        player_iface = dbus.Interface(player_obj, dbus_interface="org.mpris.MediaPlayer2.Player")
        
        def print_all_properties():
            all_properties = player_props.GetAll("org.mpris.MediaPlayer2.Player", dbus_interface="org.freedesktop.DBus.Properties")
            print(json.dumps(all_properties))
            #for key, value in all_properties.items():
            #    print(key, ":", value)
            
        
        # 1st print
        print_all_properties()

        def on_status_changed(interface, changed, invalidated):
            if not interface == "org.mpris.MediaPlayer2.Player":
                return
            if "Metadata" in changed or "PlaybackStatus" in changed or "Position" in changed:
                print_all_properties()
            
            if "Metadata" in changed:
                logging.debug("changed metadata")
            if "PlaybackStatus" in changed:
                playback_status = player_props.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus", dbus_interface="org.freedesktop.DBus.Properties")
                logging.debug("changed playback_status: " + playback_status)
            if "Position" in changed:
                position = player_props.Get("org.mpris.MediaPlayer2.Player", "Position", dbus_interface="org.freedesktop.DBus.Properties")
                position_secs = position / 1000000  # Convert microseconds to seconds
                logging.debug("changed position: " + str(position_secs))
        # end on_status_changed

        def on_seeked(time):
            logging.debug("Seeked to:" + str(time / 1000000) + " s")  # Convert microseconds to seconds
            print_all_properties()

        player_props.connect_to_signal("PropertiesChanged", on_status_changed)
        player_iface.connect_to_signal("Seeked", on_seeked)

        main_loop = GLib.MainLoop()
        main_loop.run()

