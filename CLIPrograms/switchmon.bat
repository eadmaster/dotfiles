@echo off
REM setlocal EnableDelayedExpansion

REM if exist "%PROGRAMFILES%\ATI Technologies\ATI.ACE\Core-Static\CLI.exe" (
	REM "%PROGRAMFILES%\ATI Technologies\ATI.ACE\Core-Static\CLI.exe" ??
REM 	goto :eof
REM )

REM Win7 only
if exist "%WINDIR%\system32\displayswitch.exe" (
	"%WINDIR%\system32\displayswitch.exe"
	REM supported switches: http://jeffwouters.nl/index.php/2012/06/switch-your-display-through-the-command-line/
	goto update
)

if exist "%~d0\PortableApps\NirLauncher\NirSoft\MultiMonitorTool.exe" (
	"%~d0\PortableApps\NirLauncher\NirSoft\MultiMonitorTool.exe" /switch 1 2
	goto update
)

REM ALTERNATIVE with nircmdc:
REM env variable to hold current primary monitor index
REM if not defined DISPLAY set DISPLAY=1
REM if not defined DISPLAY set DISPLAY=\\.\DISPLAY1
REM cycle between 2 monitors
REM if %DISPLAY%==1 set DISPLAY=2
REM if [%DISPLAY%]==[\\.\DISPLAY1] set DISPLAY=\\.\DISPLAY2
REM if %DISPLAY%==2 set DISPLAY=1
REM if [%DISPLAY%]==[\\.\DISPLAY2] set DISPLAY=\\.\DISPLAY1
REM call nircmdc monitor off
REM call nircmdc setprimarydisplay %DISPLAY%

REM else
echo %0: unable to find any monitor switcher
goto :eof


:update
REM update environment variables
call initenv

REM enforce correct resolution
REM call nircmdc setdisplay %XRES% %YRES% %DISPLAY_DEPTH% %DISPLAY_REFRESH% -updatereg -allusers
