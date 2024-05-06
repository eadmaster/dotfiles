@echo off
setlocal

REM goto espeak
goto nircmd

if not defined FESTIVAL (
	if exist "%SYSTEMDRIVE%\festival" set FESTIVAL=%SYSTEMDRIVE%\festival
	if exist "%PROGRAMFILES%\festival" set FESTIVAL=%PROGRAMFILES%\festival
	REM if exist "%~dp0_TESTING\festival-2.1" set FESTIVAL=%~dp0_TESTING\festival-2.1
	if exist "%~dp0festival-2.1" set FESTIVAL=%~dp0festival-2.1
	if exist "%~dp0festival-2.4" set FESTIVAL=%~dp0festival-2.4
)
if exist "%FESTIVAL%\festival.exe" (
	if not [%1]==[] (
		echo %* | "%FESTIVAL%\festival.exe" --libdir "%FESTIVAL%\lib" --tts
	) else (
		"%FESTIVAL%\festival.exe" --libdir "%FESTIVAL%\lib" --tts
	)
	goto :eof
)

:espeak
if not defined ESPEAK_DATA_PATH (
	if exist "%PROGRAMFILES%\eSpeak" set ESPEAK_DATA_PATH=%PROGRAMFILES%\eSpeak
	if exist %~d0\PortableApps\eSpeak set ESPEAK_DATA_PATH=%~d0\PortableApps\eSpeak
)
if exist "%ESPEAK_DATA_PATH%\command_line\espeak.exe" (
	if [%1]==[] (
		"%ESPEAK_DATA_PATH%\command_line\espeak.exe" -s 100 -v f2 --stdin
	) else (
		"%ESPEAK_DATA_PATH%\command_line\espeak.exe" -s 100 -v f2 %*
	)
	goto :eof
)

:nircmd
call nircmdc speak text %* -2
if not [%ERRORLEVEL%]==[9009] if not [%ERRORLEVEL%]==[0] goto :eof
REM ERRORLEVEL is 0 if no TTS engine installed

:powershell
PowerShell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('%*');"
if not [%ERRORLEVEL%]==[9009] if not [%ERRORLEVEL%]==[1] goto :eof

:sam
call sam %*
if not [%ERRORLEVEL%]==[9009] goto :eof

REM else
echo %0: no TTS found
exit /b 9009
