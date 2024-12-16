@echo off
REM setlocal enableextensions enabledelayedexpansion
setlocal

call unix units --history '' -v -1 %*
if not [%ERRORLEVEL%]==[9009] goto :eof

call qalc %1 to %2
if not [%ERRORLEVEL%]==[9009] goto :eof

if [%1]==[] goto arg_error
if [%1]==[-h] goto arg_error
if [%1]==[--help] goto arg_error
if [%1]==[/?] goto arg_error
if [%2]==[] goto arg_error
if not [%3]==[] goto arg_error

set INPUT=%1
set TARGET=%2

REM echo|set /p="%INPUT% = %TARGET%"

REM cm->inches
REM IF NOT "%INPUT:cm%"=="%INPUT%"  if "%TARGET%"=="in" (
IF "%INPUT:~-2%"=="cm"  if "%TARGET%"=="in" (
	awk "BEGIN { printf \"%%%%%%%%g\n\", %INPUT:~0,-2% / 2.54 }"
	goto :eof
)

REM inches->cm
IF "%INPUT:~-2%"=="in"  if "%TARGET%"=="cm" (
	awk "BEGIN { printf \"%%%%%%%%g\n\", %INPUT:~0,-2% * 2.54 }"
	goto :eof
)

REM inches->mm
IF "%INPUT:~-2%"=="in"  if "%TARGET%"=="mm" (
	awk "BEGIN { printf \"%%%%%%%%g\n\", %INPUT:~0,-2% * 25.4 }"
	goto :eof
)

REM ounces->grams
IF "%INPUT:~-2%"=="oz"  if "%TARGET%"=="g" (
	awk "BEGIN { printf \"%%%%%%%%g\n\", %INPUT:~0,-2% * 28.349523125 }"
	goto :eof
)

REM grams->ounces
IF "%INPUT:~-1%"=="g"  if "%TARGET%"=="oz" (
	awk "BEGIN { printf \"%%%%%%%%g\n\", %INPUT:~0,-1% / 28.349523125 }"
	goto :eof
)

REM pounds (lb)->kg
IF "%INPUT:~-2%"=="lb"  if "%TARGET%"=="kg" (
	awk "BEGIN { printf \"%%%%%%%%g\n\", %INPUT:~0,-2% * 0.4535924 }"
	goto :eof
)

REM kg->pounds
IF "%INPUT:~-2%"=="kg"  if "%TARGET%"=="lb" (
	awk "BEGIN { printf \"%%%%%%%%g\n\", %INPUT:~0,-2% / 0.4535924 }"
	goto :eof
)

REM TODO: more units
REM gal->l
REM awg->mm
REM ... (see units.dat)

REM else
echo %0: err: unsupported I/O units: %*  1>&2
REM echo units command not found
exit /b 9009


:arg_error
	echo syntax: %0 QUANTITYfrom to
REM	echo MEMO: defaults to US units, for UK units add prefix "UK"
REM	echo see "%PENDRIVE%\Documents\db\misc\units.dat" for the list of supported units
	echo.
	REM goto :eof
	REM see also the manual C:\CLIPrograms\GnuWin32\man\cat1\units.1.txt
