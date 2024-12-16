@echo off
setlocal

if [%1]==[] set _HELP=ON
if [%2]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if [%_HELP%]==[ON] (
	REM echo usage: %0 TORRENT_HASH
	echo usage: %0 AUDIFILE1 AUDIOFILE2
	goto :eof
)

REM TODO: add support for more filetypes

set INPUTEXT1=%~x1
set INPUTEXT2=%~x2

if [%INPUTEXT1%]==[.flac] if [%INPUTEXT2%]==[.flac] (
	FOR /F "delims=" %%i IN ('metaflac --show-md5sum %1') DO set HASH1=%%i
	FOR /F "delims=" %%i IN ('metaflac --show-md5sum %2') DO set HASH2=%%i
)

if [%HASH1%]==[] (
	FOR /F "delims=" %%i IN ('ffmpeg -i %1 -f crc - 2^> nul') DO set HASH1=%%i
	FOR /F "delims=" %%i IN ('ffmpeg -i %2 -f crc - 2^> nul') DO set HASH2=%%i
)

if "%HASH1%"=="" (
	FOR /F "delims=" %%i IN ('shntool md5 %1') DO set HASH1=%%i
	FOR /F "delims=" %%i IN ('shntool md5 %2') DO set HASH2=%%i
)

if "%HASH1%"=="" (
	echo %0 error: unable to hash: %1
	exit /b 1
)

echo %0: %1 = %HASH1%
echo %0: %2 = %HASH2%

if "%HASH1%"=="%HASH2%" (
	echo %0: the audio waves are equal
	exit /b 0
) else (
	echo %0: the audio waves are different
	exit /b 1
)
