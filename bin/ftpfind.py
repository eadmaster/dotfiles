#!/usr/bin/env python

# code derived from https://gist.githubusercontent.com/flibbertigibbet/8165881/raw/7f580b6735ad1f03c6e6060cd1c8571048afad6a/recurse_ftp.py

from ftplib import FTP
from time import sleep
import os
import sys

my_dirs = []  # global
curdir = ''   # global

PROGRAM_NAME = os.path.basename(sys.argv[0])

if len(sys.argv) <= 1 or sys.argv[1].startswith("-"):
  print("usage: " + PROGRAM_NAME + " SERVER_ADDR [SERVER_ROOT_DIR] [USERNAME] [PASSWORD] [MAX_LEVEL]") 
  # TODO: dirs only listing
  # TODO: use argparse
  sys.exit(1)
# else
SERVER_ADDR = sys.argv[1]

SERVER_ROOT_PATH = "/"
if len(sys.argv) >= 3:
  SERVER_ROOT_PATH = sys.argv[2]
USERNAME = None
if len(sys.argv) >= 4:
  USERNAME = sys.argv[3]
PASSWORD = None
if len(sys.argv) >= 5:
  PASSWORD = sys.argv[4]
MAX_LEVEL = 1
if len(sys.argv) >= 6:
  MAX_LEVEL = int(sys.argv[5])

  
def get_dirs(ln):
  global my_dirs
  cols = ln.split(' ')
  objname = cols[len(cols)-1] # file or directory name
  if ln.startswith('d'):
    my_dirs.append(objname)
  elif(objname == ".."):
    return
  else:
    print(curdir + "/" + objname)

def check_dir(adir, level=0):
  if level >= MAX_LEVEL:
    # end recursion
    return
  # else
  #sys.stderr.write("level=" + str(level))
  global my_dirs
  global curdir
  my_dirs = []
  gotdirs = [] # local
  try:
    curdir = ftp.pwd()
    sys.stderr.write(PROGRAM_NAME + ": going to change to directory " + adir + " from " + curdir + "\n")
    ftp.cwd(adir)
    curdir = ftp.pwd()
    ftp.retrlines('LIST', get_dirs)
  except:
    return
  print(curdir + "/")
  gotdirs = my_dirs
  #print("found in " + adir + " directories:")
  sleep(0.5)
  for subdir in gotdirs:
    if subdir.startswith("."):
      continue
    my_dirs = []
    check_dir(subdir, level+1) # recurse  
  # end for
  ftp.cwd('..') # back up a directory when done here
# end of check_dir


# main
try:
  ftp = FTP(SERVER_ADDR)
  if USERNAME and PASSWORD:
    ftp.login(user=USERNAME, passwd=PASSWORD)
  else:
    ftp.login()  # user anonymous, passwd anonymous@
  check_dir(SERVER_ROOT_PATH) # directory to start in

except:
  import logging
  logging.exception("")
  ftp.quit()

ftp.quit()
