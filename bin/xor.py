#!/usr/bin/python
# -*- coding: utf-8 -*-

# derived from https://en.wikipedia.org/wiki/XOR_cipher

def genkey(length: int) -> bytes:
    """Generate key."""
    from os import urandom
    return urandom(length)


def xor_strings(s, t) -> bytes:
    """Concate xor two strings together."""
    if isinstance(s, str):
        # Text strings contain single characters
        return "".join(chr(ord(a) ^ b) for a, b in zip(s, t)).encode('utf8')
    else:
        # Bytes objects contain integer values in the range 0-255
        return bytes([a ^ b for a, b in zip(s, t)])


# main program
if __name__ == "__main__":
	# TODO: add decrypt mode via "-d" switch
	
	import sys
	
	if len(sys.argv) > 1:
		message = open(sys.argv[1], "rb").read()
	else:
		sys.stderr.write("reading msg to encrypt from stdin...\n")
		message = sys.stdin.read()
		
	key = genkey(len(message))
	sys.stderr.write('Generated random key:' + str(key) + "\n")

	cipherText = xor_strings(message, key)
	sys.stderr.write('cipherText:\n')
	print(cipherText)
	
	#print('decrypted:', xor_strings(cipherText, key))

	# Verify
	#if xor_strings(cipherText, key) == message:
	#	print('Unit test passed')
	#else:
	#	print('Unit test failed')
