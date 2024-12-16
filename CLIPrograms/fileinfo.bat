@echo off
setlocal

REM file info tool by eadmaster
REM display file information using external tools

if [%1]==[] goto usage
if [%1]==[-h] goto usage
if [%1]==[--help] goto usage
if [%1]==[/?] goto usage
if not exist %1 goto usage

REM show generic file infos
REM call stat %*
REM echo.

REM if exist %*\ goto directory

REM read input file extension
set INPUTEXT=%~x1
if [%INPUTEXT%]==[] set INPUTEXT=.txt

REM convert extension to lowercase
call :LoCase INPUTEXT

set IMAGEEXTLIST=jpg gif png tiff tif bmp xpm pbm pgm ppm tga ico
if not defined MAGICK_HOME call initenv.bat
FOR %%G IN (%IMAGEEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=%MAGICK_HOME%\identify %* ^& exiftool %*
)
if [%INPUTEXT%]==[.jpg] set TOOL=%TOOL% ^& exiftool %*
if [%INPUTEXT%]==[.tiff] set TOOL=%TOOL% ^& unix tiffinfo %*
if [%INPUTEXT%]==[.tif] set TOOL=%TOOL% ^& unix tiffinfo %*

if [%INPUTEXT%]==[.dng] set TOOL=dcraw -i -v %* ^& exiftool %*
if [%INPUTEXT%]==[.crw] set TOOL=dcraw -i -v %*

set MEDIAEXTLIST=avi mkv m2v ogm mpg mpeg mp4 m4a mp3 mp2 ogg oga flac aac ac3 a52 dts asf rm wav wma m4a ape aiff au opus amr spx mod xm s3m stm it 3gp act mpc ra rm tta vox wv
FOR %%G IN (%MEDIAEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=call ffprobe -hide_banner -v error -show_format -show_streams %* ^& call exiftool %* ^& call mediainfo %*
)
REM if [%INPUTEXT%]==[.mid] set TOOL=timidity %* -Ol
REM if [%INPUTEXT%]==[.sf2] set TOOL=???

REM if [%INPUTEXT%]==[.mp3] set TOOL=%TOOL% ^& encspot %*
REM if [%INPUTEXT%]==[.mkv] set TOOL=%TOOL% ^& mkvmerge -i %*

if [%INPUTEXT%]==[.swf] set TOOL=swfdump %*

if [%INPUTEXT%]==[.pdf] set TOOL=pdfinfo %*
if [%INPUTEXT%]==[.djv] set TOOL=djvudump %*
if [%INPUTEXT%]==[.djvu] set TOOL=djvudump %*
if [%INPUTEXT%]==[.epub] set TOOL=ebook-meta %*

if [%INPUTEXT%]==[.exe] set TOOL=sigcheck -q -a %* ^& ldd %*
if [%INPUTEXT%]==[.dll] set TOOL=sigcheck -q -a %* ^& ldd %*
REM   ALTERNATIVES: exelist, filever /V %* (from WindowsXPSP2-SupportTools), SignTool (part of the Windows SDK), perdr -h %*, NO? sfk version ... http://stahlworks.com/dev/index.php?tool=version

REM if [%INPUTEXT%]==[.x86] set TOOL=readelf/elfdump... %*
REM if [%INPUTEXT%]==[.elf] set TOOL=readelf/elfdump... %*

REM if [%INPUTEXT%]==[.lnk] set TOOL=nircmd ...
REM if [%INPUTEXT%]==[.url] set TOOL=nircmd ...

set DISKEXTLIST=img ima vhd vmdk qcow qcow2
FOR %%G IN (%DISKEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=qemu-img info %*
)

if [%INPUTEXT%]==[.iso] set TOOL=isoinfo -d -i %*
if [%INPUTEXT%]==[.chd] set TOOL=chdman info -i %*
REM ALTERNATIVE: http://sourceforge.net/p/disktype/

set FONTEXT=ttf ttc otf pfa pfb
FOR %%G IN (%FONTEXT%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=unix ftdump -n %*
)

REM if [%INPUTEXT%]==[.torrent] set TOOL=ctorrent -x %*
if [%INPUTEXT%]==[.torrent] set TOOL=aria2 --dry-run=true --show-files=true %*

set ARCEXTLIST=zip rar 001 7z arj bz2 cab cpio gz lha lzh tar tgz tbz
REM wim
FOR %%G IN (%ARCEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=7z l -slt %*
)

REM if [%INPUTEXT%]==[.wim] set TOOL=imagex /info %*
if [%INPUTEXT%]==[.wim] set TOOL=dism /Get-ImageInfo /ImageFile:%*

REM if [%INPUTEXT%]==[.par] set TOOL=par l %*
if [%INPUTEXT%]==[.par2] set TOOL=par2 l %*

if [%INPUTEXT%]==[.srr] set TOOL=srr -l %*

REM TODO: DEB, RPM -> print description, files included, dependencies

set ROMEXTLIST=smc sfc fig gb gbc gba nds n64 z64 smd gen md 32x pce nes fds sms gg ws wsc jag ngp ngc vb
FOR %%G IN (%ROMEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=ucon64 %*
)

REM if [%INPUTEXT%]==[.diff] set TOOL=??? %*
REM if [%INPUTEXT%]==[.ips] set TOOL=ucon64 %*
REM if [%INPUTEXT%]==[.aps] set TOOL=ucon64 %*
if [%INPUTEXT%]==[.ppf] set TOOL=file %*
REM if [%INPUTEXT%]==[.ups] set TOOL=...
if [%INPUTEXT%]==[.xdelta] set TOOL=xdelta3 printhdr %*


