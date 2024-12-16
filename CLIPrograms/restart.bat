@echo off
setlocal

set PROGPATH=%1
REM TODO: get full pathname of "%1" from tasklist?

REM kill the process
REM taskkill /f /im %1.exe
call pkill %1

echo sleep 3 seconds..
REM ping 127.0.0.1 -n 3 >NUL
call sleep 3

echo restarting %PROGPATH%
start "" %PROGPATH%
