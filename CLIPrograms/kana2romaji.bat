@echo off
setlocal

REM if [%1]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if [%_HELP%]==[ON] (
	echo usage: %0 STRING|FILE_TO_TRANSLITERATE
	goto :eof
)

chcp 65001 > NUL

set INPUT=%1

if exist %INPUT% (
	type %INPUT% | uconv -f utf-8 -t utf-8 -x "Any-Latin;Latin-ASCII"
	REM type %INPUT% | sed -f "%~dp0bin\kana2romaji"
	goto :eof
) else (
	if [%1]==[] set /p INPUT=
	echo %INPUT% | uconv -f utf-8 -t utf-8 -x "Any-Latin;Latin-ASCII"
	REM echo %INPUT% | sed -f "%~dp0bin\kana2romaji"
	goto :eof
)

REM else
exit /b 9009
