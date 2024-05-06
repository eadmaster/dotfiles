@echo off
setlocal

if [%1]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if not exist %1 set _HELP=ON
if [%_HELP%]==[ON] (
	echo usage: %0 INPUTFILE
	goto :eof
)

set INPUTFILE=%1

REM echo %0: Chromaprint of %INPUTFILE%... 1>&2
REM call ffmpeg -loglevel error  -i %INPUTFILE% -f chromaprint -

echo.
echo.

echo %0: computing media hashes of %INPUTFILE%... 1>&2

call ffmpeg -loglevel error -i %INPUTFILE% -vn  -f crc - 2^> NUL

call ffmpeg -loglevel error -i %INPUTFILE% -vn  -f md5 - 2^> NUL

call ffmpeg -loglevel error -i %INPUTFILE% -vn  -f hash - 2^> NUL

