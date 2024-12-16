@echo off

if [%1]==[] goto current_pc
REM else look for a remote pc
if exist %PENDRIVE%\Documents\db\mynicmac.csv (
	findstr /I /C:"%*" %PENDRIVE%\Documents\db\mynicmac.csv
	goto :eof
)
if exist "%WINDIR%\System32\getmac.exe" (
	REM UNTESTED:
	"%WINDIR%\System32\getmac.exe" /S %* /U Administrator /V
	goto :eof
)
echo unable to find getmac
goto :eof

:current_pc
ipconfig /all
