@echo off
setlocal

if [%1]==[] goto arg_error
if [%1]==[/?] goto help
if [%1]==[-h] goto help
if [%1]==[--help] goto help
if not exist %1 goto arg_error
if exist "%~1\" goto arg_error

if not [%2]==[] set OUTPUT_PATH="%2"
if [%2]==[] set OUTPUT_PATH="%~n1"
REM md %OUTPUT_PATH%

REM used in shellext
if [%OUTPUT_PATH%]==["R:"] set OUTPUT_PATH="R:\%~n1"

echo %0: extracting to %OUTPUT_PATH%...

REM read input file extension
set INPUTEXT=%~x1

REM convert extension to lowercase
call :LoCase INPUTEXT

REM 2FIX: double extensions: .tar.gz->.tgz, .tar.bz2->.tbz, .tar.lz|lzma->.tlz, ...

set _7ZEXTLIST=7z zip rar arj iso cab xar pkg 001
REM lzma z taz cpio rpm deb lzh lha chm jar
FOR %%G IN (%_7ZEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=7z x -y -spe -o%OUTPUT_PATH% %1
)

REM set _TAREXTLIST=gz gzip tgz bz2 bzip2 tbz2 tbz tar
REM FOR %%G IN (%_TAREXTLIST%) DO (
REM 	if [%INPUTEXT%]==[.%%G] set TOOL=tar -xf %1
REM )

if [%INPUTEXT%]==[.gz] set TOOL=gzip -d %*
if [%INPUTEXT%]==[.bz2] set TOOL=bzip2 -d %*
if [%INPUTEXT%]==[.lz] set TOOL=lzma -d %*
if [%INPUTEXT%]==[.lzma] set TOOL=lzma -d %*
if [%INPUTEXT%]==[.lzo] set TOOL=lzop -d %*
if [%INPUTEXT%]==[.xz] set TOOL=xz -d %*
if [%INPUTEXT%]==[.lz] set TOOL=lzip -d %*
if [%INPUTEXT%]==[.tgz] set TOOL=tar -xzf %1 -v -C %OUTPUT_PATH%
if [%INPUTEXT%]==[.tbz] set TOOL=tar -xjf %1 -v -C %OUTPUT_PATH%
if [%INPUTEXT%]==[.tb2] set TOOL=tar -xjf %1 -v -C %OUTPUT_PATH%
if [%INPUTEXT%]==[.taz] set TOOL=tar -xZf %1 -v -C %OUTPUT_PATH%
if [%INPUTEXT%]==[.tlz] set TOOL=tar -xaf %1 -v -C %OUTPUT_PATH%
if [%INPUTEXT%]==[.txz] set TOOL=tar -xJf %1 -v -C %OUTPUT_PATH%
REM ... http://en.wikipedia.org/wiki/Tar_(file_format)

REM if [%INPUTEXT%]==[.exe] set TOOL=upx -d %*

if [%INPUTEXT%]==[.pdf] set TOOL=pdfimages -j %* "" ^& pdftotext %* ^& pdfdetach -saveall %*
REM extract fonts too
REM ALTERNATIVE: mupdfextract (from mupdf-tools)

if [%INPUTEXT%]==[.srr] set TOOL=srr -x %1 -o"%OUTPUT_PATH%"

if [%INPUTEXT%]==[.wia] set TOOL=wit copy %1 --fst --psel DATA,-UPDATE,CHANNEL --dest "%OUTPUT_PATH%\%~n1"
if [%INPUTEXT%]==[.wbfs] set TOOL=wit copy %1 --fst --psel DATA,-UPDATE,CHANNEL --preserve --dest "%OUTPUT_PATH%\%~n1"

REM .pea -> C:\PortableApps\UniversalExtractor\bin\pea.exe ...
REM .mkv -> mkvextract tracks $*
REM ? compressed image formats (jpg png gif tif ...) -> .ppm .pgm .pbm
REM ? compressed audio formats (mp3 mp2 ogg flac aac wma rm ...) -> .wav
REM ...

if not defined TOOL goto unknown

REM echo %0: executing "%TOOL%"
call %TOOL%
goto :eof


:unknown
REM try with some generic unpackers

call 7z x -y -spe -o%OUTPUT_PATH% %1
if [%ERRORLEVEL%]==[0] goto :eof

call rar x %1 %OUTPUT_PATH%
[ $? -eq 0 ] && exit 0

"%~d0\PortableApps\UniversalExtractor\UniExtract.exe" %1  %OUTPUT_PATH%
if [%ERRORLEVEL%]==[0] goto :eof

call binwalk --extract --rm --dd='.*' --directory=%OUTPUT_PATH%  %1
if [%ERRORLEVEL%]==[0] goto :eof

call hachoir-subfile %1 %OUTPUT_PATH%
if [%ERRORLEVEL%]==[0] goto :eof

echo.
goto :eof

:arg_error
echo %0: "%1" does not exist
exit /B 1

:help
echo usage: %0 ARCHIVE [TARGET_DIR]
echo.
echo  if TARGET_DIR is not specified extract to a subdir of CWD
echo  if TARGET_DIR does not exist create it
echo.
exit /B 0

:LoCase
:: Subroutine to convert a variable VALUE to all lower case.
:: The argument for this subroutine is the variable NAME.
:: by Jiri http://www.robvanderwoude.com/battech_convertcase.php
FOR %%i IN ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") DO CALL SET "%1=%%%1:%%~i%%"
GOTO:EOF
