@echo off
setlocal

if [%1]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[--help] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if not exist "%2" set _HELP=ON
if [%_HELP%]==[ON] (
	echo usage: %0 HEX_STRING  BINARY_FILE
	echo.
	goto :eof
)

REM "http://stahlworks.com/dev/?tool=hexfind"
call sfk hexfind %2 -bin /%1/
if not [%ERRORLEVEL%]==[9009] goto :eof

call bgrep %*
if not [%ERRORLEVEL%]==[9009] goto :eof

REM http://ucon64.sourceforge.net/ucon64/readme.html
REM MEMO: must separate bytes with spaces (eg. "04 06" not "0406")
call ucon64 --hfind=%*
if not [%ERRORLEVEL%]==[9009] goto :eof

REM last chance
call cat "%2" | hexdump -C | grep "%1"
