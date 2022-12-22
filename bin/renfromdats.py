#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: eadmaster
#   derived from generate_mame_playlist_for_retroarch by possatti https://gist.github.com/possatti/b4cf5ee36d5cc1970d147c48167e415f

from __future__ import print_function, division

import xml.etree.ElementTree as ET
import argparse
import sys
import logging
import os

KNOWN_ROM_EXTENSION_LIST = [ "nes", "sms", "smd", "gen", "smd", "md", "gg", "gb", "gbc", "gba","sfc" ]  # the files with these extensions will be skipped


def get_file_crc32(full_filepath):
	import binascii
	f = open(full_filepath,'rb')
	buf = f.read()
	f.close()
	hashval = (binascii.crc32(buf) & 0xFFFFFFFF)
	return ("%08X" % hashval)
	

def get_crc32_from_datfile(src_dat_ext, src_dat_root, src_dat_lines, rom_name, partial_matches):
	# look for a rom_name in the datfile
	src_rom_crc = "" # returned value
	if(src_dat_ext == ".xml"):
		# search in the xml datfile
		game_node = src_dat_root.find(".//game[@name=\"{}\"]".format(rom_name))
		if not game_node:
			if not "[!]" in rom_name:
				# try again after adding the "[!]"
				game_node = src_dat_root.find(".//game[@name=\"{}\"]".format(rom_name +" [!]"))					
			else:
				# try again after removing the "[!]"
				game_node = src_dat_root.find(".//game[@name=\"{}\"]".format(rom_name.replace(" [!]", "")))
			if ", The" in rom_name:
				# try again after removing the ", The"
				game_node = src_dat_root.find(".//game[@name=\"{}\"]".format(rom_name.replace(", The", "")))
			if not game_node:
				logging.error("nothing found for \"" + rom_name + "\" in the source datfile (file skipped)")
				return ""
		# else a match is found
		# Get game info from the dat
		src_rom_name = game_node.find('description').text
		src_rom_crc = game_node.find('rom').attrib['crc']
		#src_rom_md5 = game_node.find('rom').md5   # not always present
		#src_rom_sha1 = game_node.find('rom').sha1   # not always present
	else:
		# search a matching line
		for line in src_dat_lines:
			if line.startswith(( rom_name+".", rom_name + " [!].", rom_name.replace(" [!]", "")+".")):
				src_rom_name = rom_name
				src_rom_crc = line.split()[-1]
			elif line.startswith(( "¬"+rom_name+"¬", "¬"+rom_name+ " [!]¬", "¬"+rom_name.replace(" [!]", "")+"¬")):
				src_rom_name = rom_name
				src_rom_crc = line.split("¬")[-5]
		# end for
	# end if
	if not src_rom_crc and partial_matches and ")" in rom_name:
		# try again with a shorter rom_name
		rom_name = rom_name.split(")")[0]  # will look for "rom_name (R"
		# search a matching partial line
		#NO? return get_crc32_from_datfile(src_dat_ext, src_dat_root, src_dat_lines, rom_name, partial_matches=False)  # NOTE: partial_matches is turned false here
		for line in src_dat_lines:
			if line.startswith(rom_name):
				src_rom_name = rom_name
				src_rom_crc = line.split()[-1]
			elif line.startswith("¬"+rom_name):
				src_rom_name = rom_name
				src_rom_crc = line.split("¬")[-5]
		# end for
	#else
	return src_rom_crc
# end of get_crc32_from_datfile


def get_rom_name_from_crc32(dst_dat_ext, dst_dat_lines, dst_dat_root, src_rom_crc, extension):
	dst_rom_name = ""
	if dst_dat_ext == ".xml":
		# search in the xml datfile
		game_node = dst_dat_root.find(".//rom[@crc='{}']...".format(src_rom_crc.upper()))  # MEMO: "..." returns the parent node
		if(game_node is None):
			# try again with lowercase crc
			game_node = dst_dat_root.find(".//rom[@crc='{}']...".format(src_rom_crc.lower()))
		if(game_node is not None):
			# a match was found
			dst_rom_name = game_node.find('description').text + extension
			#dst_rom_name = game_node.attrib['name'] + extension  # same value?
	else:
		# search a matching line
		for line in dst_dat_lines:
			if line.strip().endswith(src_rom_crc.upper()):
				dst_rom_name = " ".join(line.split()[0:-1])
			elif "¬"+src_rom_crc.upper()+"¬" in line:
				dst_rom_name = line.split("¬")[1]
		# end for
	# end if
	return dst_rom_name
