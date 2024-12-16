#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging

PROGRAM_NAME = os.path.basename(sys.argv[0])

# TODO: https://developer-old.gnome.org/libsecret/unstable/py-lookup-example.html
def get_password_via_dbus(name):
	from gi.repository import Secret
	EXAMPLE_SCHEMA = Secret.Schema.new("org.freedesktop.secrets",
		Secret.SchemaFlags.NONE,
		{
			"string": Secret.SchemaAttributeType.STRING,
			"variant": Secret.SchemaAttributeType.STRING
		}
	)
	password = Secret.password_lookup_sync(EXAMPLE_SCHEMA, { "number": "8", "even": "true" }, None)
	return(password)


def get_password_via_keyring(service, key):
	# https://github.com/jaraco/keyring
	import keyring
	from keyring.backends import kwallet
	keyring.set_keyring(kwallet.DBusKeyring())
	p = keyring.get_password(service, key)
	return p

	
if __name__ == "__main__":
	if(len(sys.argv) <= 1 or sys.argv[1] in ['-h', '--help']):
		print("usage: " + PROGRAM_NAME + " KEYNAME SERVICENAME")
		sys.exit(1)
	
	key = sys.argv[1]
	service = "Scripts"
	
	print(get_password_via_keyring(service, key))
	#print(get_password_from_dbus...)
