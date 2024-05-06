@echo off
setlocal

ugrep -F -i -I -r -z -Z2 -w --exclude-dir=_\* --exclude=*.torrent -H %*
goto :eof


REM OLD ALTERNATIVES:

REM if [%~x2]==[.zip] (
zzfind -text %2 %1
goto :eof
REM	REM zzfind -text -pat %1 -dir %2
REM	goto :eof
REM )

REM else
REM echo %2:
REM call file2txt %2 | grep %1

if exist %2 file2txt %2 ^| grep %1
if exist %3 file2txt %3 ^| grep %1 %2
if exist %4 file2txt %4 ^| grep %1 %2 %3
if exist %5 file2txt %5 ^| grep %1 %2 %3 %4
if exist %6 file2txt %6 ^| grep %1 %2 %3 %4 %5

REM else
echo syntax: filegrep [OPTION]... PATTERN [FILE]... 