# end of get_rom_name_from_crc32

	
def parse_args():
	# Arguments and options.
	parser = argparse.ArgumentParser(description='Use 2 DAT files to scan a ROM folder and rename files.')
	parser.add_argument('src_dat', help="source datfile used to identify support files. Also support SFV files.")
	parser.add_argument('dst_dat', help="destination datfile used to rename files")
	parser.add_argument('romdir', default=".", nargs='*', help="dir with the files to check (defaults to .)")
	parser.add_argument('-r', '--rename', default=False, action="store_true", help='actually rename the matching entries, otherwise will only print a script on stdout (dry-mode as default)')
	parser.add_argument('--include-roms', default=False, action="store_true", help='include ROMs alongside support files. They will only be checked against the destination dafile.')
	parser.add_argument('--partial-matches', default=False, action="store_true", help='allows partial matches with support filenames (risky for batch/unsupervised mode).')
	parser.add_argument('--recurse', default=False, action="store_true", help='recurse subdirs.')
	#parser.add_argument('--skip-big-files', default="50", help='avoid checking big files')
	args = parser.parse_args()

	# # Verify paths exist.
	# Verify paths exist.
	if not os.path.isfile(args.src_dat):
		raise IOError('Could not find `.dat` on `{}`, file does not exist.'.format(args.src_dat))
	if not os.path.isfile(args.dst_dat):
		raise IOError('Could not find `.dat` on `{}`, file does not exist.'.format(args.dst_dat))
	if not os.path.isdir(args.romdir[0]):
		raise IOError('Could not find ROM\'s directory on `{}`, directory does not exist.'.format(args.romdir))
	return args


def main():
	args = parse_args()
	
	# parse source datfile
	src_dat_root = None
	src_dat_lines = None
	src_dat_ext = os.path.splitext(args.src_dat)[-1]
	if(src_dat_ext == ".dat"):
		# check if xml
		src_dat_header = open(args.src_dat, 'r').read(10)
		if src_dat_header.startswith("<?xml version"):
			src_dat_ext = ".xml"
	if(src_dat_ext == ".xml"):
		# assume a listxml datfile
		src_dat_tree = ET.parse(args.src_dat)
		src_dat_root = src_dat_tree.getroot()
	#elif(src_dat_ext in ["zip", "gz" ]):
	#	# TODO: decompress on the fly
	else:
		# just fully read the file in memory
		src_dat_lines = open(args.src_dat, encoding='latin_1').readlines()
	
	# parse destination datfile
	dst_dat_root = None
	dst_dat_lines = None
	dst_dat_ext = os.path.splitext(args.dst_dat)[-1]
	if(dst_dat_ext == ".dat"):
		# check if xml
		dst_dat_header = open(args.dst_dat, 'r').read(16)
		if dst_dat_header.startswith("<?xml version"):
			dst_dat_ext = ".xml"
	if(dst_dat_ext == ".xml"):
		dst_dat_tree = ET.parse(args.dst_dat)
		dst_dat_root = dst_dat_tree.getroot()
	else:
		dst_dat_lines = open(args.dst_dat, encoding='latin_1').readlines()

	# Scan the ROM's directory.
	for root, dirs, files in os.walk(args.romdir[0]):
		for filename in files:
			full_filepath = os.path.join(root, filename)
			#if os.path.getsize(full_filepath) < 50000000:  # skip very big files? (>50MB)
			
			# extract curr file name and extension
			#rom_name, extension = os.path.splitext(filename)  # NOT WORKING correctly with multiple extensions
			import pathlib
			extension = "".join([s for s in pathlib.Path(filename).suffixes if (not " " in s and len(s)<=10)])
			rom_name = filename[:-len(extension)]
			#print(filename)
			#print(rom_name)
			#print(extension)
			
			# check the extension against know ROM extension
			if not extension[1:] in KNOWN_ROM_EXTENSION_LIST:
				src_rom_crc = get_crc32_from_datfile(src_dat_ext, src_dat_root, src_dat_lines, rom_name, args.partial_matches)
				if not src_rom_crc:
					logging.warning("nothing found in the source datfile (file skipped): " + rom_name)
					continue
			else:
				# curr file is a ROM
				if not args.include_roms:
					logging.warning("ROM file skipped (to override pass \"--include-roms\"): " + filename)
					continue
				else:
					src_rom_crc = get_file_crc32(full_filepath)
			# end if
			
			#logging.debug("found:" + src_rom_name +  ", crc32=" + src_rom_crc)		
			
			# look in the destination datfile for a ROM with a matching crc
			dst_rom_name = get_rom_name_from_crc32(dst_dat_ext, dst_dat_lines, dst_dat_root, src_rom_crc, extension)
			if not dst_rom_name:
				logging.warning("nothing found for crc=\"" + src_rom_crc + "\" in the destination datfile (file skipped): " + filename)
				continue
			# else do the renaming

			MOVE_COMMAND = "mv"
			if(os.name=="nt"):
				MOVE_COMMAND = "move"
			if (filename != dst_rom_name):
				full_dst_path = os.path.join(root, dst_rom_name)
				print(MOVE_COMMAND + " \"" + full_filepath + "\" \"" + full_dst_path + "\"")
				if args.rename:
					os.rename(full_filepath, full_dst_path)
		# end for filename in files
		if not args.recurse:
			break   #prevent descending into subfolders
	# end for
			

if __name__ == '__main__':
	main()
