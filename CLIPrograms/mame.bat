@echo off
setlocal

REM extract faq if exist
REM call 7z e -y -o%TEMP% %PENDRIVE%\Documents\db\faq\mame.zip %1.faq
REM if exist %RAMDRIVE%\%1.faq  call geany %TEMP%\%1.faq
REM if [%1]==[aed]  start "" "%~dp0_MEMO.txt"
REM start "" "%~d0\Games\MAME\_MEMO.txt"
REM del /Q %TEMP%\%1.faq

goto regular_mame

REM prefer accelerated emus if available
if exist "%~d0\Games\Model2Emulator\roms\%1.zip" (
	m2emu %1
	goto :eof
)
if exist "%~d0\Games\SSF\roms\%1.zip" (
	ssf %1
	goto :eof
)
if exist "%~d0\Games\pSxMAME\roms\%1.zip" (
	psxmame %1
	goto :eof
)
if exist "%~d0\Games\pSxMAME\roms\%1.chd" (
	psxmame %1
	goto :eof
)
if exist "%~d0\Games\mameppk\roms\%1.zip" (
	psxmame %1
	REM mameppk %1
	goto :eof
)
REM if exist C:\Games\nullDC-Naomi\Roms\%1.lst (
REM ...
REM	goto :eof
REM )
if exist "%~d0\Games\DEmul\roms\%1.zip" (
	demul -run=naomi2 -rom=%1
	REM demul -run=naomi2|... -rom=%1
	goto :eof
)

REM if exist "%~d0\Games\FBAS\cheats\%1.xml" (
REM  	fba -g %1
	REM  -w
REM )

:regular_mame
set MAME_PATH=%~d0\Games\MAME
set MAME_OPTIONS=-inipath %MAME_PATH%;%MAME_PATH%\ini 
REM -cfg_directory R:\TEMP

::if [%COMPUTERNAME%]==[BOSS3]  (
	::REM enable shaders
	::set MAME_OPTIONS=%MAME_OPTIONS% -hlsl_enable 1
::) else (
	::REM enable scanlines
	::set MAME_OPTIONS=%MAME_OPTIONS% -effect Scanrez2
	::REM req. %MAME_PATH%\artwork\Scanrez2.png
::)

REM TODO: detect currently connected controller
REM devcon find "HID\VID_1345&PID_0003"
REM NO? if %ERRORLEVEL%==...
REM  | look at HKLM\SYSTEM\CurrentControlSet\Enum\USB
REM  | USBDView ... http://www.nirsoft.net/utils/usb_devices_view.html
REM set MAME_OPTIONS=%MAME_OPTIONS% -ctrlr FlyEagle
REM else
REM set MAME_OPTIONS=%MAME_OPTIONS% -ctrlr mouse2

REM call mynotes mame

REM mkdir R:\MAME\cfg
REM copy /Y D:\Documenti\ROMs\MAME\cfg\default.cfg R:\MAME\cfg

if not exist "%ProgramFiles(x86)%" goto 32bit
REM else 64-bit


if exist "%MAME_PATH%\houbappkui64.exe" (
	start "" /B /D"%MAME_PATH%" houbappkui64.exe %MAME_OPTIONS% %*
	REM TODO: send keystroke: F11 -> Show FPS
	REM TODO: send keystroke: Space for 10 seconds - quickstart
	REM TODO: while mame is runnning:
	REM   quicksave
	REM   sleep 5 seconds
	exit /b %ERRORLEVEL%
)

if exist "%MAME_PATH%\negamame.exe" (
	start "" /B /D"%MAME_PATH%" negamame.exe %*
	exit /b %ERRORLEVEL%
)

REM else fallback to 32-bit
:32bit
if exist "%MAME_PATH%\houbappkui.exe" (
	start /D "%MAME_PATH%" houbappkui.exe %MAME_OPTIONS% %*
	exit /b %ERRORLEVEL%
)

if exist "%MAME_PATH%\mamep.exe" (
	start "" /B /D"%MAME_PATH%" mamep.exe %MAME_OPTIONS% %*
	exit /b %ERRORLEVEL%
)

if exist "%MAME_PATH%\mame.exe" (
	"%MAME_PATH%\mame.exe" %MAME_OPTIONS% %*
	exit /b %ERRORLEVEL%
)

REM else
echo no MAME executable found
exit /b 9009
