@echo off
setlocal EnableDelayedExpansion

if [%1]==[start] service av %1
if [%1]==[stop] service av %1
REM else file scan mode

REM TODO: detect if invoked from Windows shell or console -> prefer GUI or CLI output

REM test if input is not a directory
if exist %*\NUL goto recursive_scan
REM else input is a single file
REM online scan
FOR /F "tokens=1" %%H IN ('openssl dgst -sha256 -r %*') DO xdg-open "http://www.virustotal.com/en/file/%%H/analysis/"
REM FOR /F "tokens=1" %%H IN ('busybox sha256sum %*') DO start "" "http://www.virustotal.com/en/file/%%H/analysis/"
REM goto :eof

:recursive_scan
REM Windows Defender
if exist "%ProgramFiles%\Windows Defender\MpCmdRun.exe" (
	REM echo %0: launching Windows Defender... ^(if malware is found an alert will be shown^)
	"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -scan -scantype 3 -File %*
	REM type %PROGRAMDATA%\Microsoft\Windows Defender\...
	REM goto :eof
)
echo.
REM Avira AntiVir Desktop
if exist "%PROGRAMFILES%\Avira\AntiVir Desktop" (
	"%PROGRAMFILES%\Avira\AntiVir Desktop\avscan.exe" /PATH=%*
	REM goto :eof
)
echo.
REM Avira AntiVir CLI
set SCANCLPATH=%~dp0scancl-1.9.150.0
if exist "%SCANCLPATH%\vdf" set IDF_PATH=%SCANCLPATH%\vdf
if exist "%PROGRAMFILES%\Avira\AntiVir Desktop" set IDF_PATH=%PROGRAMFILES%\Avira\AntiVir Desktop
if exist "%SCANCLPATH%\scancl.exe" (
	REM if exist "%PROGRAMFILES%\Avira\AntiVir Desktop" set ADDITIONAL_OPTIONS=
	REM  ALSO: C:\Program Files\Avira\AntiVir Desktop\FAILSAFE
	"%SCANCLPATH%\scancl.exe" --nombr --recursion --colors --quarantine=%TEMP% --workingdir="%IDF_PATH%" --heurlevel=1 %*
	REM --scaninarchive
	REM --archivemaxsize=100MB
	REM --defaultaction=ask
	REM --suspiciousaction=ask
	REM -r3 -e -ren -alltypes -tmp R:\temp
)
echo.
REM Microsoft Security Essentials
REM  TODO: more verbose
if exist "%PROGRAMFILES%\Microsoft Security Client" (
	"%PROGRAMFILES%\Microsoft Security Client\MpCmdRun.exe" -Scan -ScanType 3 -File %*
)
if exist "%ProgramW6432%\Microsoft Security Client" (
	"%ProgramW6432%\Microsoft Security Client\MpCmdRun.exe" -Scan -ScanType 3 -File %*
)
echo.
REM AVG2013
if exist "%PROGRAMFILES%\AVG\AVG2013\avgscanx.exe" (
	"%PROGRAMFILES%\AVG\AVG2013\avgscanx.exe" /SCAN=%*
)
echo.
REM TODO: other antiviruses check: clamscan, panda, nav, etc.

REM keeps the window opened if invoked from the GUI  http://stackoverflow.com/questions/9419875/determining-if-the-batch-script-has-been-executed-from-the-command-line-or-to
REM echo %CMDCMDLINE% | find /i "/c"
REM if ERRORLEVEL 1 pause
REM pause
REM goto :eof
