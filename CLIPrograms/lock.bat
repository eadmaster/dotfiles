@echo off
setlocal

REM call unix flock %*
REM if not [%ERRORLEVEL%]==[9009] goto :eof

if [%1]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if [%_HELP%]==[ON] (
	echo usage: %0 FILETOLOCK
	REM echo usage flock lockfile command...
	goto :eof
)

if not exist %1 (
	echo %0 error: does not exist: %1
	goto :eof
)

REM use redirect trick to lock any file  http://superuser.com/questions/294826/how-to-purposefully-exclusively-lock-a-file
start "" /MIN notepad >> %1
echo %0: "%1" locked, close notepad to release the lock...
REM %2 %3 %4 %5 %6 %7 %8 %9
