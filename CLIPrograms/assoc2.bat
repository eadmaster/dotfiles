@echo off
setlocal

REM TODO: add ShellNew?

if [%2]==[]  (
	REM echo help
	echo usage: assoc2 .ext ftype [PerceivedType] [MIME]
	echo PerceivedType can be: audio, compressed, document, image, system, text, or video
	echo see MIME types list here http://www.iana.org/assignments/media-types/ or here http://en.wikipedia.org/wiki/Internet_media_type
	exit /b 0
)

REM TODO: check if ftype exist with reg query or ftype

reg delete HKCU\Software\Classes\%1 /f >NUL

reg add HKCU\Software\Classes\%1 /f >NUL
reg add HKCU\Software\Classes\%1 /ve /d %2 /f >NUL
if not [%3]==[] reg add HKCU\Software\Classes\%1 /v "PerceivedType" /d %3 /f >NUL
if not [%4]==[] reg add HKCU\Software\Classes\%1 /v "Content Type" /d %4 /f >NUL
