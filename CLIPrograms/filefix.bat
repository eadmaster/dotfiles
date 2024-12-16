@echo off
setlocal

if [%1]==[] goto arg_error
if [%1]==[-h] goto arg_error
if [%1]==[--help] goto arg_error
if not exist %1 goto arg_error

if not defined RAMDRIVE call initenv

if exist %*\ goto directory

set INPUTFILE=%1
set INPUTEXT=%~x1
if [%INPUTEXT%]==[] set INPUTEXT=.txt
REM convert extension to lowercase
call :LoCase INPUTEXT

set OUTPUTFILE=%2
if [%OUTPUTFILE%]==[] set OUTPUTFILE="%~n1_FIXED%~x1"

REM WANTED:
REM set IMAGEEXTLIST=jpg gif png tiff tif bmp xpm pbm pgm ppm tga ico
REM FOR %%G IN (%IMAGEEXTLIST%) DO (
REM	if [%INPUTEXT%]==[.%%G] set TOOL=imconvert %1 "%~n1_FIXED%~x1"
REM )

set MEDIAEXTLIST=avi mkv ogm mpg mpeg mp4 mp3 mp2 ogg flac aac ac3 a52 dts asf rm wav ape
FOR %%G IN (%MEDIAEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=ffmpeg -i %INPUTFILE% -c copy %OUTPUTFILE%
	REM alternative syntax:  ffmpeg -i %1 -vcodec copy -acodec copy ...
)

if [%INPUTEXT%]==[.zip] set TOOL=rar r %INPUTFILE%
REM ALTERNATIVE: http://www.neillcorlett.com/zipbit/
if [%INPUTEXT%]==[.rar] set TOOL=rar r %INPUTFILE%
REM if [%INPUTEXT%]==[.7z] set TOOL=???

if [%INPUTEXT%]==[.pdf] set TOOL=pdftk %INPUTFILE% output %OUTPUTFILE%
REM      ALTERNATIVE: java -cp %SYSTEMDRIVE%\CLIPrograms\Multivalent.jar tool.pdf.Repair $*

if [%INPUTEXT%]==[.csv] set TOOL="%~dp0csvutils-0.9.3\csvfix.exe" %1 %OUTPUTFILE%

if [%INPUTEXT%]==[.smc] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --snes --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.sfc] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --snes --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.gba] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --gba --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.nds] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --nds --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.n64] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --n64 --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.z64] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --n64 --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.smd] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --gen --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.gen] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --gen --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.gb]  set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --gb --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.gbc] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --gb --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.pce] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --pce --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.nes] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --nes --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.fds] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --nes --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.sms] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --sms --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.gg]  set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --sms --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.ws]  set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --swan --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.wsc] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --swan --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.jap] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --jag --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.ngp] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --ngp --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.ngc] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --ngp --chk --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.vb]  set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --vboy --chk --nbak %OUTPUTFILE%


if not defined TOOL set TOOL=echo %0: unsupported file format: "%INPUTEXT%"

REM echo %0: executing "%TOOL%"
%TOOL%
exit /B %ERRORLEVEL%
REM END OF MAIN


: arg_error
echo %0: no input file
exit /B 1

:directory
echo input file is a directory
echo.
echo renaming safe filenames:
call detox "%~1\*.*"
echo.
goto :eof

:LoCase
:: Subroutine to convert a variable VALUE to all lower case.
:: The argument for this subroutine is the variable NAME.
:: by Jiri http://www.robvanderwoude.com/battech_convertcase.php
FOR %%i IN ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") DO CALL SET "%1=%%%1:%%~i%%"
GOTO:EOF
