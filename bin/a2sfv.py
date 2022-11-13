#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import os
import stat
import io
import logging

# pip install git+https://github.com/topia/pylib7zip
from lib7zip import Archive, formats

try:
	# faster, but not available on some platforms  https://stackoverflow.com/questions/44502855/why-is-zlib-crc32-faster-than-binascii-crc32
	from zlib import crc32
except:
	# slower
	from binascii import crc32

PROGRAM_NAME = os.path.basename(sys.argv[0])

sys.path.append( os.path.dirname(__file__) )  # try to load modules from subdirs

sys.stdout.reconfigure(encoding='utf-8')  # prevents encoding errors in py3.7+ https://stackoverflow.com/questions/4374455/how-to-set-sys-stdout-encoding-in-python-3/33470043

# catch sigints
def sigint_handler(signum, frame):
    # TODO: exit all threads?
    sys.exit(1)
import signal
signal.signal(signal.SIGINT, sigint_handler)

def main():
	# args check
	if(len(sys.argv)==1 or sys.argv[1] in ['-h', '--help'] or not os.path.isfile(sys.argv[1])):
		print("usage: " + PROGRAM_NAME + " file.ext")
		sys.stdout.write("supported archive formats: ")
		for format in formats:
			sys.stdout.write(str(format) + ", ")
		print("")
		sys.exit(0)

	inputfilename = sys.argv[1]
	#_, inputfile_extension = os.path.splitext(inputfilename)  # TODO: better hadling

	# read input archive file
	archive = None

	try:
		archive = Archive(inputfilename)
	except:
		#logging.exception("")  # print the full stacktrace
		sys.stderr.write(PROGRAM_NAME + ": err: error auto-guessing archive type\n")
		# try guess file type based on extension
		ext_to_types_to_try_dict = {
			".ima" : [ "FAT", "Ext", "NTFS", "Iso", "Udf" ],
			".img" : [ "FAT", "Ext", "NTFS", "Iso", "Udf" ],
			".iso" : [ "Udf", "Iso" ],
			".udf" : [ "Udf", "Iso" ],
			#".tar" : [ "tar"],
			# TODO: more formats? APM, Ar, Arj, bzip2, Cab, Chm, Hxs, Compound, Cpio, CramFS, Dmg, ELF, FLV, gzip, GPT, HFS, IHex, Iso, Lzh, lzma, lzma86, MachO, MBR, MsLZ, Mub, Nsis, PE, TE, Ppmd, QCOW, Rar, Rar5, Rpm, Split, SquashFS, SWFc, SWF, tar,  UEFIc, UEFIf, VDI, VHD, VMDK, wim, Xar, xz, Z, zip
		}
		for ext in ext_to_types_to_try_dict:
			if(inputfilename.lower().endswith(ext)):
				for type_to_try in ext_to_types_to_try_dict[ext]:
					try:
						archive = Archive(inputfilename, forcetype=type_to_try)
					except:
						pass
				# end for
			# end if
		# end for
		
	# special handling for tarballs (nested archives)
	if(inputfilename.endswith(( ".tar.gz", ".tgz", ".tar.xz", ".txz", ".tar.bz2", ".tbz", ".tar.lzma", ".tar.lz", ".tlz" ))):
		sys.stderr.write(PROGRAM_NAME + ": warn: tar files have no builtin hashes, need to extract the archive in memory (slow)\n")
		#TODO: if small, extract the whole archive in memory
		#tarfilebuf = io.BytesIO(archive[0].contents)
		#archive = Archive(tmpfile.name, stream=tarfilebuf, forcetype="tar")
		# else via a tempfile
		import tempfile
		tmpfile = tempfile.NamedTemporaryFile()
		tmpfile.write(archive[0].contents)
		archive = Archive(tmpfile.name, stream=tmpfile, forcetype="tar")
	# end if tarball
	
	if not archive:
		sys.stderr.write(PROGRAM_NAME + ": fatal error: input archive format not supported\n")
		sys.exit(1)

	# TODO: if archive is not compressed
	#sys.stderr.write(PROGRAM_NAME + ": warn: RAW fs files have no builtin hashes, need to extract the archive in memory (slow)\n")
		
	# HEADER
	print("; Generated by " + PROGRAM_NAME + " on " + datetime.now().strftime("%Y-%m-%d at %H:%M.%S"))
	print("; Written by eadmaster - http://eadmaster.altervista.org/")
	print(";")
	for f in archive:
		if f.is_dir:
			continue
		if f.symlink: # skip symlinks
			continue
		if not f.mtime:
			# date missing
			f.mtime = datetime.fromtimestamp(0)  # init as unix epoch
		print("; %12s  %s %s" % ( f.size, f.mtime.strftime("%H:%M.%S %Y-%m-%d"), f.path))
	# END OF HEADER

	# 2nd listing with CRC32 hashes
	for f in archive:
		if f.is_dir:
			continue
		if f.symlink: # skip symlinks
			continue
		f_crc = f.crc
		if not f_crc:
			# extract in memory and compute crc32
			f_crc = 0
			try:
				f_contents = f.contents
			except:
				# possible extraction error
				logging.exception("")  # print the full stacktrace
				continue
			if len(f_contents) > 0:
				f_crc = crc32(f_contents)
		# end if
		print("%s %08X " % ( f.path, f_crc ) )
	# end for


if __name__ == '__main__':
	main()
	# clean exit
	sys.exit(0)
