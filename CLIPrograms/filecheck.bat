@echo off
setlocal

REM file error checking tool by eadmaster

if [%1]==[] goto usage
if [%1]==[-h] goto usage
if [%1]==[--help] goto usage
if [%1]==[/?] goto usage
if not exist %1 goto usage

REM generic file checks
REM chkdsk ...
REM echo.
REM echo suggested safe filename:
REM call detox --dry-run "%~nx1"
REM if %ERRORLEVEL%==? echo "%1" ^(no renaming required^)
REM call detox --dry-run -v "%~nx1"
echo.

REM if exist %*\ goto directory
REM TODO: if it is an hd drive letter -> chkdsk
REM TODO: if it is a cd drive letter -> dvdisaster -d %CD_DRIVE% -s

REM read input file extension
set INPUTEXT=%~x1
if [%INPUTEXT%]==[] set INPUTEXT=.txt
REM convert extension to lowercase
call :LoCase INPUTEXT
REM 2FIX: double extensions: .tar.gz->.tgz, .tar.bz2->.tbz, .tar.lz|lzma->.tlz, ...

REM check if file extension is correct | validate file extension:
REM  NO(IMAGES ONLY, GUI ONLY)? IrfanView
REM  OK? file
echo input file extension: %INPUTEXT%
echo MIME check:
call file -b --mime-type %*
echo.

set CRCEXTLIST=crc crc32 sfv md5 ed2k emulecollection
FOR %%G IN (%CRCEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=rhash -c %*
	REM TODO: cd to file path ?
)

REM if [%INPUTEXT%]==[.par] set TOOL=par v %*
if [%INPUTEXT%]==[.par2] set TOOL=par2 v %*

set PGPEXTLIST=pgp sig asc sign
FOR %%G IN (%PGPEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=gpg --verbose --verify %*
)

if [%INPUTEXT%]==[.exe] set TOOL=sigcheck %*

if [%INPUTEXT%]==[.torrent] (
	REM echo %0: checking files in current dir...
	REM set TOOL=ctorrent -c %*
	set TOOL=aria2 --check-integrity --dry-run %*
	REM TODO: fix https://github.com/aria2/aria2/issues/1525
)

set ARCEXTLIST=zip rar 7z arj bz2 cab cpio gz lha lzh tar tgz tbz wim odt odp odg ods docx pptx xlsx
FOR %%G IN (%ARCEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=7z t -slt %*
)
REM if [%INPUTEXT%]==[.wim] set TOOL=imagex /info %* /check
REM  http://social.technet.microsoft.com/Forums/en/w7itproinstall/thread/d2e4a728-aa89-4515-b4da-e2171d32c814

if [%INPUTEXT%]==[.chd] set TOOL=chdman verify -i %*

set SRCEXTLIST=c cpp h hpp c++ cxx
FOR %%G IN (%SRCEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=lint %*
)
REM if [%INPUTEXT%]==[.php] set TOOL=
if [%INPUTEXT%]==[.java] set TOOL=jlint %*
REM if [%INPUTEXT%]==[.jsp] set TOOL=
REM if [%INPUTEXT%]==[.bat] set TOOL=
REM if [%INPUTEXT%]==[.sh] set TOOL=
if [%INPUTEXT%]==[.py] set TOOL=pylint %*

set XMLEXTLIST=xml sgml xsd xsl opml kml poi wis nzb
FOR %%G IN (%XMLEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=xmllint %*
)

set HTMEXTLIST=html htm shtml
FOR %%G IN (%HTMEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=weblint %*
)

if [%INPUTEXT%]==[.csv] set TOOL="%~dp0csvutils-0.9.3\csvcheck.exe" %*
REM if [%INPUTEXT%]==[.vcf] set TOOL=... -> check if well-formed

REM if [%INPUTEXT%]==[.ttf] set TOOL=C:\CLIPrograms\GnuWin32\bin\ftlint.exe %*

REM if [%INPUTEXT%]==[.dat] set TOOL=datutil ...

REM if [%INPUTEXT%]==[.pdf] set TOOL=pdftk ...

set MEDIAEXTLIST=avi mkv ogm mpg mpeg mp4 mp3 mp2 ogg flac aac ac3 a52 dts asf rm wav
FOR %%G IN (%MEDIAEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=ffmpeg -loglevel error -i %* -f null - ^& echo %0 MEMO: if no error was shown above then the media stream is fine
	REM if [%INPUTEXT%]==[.%%G] set TOOL=mplayer -ao pcm:waveheader:file=NUL %*
	REM if [%INPUTEXT%]==[.%%G] set TOOL=mplayer -benchmark -vo null -vc dummy -ao pcm:fast:file=NUL %*
	REM http://superuser.com/questions/100288/how-to-check-the-integrity-of-a-video-avi-mpeg-file
)

set LOSSLESSAUDIOEXTLIST=flac ape wv tta m4a wav
FOR %%G IN (%LOSSLESSAUDIOEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=ffmpeg -i %1 -acodec pcm_s16le -ar 44100 -f wav "%TEMP%\%~n1.wav" ^& "%~dp0auCDtect-0.8\auCDtect.exe" "%TEMP%\%~n1.wav" ^& del /Q "%TEMP%\%~n1.wav"
	REM if [%INPUTEXT%]==[.%%G] set TOOL=fakeflac %1
	REM todo: fix http://superuser.com/questions/1099758/ffmpeg-piping-to-aucdtect-in-a-batch-file
)

if [%INPUTEXT%]==[.flac] call flac -t %1

set IMAGEEXTLIST=jpg gif png tiff tif bmp xpm pbm pgm ppm tga ico
FOR %%G IN (%IMAGEEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=imconvert %* NUL ^& echo %0 MEMO: if no error was shown above then the image is fine
)

set TXTEXTLIST=txt me 1st log ion lst frm srt ssa ass sub
FOR %%G IN (%TXTEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] (
		call file -b %*
		echo.
		REM TODO: check newlines inconsistency and charset encoding errors
		REM     NO? CheckEOL in http://svn.wxwidgets.org/svn/wx/wxPython/3rdParty/Editra/src/ed_stc.py
		REM     ...
		CHOICE /C YN /M "Want to run spellchecking "
		IF errorlevel 2 goto :eof
		REM else
		echo list of mispelled words: ^& type %* ^| spell -l
		goto :eof
	)
)

set ROMEXTLIST=smc sfc fig gb gbc gba nds n64 z64 smd gen pce nes fds sms gg ws wsc jag ngp ngc vb
FOR %%G IN (%ROMEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=ucon64 %*
)


if not defined TOOL set TOOL=echo %0: unsupported file format: "%INPUTEXT%"

REM echo %0: executing "%TOOL%"
%TOOL%
exit /B %ERRORLEVEL%
REM END OF MAIN


:usage
echo usage: %0 FILE.EXT
exit /B 0

:directory
echo input file is a directory
echo.
goto :eof

:LoCase
:: Subroutine to convert a variable VALUE to all lower case.
:: The argument for this subroutine is the variable NAME.
:: by Jiri http://www.robvanderwoude.com/battech_convertcase.php
FOR %%i IN ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") DO CALL SET "%1=%%%1:%%~i%%"
GOTO:EOF
