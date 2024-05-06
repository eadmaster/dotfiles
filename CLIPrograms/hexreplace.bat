@echo off
setlocal

if [%1]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[--help] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if not exist "%3" set _HELP=ON
if [%_HELP%]==[ON] (
	echo usage: %0 HEX_STRING_ORIG  HEX_STRING_REPL  BINARY_FILE
	echo.
	echo MEMO: will create "*.patched" a file in CWD.
	goto :eof
)

REM using sfk http://stahlworks.com/dev/index.php?tool=rep
copy %3 "%~3.patched"
sfk replace "%~3.patched" -bin /%1/%2/  -yes
REM -tofile "%~3.patched"