if [%INPUTEXT%]==[.gcm] set TOOL=gcmtool %*
if [%INPUTEXT%]==[.gci] (
	echo|set /p=game code and name: 
	head -c 6 %*
	echo.
	head -c 6 %* | grep -f - "%PENDRIVE%\Documents\db\vg\wiitdb_titles.txt"
	REM if [%ERRORLEVEL%]==[1] head -c 6 %* && echo  ^(not found in wiitdb^)
	echo|set /p=region: 
	hex %* 3
	echo  ^(MEMO: 0x50=PAL, 0x45=USA, 0x??=JAP^)
	echo|set /p=protection check: 
	hex %* 0x34
	echo  ^(MEMO: 0x1C=protected, 0x04=not protected^)
	goto :eof
)

if [%INPUTEXT%]==[.psu] (
	echo|set /p=game code and name:
	REM grep -m 1 B.SC..- %* | dd skip=2 count=10 bs=1 2>NUL | zzfind "P:\Documents\db\vg\Sony Index.zip" - <- stdin not supported?  https://sourceforge.net/p/swissfileknife/support-requests/3/
	grep -m 1 B.SC..- %* | dd skip=2 count=10 bs=1 2>NUL
	echo.
	grep -m 1 B.SC..- %* | dd skip=2 count=10 bs=1 2>NUL | findsony -f -
	REM if %ERRORLEVEL%==1 echo ^(not found in Sony Index^)
	goto :eof
)

if [%INPUTEXT%]==[.crt] set TOOL=openssl x509 -text -pubkey -fingerprint -in %*
if [%INPUTEXT%]==[.cer] set TOOL=openssl x509 -text -pubkey -fingerprint -in %*
if [%INPUTEXT%]==[.pem] set TOOL=openssl x509 -text -pubkey -fingerprint -noout -in %*
if [%INPUTEXT%]==[.der] set TOOL=openssl x509 -text -pubkey -fingerprint -inform DER -in %*
if [%INPUTEXT%]==[.p7b] set TOOL=openssl pkcs7 -text -inform DER -print_certs -in %*
if [%INPUTEXT%]==[.p12] set TOOL=openssl pkcs12 -in %*

set PGPEXTLIST=pgp sig asc
FOR %%G IN (%PGPEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=gpg --verbose --dry-run %*
)

set TXTEXTLIST=txt me 1st log ion lst frm srt ssa ass sub
FOR %%G IN (%TXTEXTLIST%) DO (
	REM output file encoding+EOL type
	if [%INPUTEXT%]==[.%%G] set TOOL=file -b %*
)

REM set SQLITEEXTLIST=sqlite -> echo .schema | sqlite3 %*

REM set JSONEXTLIST=json rjson


REM if not defined TOOL set TOOL=file %* ^& file -b -i %*
REM if not defined TOOL set TOOL=echo %0: no specific file format info tool found
if not defined TOOL goto unknown

REM echo %0: executing "%TOOL%"
%TOOL%
exit /B %ERRORLEVEL%
REM END OF MAIN

:usage
echo usage: %0 INPUT_FILE
exit /B 1

:unknown
echo.
REM echo file header:
REM hexdump -n 200 %* | head
REM echo.

echo|set /p=MIME type: 
call file -b --mime-type %*
echo|set /p=file description: 
call file -b %*
echo.
call exiftool.bat %*
echo.
REM REM  "C:\CLIPrograms\_TESTING\libextractor-1.0.0\bin\extract.exe" %*
call extract %*
echo.
call hachoir-metadata %*
echo.
REM https://github.com/apache/tika
call tika --text --metadata  %*
echo.
REM https://github.com/wader/fq/
fq . %*
echo.

REM if %~z1 GTR 100000000 (
REM	CHOICE /C YN /M "File is bigger than 100MB, proceed with the analisys "
REM	IF errorlevel 2 goto :eof
REM )

REM set _ANSWER=n
REM SET /P _ANSWER="search subfiles [Y,N]? "
REM echo.
REM call binwalk --signature %*
REM call hachoir-subfile %*

REM :ascii
REM SET /P _ANSWER=extract ASCII strings? 
REM IF [%_ANSWER%]==[n] goto entropy
REM IF [%_ANSWER%]==[N] goto entropy
REM echo.
REM strings %*
REM echo|set /p=ASCII strings lenght (in bytes): 
REM strings %* | wc -c
REM echo.

REM :hash
REM set _ANSWER=n
REM SET /P _ANSWER="compute hashes [Y,N]? "
REM REM if %~z1 GTR 100000000 SET /P _ANSWER="file is bigger than 100MB, compute hashes [Y,N]? "
REM IF [%_ANSWER%]==[n] goto :eof
REM IF [%_ANSWER%]==[N] goto :eof
REM call hash %*
REM echo.

REM :entropy
REM set _ANSWER=n
REM SET /P _ANSWER="compute entropy [yN]? "
REM if %~z1 GTR 100000000 SET /P _ANSWER="file is bigger than 100MB, compute entropy [Y,N]? "
REM empty answer=leave variable unchanged
REM IF [%_ANSWER%]==[n] goto hash
REM IF [%_ANSWER%]==[N] goto hash
REM call ent %* | head -n4
echo.
goto :eof

:directory
echo %0: input file is a directory
REM dir
echo.
if exist file_id.diz type file_id.diz
echo.
if exist descript.ion type descript.ion
goto :eof


:LoCase
:: Subroutine to convert a variable VALUE to all lower case.
:: The argument for this subroutine is the variable NAME.
:: by Jiri http://www.robvanderwoude.com/battech_convertcase.php
FOR %%i IN ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") DO CALL SET "%1=%%%1:%%~i%%"
GOTO:EOF
