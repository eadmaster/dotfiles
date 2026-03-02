@echo off

if not defined SYSINTERNALS_PATH call initenv.bat
"%SYSINTERNALS_PATH%\pssuspend.exe" -accepteula -r %*.exe
if not [%ERRORLEVEL%]==[9009] goto :eof

REM TODO: check if nircmdc ver >=2.75
call nircmdc resumeprocess %*.exe
if not [%ERRORLEVEL%]==[9009] goto :eof

REM else
exit /b 9009