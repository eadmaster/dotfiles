@echo off
setlocal

REM verify valid flac:
REM call fakeflac %1
REM if not [%ERRORLEVEL%]==[0] (
REM     echo %0: err: fake FLAC detected: %1
REM     goto :eof
REM )

REM alternative using ffmpeg (more reliable decoding than lame?) 

call ffmpeg -i %1 -vf scale=300:-1  -xerror -compression_level 0 -aq 0  -metadata encoded_by="eadmaster"  -metadata lyrics-eng=""  %2

REM -vn  : skip attached covers
REM OR: append to existing comment: "encoded with flac2mp3 batch script by eadmaster - old comment follows: ..."
REM more tags: https://gist.github.com/eyecatchup/0757b3d8b989fe433979db2ea7d95a01
REM -ar 44100
REM MEMO: "-xerror" fails on decode error  https://superuser.com/questions/588147/can-i-make-ffmpeg-stop-if-integrity-check-encounters-an-error
REM 2fix: year and comment tag is not copied?

call mp3gain -r -k -T -p %2

goto :eof


REM LAME build using libsndfile is required, download from http://www.rarewares.org
set LAME=call lame.bat
REM set LAME_OPTIONS=--preset insane
REM equals to -m j -V 4 -q 3 -lowpass 20.5
REM ALTERNATIVE:
set LAME_OPTIONS=-V 0 -q 0
REM OLD: set LAME_OPTIONS=-m s -b 320 -q 2
set METAFLAC=%~dp0flac-1.2.1\metaflac.exe

echo.
echo %0 batch script by eadmaster

REM check arguments
if [%1]==[-h] goto help
if [%1]==[--help] goto help
if [%1]==[] goto arg1_err
if not exist %1 goto file_err
REM if [%2]==[] (set OUTFILE=%1) else (set OUTFILE=%2)

REM read tags
FOR /F "delims=" %%i IN ('%METAFLAC% --show-tag=TITLE %1') DO @set %%i
FOR /F "delims=" %%i IN ('%METAFLAC% --show-tag=ARTIST %1') DO @set %%i
FOR /F "delims=" %%i IN ('%METAFLAC% --show-tag=GENRE %1') DO @set %%i
FOR /F "delims=" %%i IN ('%METAFLAC% --show-tag=ALBUM %1') DO @set %%i
FOR /F "delims=" %%i IN ('%METAFLAC% --show-tag=COMMENT %1') DO @set %%i
FOR /F "delims=" %%i IN ('%METAFLAC% --show-tag=DATE %1') DO @set %%i
FOR /F "delims=" %%i IN ('%METAFLAC% --show-tag=TRACKNUMBER %1') DO @set %%i

echo INPUT: %1
echo OUTPUT: %2

REM encode and write tags
%LAME% --noreplaygain --add-id3v2 --tt "%TITLE%" --ta "%ARTIST%" --tg "%GENRE%" --tl "%ALBUM%" --tc "%COMMENT%" --ty "%DATE%" --tn "%TRACKNUMBER%" %LAME_OPTIONS% %1 %2

call mp3gain -r -k -T -p %2

goto :eof

:arg1_err
    echo %0 error: first argument missing
    goto help

:file_err
    echo %0 error: %1 does not exists

:help
    echo.
    echo usage: %0 input.flac [output.mp3]
