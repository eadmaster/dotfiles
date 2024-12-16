#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import os
import stat
import io
import logging
import zipfile
import tarfile

PROGRAM_NAME = os.path.basename(sys.argv[0])

sys.path.append( os.path.dirname(__file__) )  # try to load modules from subdirs

sys.stdout.reconfigure(encoding='utf-8')  # prevents encoding errors in py3.7+ https://stackoverflow.com/questions/4374455/how-to-set-sys-stdout-encoding-in-python-3/33470043

# catch sigints
def sigint_handler(signum, frame):
    # TODO: exit all threads?
    sys.exit(1)
import signal
signal.signal(signal.SIGINT, sigint_handler)

try:
	# faster, but not available on some platforms  https://stackoverflow.com/questions/44502855/why-is-zlib-crc32-faster-than-binascii-crc32
	from zlib import crc32
except:
	# slower
	from binascii import crc32

try:
	from lib7zip import Archive, formats
except:
	#logging.exception("")
	sys.stderr.write(PROGRAM_NAME + ": warn: lib7zip modules missing, run pip install git+https://github.com/topia/pylib7zip\n")

# TODO: nest in
#def archive2fileslist(filename):

class SevenZipFile(object):
	"""
	zipfile-like wrapper class for 7-zip file info descriptors
	"""
	def __init__(self, file_desc):
		import lib7zip
		if(not isinstance(file_desc, lib7zip.archive.ArchiveItem)):
			return
		self.filename = file_desc.path
		self.filename = self.filename.lstrip("./")  # prefix in tar archives
		self.file_size = file_desc.size
		from datetime import timezone, timedelta
		file_dt_obj = file_desc.mtime
		#file_dt_obj = file_desc.mtime.astimezone(timezone.utc)
		#file_dt_obj = file_desc.mtime.replace(tzinfo=None)
		#file_dt_obj = file_desc.mtime.replace(tzinfo=timezone.utc)
		# TODO: fix in lib?
		#file_dt_obj = file_desc.mtime.replace(hour=file_dt_obj.hour-9)
		if not file_desc.mtime:
			# date missing
			file_dt_obj = datetime.fromtimestamp(0)  # init as unix epoch
		self.date_time = tuple((file_dt_obj.year, file_dt_obj.month, file_dt_obj.day, file_dt_obj.hour, file_dt_obj.minute, file_dt_obj.second))
		self.CRC = file_desc.crc
		if not self.CRC:
			# extract in memory and compute the crc32
			self.CRC = 0
			f_contents = ""
			try:
				f_contents = file_desc.contents
			except:
				# possible extraction error
				logging.exception("")  # print the full stacktrace
			if len(f_contents) > 0:
				self.CRC = crc32(f_contents)

class TarFile(object):
	"""
	zipfile-like wrapper class for Tar file info descriptors
	"""
	def __init__(self, file_desc, opened_tar_file):
		if(not isinstance(file_desc, tarfile.TarInfo)):
			return
		self.filename = file_desc.name
		self.CRC = 0
		#print(opened_tar_file.extractfile(file_desc.name))
		file_content_byte = None
		try:
			file_content_byte = opened_tar_file.extractfile(file_desc.name)
		except:
			pass
		if file_content_byte:
			# read the whole file inmemory (slow)
			file_content_byte = file_content_byte.read()
			self.CRC = crc32(file_content_byte)
		self.file_size = file_desc.size
		file_dt_obj = datetime.fromtimestamp(file_desc.mtime)
		self.date_time = tuple((file_dt_obj.year, file_dt_obj.month, file_dt_obj.day, file_dt_obj.hour, file_dt_obj.minute, file_dt_obj.second))
	
