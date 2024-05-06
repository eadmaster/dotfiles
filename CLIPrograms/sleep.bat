@echo off

call unix sleep %*
if not [%ERRORLEVEL%]==[9009] goto :eof

if exist "%~dp0nircmdc.bat" (
	call "%~dp0nircmdc.bat" wait %1000
	goto :eof
)

if exist "%~dp0sfk.exe" (
	"%~dp0sfk.exe" sleep %1000
	goto :eof
)

if exist "%PYTHONHOME%\python.exe" (
	"%PYTHONHOME%\python.exe" -c "import time; time.sleep(%1)"
	goto :eof
)

if exist "%WINDIR%\System32\timeout.EXE" (
	"%WINDIR%\System32\timeout.EXE" /T %1 /NOBREAK
	goto :eof
)

REM else
REM ping 1.1.1.1 -n 1 -w %1000 > nul
ping 127.0.0.1 -n %1 >NUL
goto :eof

REM ALTERNATIVES:
REM   NO? %~dp0_CANCELLARE\WindowsServer2003-ResourceKitTools-28.04.2003\sleep.exe
REM   ... http://stackoverflow.com/questions/1672338/how-to-sleep-for-5-seconds-in-windowss-command-prompt-or-dos
