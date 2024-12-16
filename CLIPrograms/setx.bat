@echo off
REM setlocal -> NO, we also want to affect the current environment...

REM MS Resource Kit's SETX.EXE Replacement 
REM by eadmaster

REM Set environment variables permanently in the user profile
REM http://www.ss64.com/nt/setx.html

if [%1]==[/?] goto :syntax
if [%1]==[-h] goto :syntax
if [%2]==[] goto :syntax

if [%2]==[-d] (
	REG delete HKCU\Environment /V %1 > NUL
	if [%ERRORLEVEL%]==[0] (
		echo %0: "%1" deleted successfully from registry
		SET %1=
	) else (
		echo %0: ERROR unable to delete "%1" from registry
	)
	goto :eof
)

if [%3]==[-m] (
	set TARGET=HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
) else (
	set TARGET=HKCU\Environment
)

REG add %TARGET% /v %1 /d %2 /F > NUL
if [%ERRORLEVEL%]==[0] (
	echo %0: "%1=%2" stored in the registry key "%TARGET%"
	SET %1=%2
) else (
	echo %0: ERROR unable to store "%1=%2" in the registry key "%TARGET%"
)
goto :eof

:syntax
echo.
echo Usage:
echo  SETX [Variable] [Value] -^> set the value in current user profile
echo  SETX [Variable] [Value] -m -^> Set the value in the Machine environment (HKLM) - Default is User (HKCU)
echo  SETX [Variable] -d -^> delete specified value
echo.
