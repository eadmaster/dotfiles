@echo off
setlocal

if [%1]==[] (
	set GTK_HOME=%~d0\PortableApps\qalculate
	set GTK_BASEPATH=%~d0\PortableApps\qalculate
	REM TODO: move gnuplot inside %~d0\PortableApps\qalculate?
	set PATH=C:\CLIPrograms\gnuplot-5.2.4\bin
	%~d0\PortableApps\qalculate\qalculate.exe %*
	if not [%ERRORLEVEL%]==[9009] goto :eof
	
	REM Windows default calc
	%WINDIR%\System32\calc.exe
	goto :eof
)

call qalc %*
if not [%ERRORLEVEL%]==[9009] goto :eof

echo %* | call awk "BEGIN { printf \"\t%%%%%%%%g\n\", %*}"
if not [%ERRORLEVEL%]==[9009] goto :eof

echo %* | call bc -l
if not [%ERRORLEVEL%]==[9009] goto :eof

call units %*
if not [%ERRORLEVEL%]==[9009] goto :eof

REM else
echo %0: warn: no bc or awk found, using set cmd math (integer only)...  1>&2
SET /A RES = %*
echo 	%* = %RES%
