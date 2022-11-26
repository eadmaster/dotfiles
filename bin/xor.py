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

	import argparse, sys
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'), default=sys.stdin, help="input file, default to stdin if unspecified")
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('wb'), default=sys.stdout, help="output file, default to stdout if unspecified")
	#TODO: parser.add_argument("-d", "--decode", default=False, help="decode")
	args = parser.parse_args()

	if args.infile == sys.stdin:
		sys.stderr.write("reading from stdin...\n")
	
	message = args.infile.read()
		
	key = genkey(len(message))
	#sys.stderr.write('Generated random key:' + str(key) + "\n")

	cipherText = xor_strings(message, key)
	if args.outfile == sys.stdout:
		sys.stderr.write('cipherText:\n')
		print(cipherText)
	
	#print('decrypted:', xor_strings(cipherText, key))

	# Decode/Verify
	#if xor_strings(cipherText, key) == message:
	#	print('Unit test passed')
	#else:
	#	print('Unit test failed')
