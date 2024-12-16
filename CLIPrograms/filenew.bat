@echo off
setlocal

if [%1]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if [%_HELP%]==[ON] (
	echo usage: %0 NEWFILENAME
	echo.
	goto :eof
)

if exist %1 (
	echo %0: err: file already exist: %1  1>&2
	exit /b 1
)
REM else %1 does not exit

if not defined XDG_TEMPLATES_DIR call initenv
REM if not defined XDG_TEMPLATES_DIR set XDG_TEMPLATES_DIR=%USERPROFILE%\Templates
if not defined XDG_TEMPLATES_DIR set XDG_TEMPLATES_DIR=%ALLUSERSPROFILE%\Templates
if exist %PENDRIVE%\Documents\tem set XDG_TEMPLATES_DIR=%PENDRIVE%\Documents\tem

if exist "%XDG_TEMPLATES_DIR%\new.%~x1" set TEMPLATE_FILE="%XDG_TEMPLATES_DIR%\new.%~x1"
if exist "%XDG_TEMPLATES_DIR%\example.%~x1" set TEMPLATE_FILE="%XDG_TEMPLATES_DIR%\example.%~x1"
if exist "%XDG_TEMPLATES_DIR%\hello.%~x1" set TEMPLATE_FILE="%XDG_TEMPLATES_DIR%\hello.%~x1"
if exist "%XDG_TEMPLATES_DIR%\reference.%~x1" set TEMPLATE_FILE="%XDG_TEMPLATES_DIR%\reference.%~x1"
if exist "%XDG_TEMPLATES_DIR%\tpk.%~x1" set TEMPLATE_FILE="%XDG_TEMPLATES_DIR%\tpk.%~x1"
REM if not exist "%TEMPLATE_FILE%" for /f "delims=" %%G in ('dir /b "%XDG_TEMPLATES_DIR%\*%~x1"') do set TEMPLATE_FILE="%XDG_TEMPLATES_DIR%\%%G"

if exist "%TEMPLATE_FILE%" (
	echo %0: creating new file from %TEMPLATE_FILE% -^> %*
	copy %TEMPLATE_FILE% %*
	goto :eof
)

REM else just create an empty file
echo %0: no template found, creating an emtpy file...   
copy NUL %1