def main():
	# args check
	# TODO: use argparse
	# TODO: add cmdline switch to skip header with datetimes
	# TODO: add cmdline switch to skip system files like 
	#  https://github.com/github/gitignore/blob/main/Global/macOS.gitignore
	#  https://github.com/github/gitignore/blob/main/Global/Windows.gitignore
	if(len(sys.argv)==1 or sys.argv[1] in ['-h', '--help'] or not os.path.isfile(sys.argv[1])):
		print("usage: " + PROGRAM_NAME + " file.ext")
		print("")
		sys.stdout.write("supported archive formats: zip, tar")  # from python stdlib
		if "lib7zip" in sys.modules:  # check if lib7zip was imported
			sys.stdout.write(", ")
			for format in formats:
				sys.stdout.write(str(format) + ", ")
		else:
			print("")
			sys.stdout.write("for more, pip install git+https://github.com/topia/pylib7zip\n")
		print("")
		sys.exit(0)

	inputfilename = sys.argv[1]
	#_, inputfile_extension = os.path.splitext(inputfilename)  # TODO: better hadling

	# open the file a fill archive_files_list
	inputfile = None
	archive_files_list = []

	if "lib7zip" in sys.modules:
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
				".rar" : [ "Rar" ]
				#".tar" : [ "tar"],
				# TODO: more formats? APM, Ar, Arj, bzip2, Cab, Chm, Hxs, Compound, Cpio, CramFS, Dmg, ELF, FLV, gzip, GPT, HFS, IHex, Iso, Lzh, lzma, lzma86, MachO, MBR, MsLZ, Mub, Nsis, PE, TE, Ppmd, QCOW, Rar, Rar5, Rpm, Split, SquashFS, SWFc, SWF, tar,  UEFIc, UEFIf, VDI, VHD, VMDK, wim, Xar, xz, Z, zip
			}
			for ext in ext_to_types_to_try_dict:
				if(inputfilename.lower().endswith(ext)):
					for type_to_try in ext_to_types_to_try_dict[ext]:
						try:
							archive = Archive(inputfilename, forcetype=type_to_try)
						except:
							logging.exception("")
							#pass
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
		else:
			# populate archive_files_list
			for f in archive:
				if f.is_dir:
					continue
				if f.symlink: # skip symlinks
					continue
				archive_files_list.append( SevenZipFile(f) )
		# end if
	# endif "lib7zip" in sys.modules:
	
	elif(zipfile.is_zipfile(inputfilename)):
		inputfile = zipfile.ZipFile(inputfilename, 'r')
		archive_files_list = inputfile.infolist()
		
	elif(tarfile.is_tarfile(inputfilename)):
		sys.stderr.write(PROGRAM_NAME + ": warn: tar files have no builtin hashes, need to extract the archive in memory (slow)\n")
		inputfile = tarfile.open(inputfilename, 'r')
		archive_files_members = inputfile.getmembers()
		for m in archive_files_members:
			if m.isdir():
				continue  # skip dirs
			archive_files_list.append( TarFile(m, inputfile) )
	else:
		sys.stderr.write(PROGRAM_NAME + ": fatal error: input archive format not supported\n")
		sys.exit(1)

	# output SFV to stdout
	
	# OPTIONAL HEADER
	print("; Generated by " + PROGRAM_NAME + " on " + datetime.now().strftime("%Y-%m-%d at %H:%M.%S"))
	print("; Written by eadmaster - http://eadmaster.altervista.org/")
	print(";")
	for f in archive_files_list:
		#if(stat.S_IFDIR(f.external_attr)):
		#if((f.external_attr & stat.S_IFMT)==stat.S_IFDIR): #req. py3.x
		if(f.filename.endswith("/")):
			continue # skip directories
		print("; %12s  %s %s" % ( f.file_size, datetime(*f.date_time).strftime("%H:%M.%S %Y-%m-%d"), f.filename))
	# END OF OPTIONAL HEADER

	for f in archive_files_list:
		try:
			if(f.filename.endswith("/")):
				continue # skip directories
			print("%s %08X " % ( f.filename, f.CRC ) )
		except:
			continue
# end of main


if __name__ == '__main__':
	main()
	# clean exit
	sys.exit(0)
