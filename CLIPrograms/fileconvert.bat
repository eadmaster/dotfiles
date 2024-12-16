@echo off
setlocal
REM enabledelayedexpansion

REM file converter tool by eadmaster

REM TODO: txt encoding convert, generic binaries encoding convert (base64, etc.)?
if [%1]==[] goto arg_error
if [%2]==[] goto arg_error
if not exist %1 goto arg_error

if not defined RAMDRIVE call initenv

REM if exist %*\ goto directory

set INPUTFILE=%1
set INPUTEXT=%~x1
if [%INPUTEXT%]==[] set INPUTEXT=.txt
set OUTPUTFILE=%2
set OUTPUTEXT=%~x2
set OUTPUTPATH=%~dp2
if [%OUTPUTEXT%]==[] set OUTPUTEXT=.%~n2
if [%OUTPUTEXT%]==[] set "OUTPUTFILE=%~n1.%2"
REM convert extension to lowercase
call :LoCase INPUTEXT
call :LoCase OUTPUTEXT

REM search for a specific converter script
if exist "%~dp0%INPUTEXT:~1%to%OUTPUTEXT:~1%.bat" "%~dp0%INPUTEXT:~1%to%OUTPUTEXT:~1%.bat" %INPUTFILE% %OUTPUTFILE%
if exist "%~dp0%INPUTEXT:~1%2%OUTPUTEXT:~1%.bat" "%~dp0%INPUTEXT:~1%2%OUTPUTEXT:~1%.bat" %INPUTFILE% %OUTPUTFILE%
REM call %INPUTEXT:~1%2%OUTPUTEXT:~1% >NUL 2>&1
REM if not [%ERRORLEVEL%]==[9009] set TOOL="%INPUTEXT:~1%2%OUTPUTEXT:~1%" %INPUTFILE%


set IMAGEEXTLIST=jpg gif png tiff tif bmp xpm pbm pgm ppm tga ico
FOR %%G IN (%IMAGEEXTLIST%) DO (
	REM TODO: single nested if
	if [%INPUTEXT%]==[.%%G] call imconvert %INPUTFILE% %OUTPUTFILE%
	if [%INPUTEXT%]==[.%%G] if not [%ERRORLEVEL%]==[9009] goto :eof
		
	if [%INPUTEXT%]==[.%%G] call ffmpeg -i %INPUTFILE% %OUTPUTFILE%
	if [%INPUTEXT%]==[.%%G] if not [%ERRORLEVEL%]==[9009] goto :eof
		
	if [%INPUTEXT%]==[.%%G] "%~d0\PortableApps\IrfanView\i_view32.exe" %INPUTFILE% /convert=%2 /transpcolor=(0,0,0)
	if [%INPUTEXT%]==[.%%G] if not [%ERRORLEVEL%]==[9009] goto :eof

	if [%INPUTEXT%]==[.%%G] call nircmdc convertimage %INPUTFILE% %OUTPUTFILE%
	if [%INPUTEXT%]==[.%%G] if not [%ERRORLEVEL%]==[9009] goto :eof

	REM MORE ALTERNATIVEs:
	REM  call gimp -i -b ... http://www.gimp.org/tutorials/Basic_Batch/
	REM  "%~dp0OpenImageIO-1.0.8\oiiotool.exe" -v -o %*
	REM  python -c "import pil...
	REM  ...
	REM else
	REM echo %0: err: unable to find any image converter program  1>&2
	REM exit /b 9009
)

if [%INPUTEXT%]==[.dng] set TOOL=dcraw -c %INPUTFILE% ^| imconvert ppm:- %OUTPUTFILE%
if [%INPUTEXT%]==[.crw] set TOOL=dcraw -c %INPUTFILE% ^| imconvert ppm:- %OUTPUTFILE%
REM if [%INPUTEXT%]==[.svg] set TOOL=GIMP ... | inkscape "$*" --without-gui --export-png="$*.png" --export-use-hints
REM if [%OUTPUTEXT%]==[.svg] set TOOL=potrace -s ... | autotrace | inkscape ...
REM if [%INPUTEXT%]==[.wmf] if [%OUTPUTEXT%]==[.svg] set TOOL=unix wmf2svg ...

set MEDIAEXTLIST=avi mkv ogm mpg mpeg mp4 m4a mp3 mp2 ogg flac aac ac3 a52 dts asf rm wav ape tta
FOR %%G IN (%MEDIAEXTLIST%) DO (
	REM bitrate options: -ab ^<fixed bitrate^>k -aq ^<quality/10^>
	if [%INPUTEXT%]==[.%%G] set TOOL=ffmpeg -i %INPUTFILE% %OUTPUTFILE%
	REM ALTERNATIVEs:
	REM  mencoder
	REM  VLC
	REM  sox
)

set _VLC_CODEC=%OUTPUTEXT:~1%
if [%OUTPUTEXT%]==[.wav] set _VLC_CODEC=s16l
if [%OUTPUTEXT%]==[.ogg] set _VLC_CODEC=vorb
REM ...  https://wiki.videolan.org/Codec/#Audio_Codecs
set MODEXTLIST=mod xm s3m stm it mid midi kar vgm nsf spc gbs hes sid
FOR %%G IN (%MODEXTLIST%) DO (
	REM old syntax: issue with filenames with  "[!]" was unexpected at this time.
	REM if [%INPUTEXT%]==[.%%G] set TOOL=vlc -I dummy %INPUTFILE% :no-video :sout=#transcode{acodec=%_VLC_CODEC%}:std{access=file,mux=dummy,dst="%OUTPUTFILE%"} vlc://quit
	if [%INPUTEXT%]==[.%%G] set TOOL=vlc -I dummy %INPUTFILE% --no-video --sout-transcode-acodec=%_VLC_CODEC% ...

	REM ALTERNATIVES:
	REM  NO(REQ. libmodplug patch)? ffmpeg
	REM  (ONLY WRITE AS WAV)? timidity %INPUTFILE% -Ow -o %OUTPUTFILE%
	REM  (MIDI ONLY, ONLY WRITE AS WAV)? set TOOL=fluidsynth -a file ...
	REM  (MIDI SUPPORT REMOVED ON WINDOWS)? vlc ...  https://trac.videolan.org/vlc/ticket/9486
)

set OFFICEEXTLIST=odt odp odg ods doc xls mdb docx pptx xlsx csv tsv dbf txt rtf html htm xhtml md tex rtf text t2t rst
REM   full list: http://dag.wieers.com/home-made/unoconv/
FOR %%G IN (%OFFICEEXTLIST%) DO (
	REM if [%INPUTEXT%]==[.%%G] set TOOL=unoconv -f %OUTPUTEXT:~1% -o %OUTPUTFILE% %INPUTFILE%
	if [%INPUTEXT%]==[.%%G] set TOOL=pandoc -o %OUTPUTFILE% %INPUTFILE%
	REM if [%INPUTEXT%]==[.%%G] set TOOL=loffice --headless --convert-to %OUTPUTEXT:~1% %INPUTFILE%
	REM else try other alternatives
)

set EBOOKEXTLIST=pdf ps eps dvi djvu xps epub mobi azw azw3 azw4 prc pdb chm cbz cbr cb7 lit opf cbc prc
FOR %%G IN (%EBOOKEXTLIST%) DO (
	REM if [%INPUTEXT%]==[.%%G] set TOOL=ebook-convert %INPUTFILE% %OUTPUTFILE%
	if [%INPUTEXT%]==[.%%G] set TOOL=pandoc -o %OUTPUTFILE% %INPUTFILE%	
	REM else try other alternatives
)

set SUBEXTLIST=srt ssa ass sub lrc
FOR %%G IN (%SUBEXTLIST%) DO (
	REM using SubtitleEdit /convert /list  http://www.nikse.dk/SubtitleEdit/Help#commandline
	if [%INPUTEXT%]==[.%%G] set TOOL=call SubtitleEdit.bat /convert %INPUTFILE% %OUTPUTEXT:~1%  /outputfolder:%OUTPUTPATH%
)

set HDIEXTLIST=img ima vhd vmdk qcow qcow2
FOR %%G IN (%HDIEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=qemu-img convert %INPUTFILE% %OUTPUTFILE%
)

set CDIEXTLIST=bin cue nrg mdf pdi cdi b5i iso
FOR %%G IN (%CDIEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G] set TOOL=iat -i %INPUTFILE% -o %OUTPUTFILE%
)

set ARCEXTLIST=zip rar 7z arj bz2 cab cpio gz lha lzh tar tgz tbz wim
FOR %%G IN (%ARCEXTLIST%) DO (
	REM if [%INPUTEXT%]==[.%%G] (
	if [%INPUTEXT%]==[.%%G] if not exist "%TEMP%\%~n1" (
		REM echo make sure there is enought space in "%TEMP%" to extract the input archive & pause
		md "%TEMP%\%~n1" 
		call 7z x %INPUTFILE% -o"%TEMP%\%~n1" 
	)
	
	if [%INPUTEXT%]==[.%%G] if [%OUTPUTEXT%]==[.chd] (
		if exist "%TEMP%\%~n1\%~n1.cue" call chdman createcd -i "%TEMP%\%~n1\%~n1.cue" -o %OUTPUTFILE%
		rd /S /Q  "%TEMP%\%~n1"
		goto :eof
	)
	
	if [%INPUTEXT%]==[.%%G] if [%OUTPUTEXT%]==[.wia] (
		if exist "%TEMP%\%~n1\game.iso" call wit COPY "%TEMP%\%~n1\game.iso" --wia=DEFAULT --long --prealloc=OFF --compression=FAST %OUTPUTFILE%
		rd /S /Q  "%TEMP%\%~n1"
		goto :eof
	)

	REM else
	REM TODO: check if output ext in ARCEXTLIST
	REM TODO: keep comments, original attibutes, etc.
	REM call 7z a -r %OUTPUTFILE% "%TEMP%\%~n1\*" "%TEMP%\%~n1\*.*"
	REM rd /S /Q  "%TEMP%\%~n1"
	REM goto :eof
)

REM point of interests: ov2 kml gpx poi -> http://www.gpsbabel.org
REM    gpsbabel [options] -i INTYPE -f INFILE -o OUTTYPE -F OUTFILE
REM  http://wiki.openstreetmap.org/wiki/Using_GPSBabel_from_the_command_line

if [%INPUTEXT%]==[.mid] if [%OUTPUTEXT%]==[.wav] set TOOL=timidity %INPUTFILE% -Ow -o %OUTPUTFILE%
if [%INPUTEXT%]==[.mod] if [%OUTPUTEXT%]==[.wav] set TOOL=timidity %INPUTFILE% -Ow -o %OUTPUTFILE%

REM databases file format
if [%INPUTEXT%]==[.db] if [%OUTPUTEXT%]==[.sql] set TOOL=sqlite3 %INPUTFILE% .dump ^> %OUTPUTFILE%
if [%INPUTEXT%]==[.db3] if [%OUTPUTEXT%]==[.sql] set TOOL=sqlite3 %INPUTFILE% .dump ^> %OUTPUTFILE%
REM if [%INPUTEXT%]==[.db] if [%OUTPUTEXT%]==[.csv] set TOOL=sqlite3 %INPUTFILE% .dump ^> %OUTPUTFILE%

REM if [%INPUTEXT%]==[.pdf] if [%OUTPUTEXT%]==[.png] set TOOL=pdf2png %INPUTFILE%
REM if [%INPUTEXT%]==[.pdf] if [%OUTPUTEXT%]==[.jpg] set TOOL=pdf2jpg %INPUTFILE%
if [%INPUTEXT%]==[.pdf] if [%OUTPUTEXT%]==[.djvu] set TOOL=pdf2djvu %INPUTFILE% --verbose --loss-level=0 --guess-dpi -o %OUTPUTFILE%
if [%INPUTEXT%]==[.pdf] if [%OUTPUTEXT%]==[.ps] set TOOL=pdf2ps %INPUTFILE% %OUTPUTFILE%
if [%INPUTEXT%]==[.pdf] if [%OUTPUTEXT%]==[.txt] set TOOL=pdftotext %INPUTFILE% %OUTPUTFILE%
if [%INPUTEXT%]==[.pdf] if [%OUTPUTEXT%]==[.htm] set TOOL=pdftohtml %INPUTFILE% %OUTPUTFILE%
if [%INPUTEXT%]==[.pdf] if [%OUTPUTEXT%]==[.html] set TOOL=pdftohtml %INPUTFILE% %OUTPUTFILE%
if [%INPUTEXT%]==[.ps] if [%OUTPUTEXT%]==[.pdf] set TOOL=ps2pdf %INPUTFILE% %OUTPUTFILE%
if [%INPUTEXT%]==[.tex] if [%OUTPUTEXT%]==[.pdf] set TOOL=pdflatex %INPUTFILE% %OUTPUTFILE%
REM if [%INPUTEXT%]==[.svg] if [%OUTPUTEXT%]==[.ico] set TOOL=svg2ico %INPUTFILE%
REM if [%INPUTEXT%]==[.svg] if [%OUTPUTEXT%]==[.png] set TOOL=svg2png %INPUTFILE%

REM img2txt=ocr $*

REM if [%INPUTEXT%]==[.jpg] if [%OUTPUTEXT%]==[.tiff] set TOOL=TiffToy ?
REM if [%INPUTEXT%]==[.jpg] if [%OUTPUTEXT%]==[.tif] set TOOL=TiffToy ?
if [%INPUTEXT%]==[.jpg] if [%OUTPUTEXT%]==[.pdf] set TOOL=img2pdf %INPUTFILE% -o %OUTPUTFILE%

if [%INPUTEXT%]==[.dot] set TOOL=dot -o %OUTPUTFILE% -T%OUTPUTEXT% %INPUTFILE%

REM gen<->smd roms
if [%INPUTEXT%]==[.gen] if [%OUTPUTEXT%]==[.smd] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --gen --smd --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.bin] if [%OUTPUTEXT%]==[.smd] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --gen --smd --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.smd] if [%OUTPUTEXT%]==[.bin] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --gen --bin --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.smd] if [%OUTPUTEXT%]==[.gen] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --gen --bin --nbak %OUTPUTFILE% ^& del /F /Q %OUTPUTFILE%
REM smc<->sfc roms
REM TODO: check if Backup unit/emulator header: No -> many .smc roms are missing the header already and stripping will produce a broken ROM  http://romhack.wikia.com/wiki/SMC_header
REM if [%INPUTEXT%]==[.smc] if [%OUTPUTEXT%]==[.sfc] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --snes --stp --nbak %OUTPUTFILE%
if [%OUTPUTEXT%]==[.smc] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --snes --smc --nbak %OUTPUTFILE%
REM tg<->pce roms
if [%INPUTEXT%]==[.tg] if [%OUTPUTEXT%]==[.pce] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --pce --swap --nbak %OUTPUTFILE%
if [%INPUTEXT%]==[.pce] if [%OUTPUTEXT%]==[.tg] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --pce --swap --nbak %OUTPUTFILE%
REM n64<->z64... roms

REM wia<->wbfs Wii ISOs (MEMO: OUTPUTFILE must be a dir)
REM if [%INPUTEXT%]==[..wia|wbfs|iso] 
if [%OUTPUTEXT%]==[.wbfs]  set TOOL=wit COPY %INPUTFILE% --wbfs --split %OUTPUTFILE%
REM TODO: handle FST dir conversion: (remove the "\" suffix in INPUTFILE)
if [%OUTPUTEXT%]==[.wia] set TOOL=wit COPY %INPUTFILE% --wia=DEFAULT --psel DATA,-UPDATE,CHANNEL --long --prealloc=OFF --compression=FAST %OUTPUTFILE%
if [%OUTPUTEXT%]==[.gcz] set TOOL=wit COPY %INPUTFILE% --gcz --psel DATA,-UPDATE,CHANNEL --long %OUTPUTFILE%
if [%OUTPUTEXT%]==[.ciso] set TOOL=wit COPY %INPUTFILE% --ciso --psel DATA,-UPDATE,CHANNEL --long %OUTPUTFILE%
REM FST->wbfs: dirname must not include spaces to avoid cygwin errors
if [%INPUTEXT%]==[.wia] if [%OUTPUTEXT%]==[.iso] set TOOL=wit COPY %INPUTFILE%  %OUTPUTFILE%
if [%INPUTEXT%]==[.gcz] if [%OUTPUTEXT%]==[.iso] set TOOL=wit COPY %INPUTFILE%  %OUTPUTFILE%

REM WANTED:: wbfs->rvz
if [%OUTPUTEXT%]==[.rvz] set TOOL=C:\PortableApps\Dolphin\DolphinTool.exe convert -i %INPUTFILE% -f rvz --block_size=131072 --compression=zstd --compression_level=5 -o %OUTPUTFILE%

REM iso<->cso conversion with CisoPlus http://cisoplus.pspgen.com/
if [%INPUTEXT%]==[.iso] if [%OUTPUTEXT%]==[.cso] set TOOL=cisoplus -com -opt -l6 -t90 -rm_update  %INPUTFILE% %OUTPUTFILE% 
if [%INPUTEXT%]==[.cso] if [%OUTPUTEXT%]==[.iso] set TOOL=cisoplus -dec  %INPUTFILE% %OUTPUTFILE% 
REM with maxcso  https://github.com/unknownbrackets/maxcso/
REM if [%INPUTEXT%]==[.cso] if [%OUTPUTEXT%]==[.iso] set TOOL=maxcso  %INPUTFILE% -o %OUTPUTFILE% 

REM dir->xiso conversion with extract-xiso  https://github.com/XboxDev/extract-xiso
if [%OUTPUTEXT%]==[.xiso]  set TOOL=extract-xiso -c %INPUTFILE% %OUTPUTFILE% 

REM 3DS<->CIA
if [%OUTPUTEXT%]==[.cia] set TOOL=3dsconv --output=%OUTPUTPATH%  %INPUTFILE%

REM Wiiu rpx<->elf
if [%OUTPUTEXT%]==[.rpx] set TOOL=wiiurpxtool -c %INPUTFILE% %OUTPUTFILE%
if [%INPUTEXT%]==[.rpx] set TOOL=wiiurpxtool -d %INPUTFILE% %OUTPUTFILE%

REM savegames conversion
if [%INPUTEXT%]==[.gcs] if [%OUTPUTEXT%]==[.gci] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --nbak --stpn=272 %OUTPUTFILE%
REM ALTERNATIVE: if [%INPUTEXT%]==[.gcs] if [%OUTPUTEXT%]==[.gci] set TOOL=dd if=%INPUTFILE% of=$1.gci bs=1 skip=272
REM ...
REM if [%INPUTEXT%]==[.duc] if [%OUTPUTEXT%]==[.sav] set TOOL=firefox http://shunyweb.info/convert.php
REM if [%INPUTEXT%]==[.dss] if [%OUTPUTEXT%]==[.sav] set TOOL=firefox http://shunyweb.info/convert.php
REM if [%INPUTEXT%]==[.cbs] set TOOL=mymc memcard.ps2 import %INPUTFILE% ; mymc memcard.ps2 export %OUTPUTFILE%
REM if [%INPUTEXT%]==[.max] set TOOL=mymc memcard.ps2 import %INPUTFILE% ; mymc memcard.ps2 export %OUTPUTFILE%
REM if [%INPUTEXT%]==[.psu] set TOOL=mymc memcard.ps2 import %INPUTFILE% ; mymc memcard.ps2 export %OUTPUTFILE%
REM if [%OUTPUTEXT%]==[.psu] set TOOL=mymc memcard.ps2 format ; mymc memcard.ps2 import %INPUTFILE% ; mymc memcard.ps2 export %GAME_CODE%
if [%OUTPUTEXT%]==[.ps2] set TOOL=call mymc %OUTPUTFILE% format ^& call mymc %OUTPUTFILE% import %INPUTFILE%
REM if [%INPUTEXT%]==[.mcr] set TOOL=MemcardRex ...
REM if [%OUTPUTEXT%]==[.mcr] set TOOL=MemcardRex ...
if [%INPUTEXT%]==[.gme] if [%OUTPUTEXT%]==[.mcr] set TOOL=copy %INPUTFILE% %OUTPUTFILE% ^& ucon64 --nbak --stpn=3904 %OUTPUTFILE%
REM if [%INPUTEXT%]==[.mcs] set TOOL=MemcardRex ...
REM if [%INPUTEXT%]==[.psx] set TOOL=MemcardRex ...

REM no conversion needed, simply copy
if [%INPUTEXT%]==[.sps] if [%OUTPUTEXT%]==[.xps] set TOOL=copy %INPUTFILE% %OUTPUTFILE%
if [%INPUTEXT%]==[.xps] if [%OUTPUTEXT%]==[.sps] set TOOL=copy %INPUTFILE% %OUTPUTFILE%

REM convert N64 .eep, .mpk, .sra, .fla <-> libretro srm
REM if [%INPUTEXT%]==[.srm] set TOOL=pj64tosrm %INPUTFILE%
REM if [%OUTPUTEXT%]==[.srm] set TOOL=pj64tosrm %INPUTFILE%

REM TODO: PS2, PSX savegames conversion

if [%INPUTEXT%]==[.bin] if [%OUTPUTEXT%]==[.iso] set TOOL=%~dp0cmdpack-1.03\bin2iso.exe  %INPUTFILE% %OUTPUTFILE%

REM TODO: fixare errors with 
if [%OUTPUTEXT%]==[.chd] set TOOL=chdman createcd -i %INPUTFILE% -o %OUTPUTFILE%
REM --compression cdzl 
if [%INPUTEXT%]==[.chd] if [%OUTPUTEXT%]==[.cue] set TOOL=chdman extractcd -i %INPUTFILE% -o %OUTPUTFILE%

if [%INPUTEXT%]==[.ecm] set TOOL="%~dp0cmdpack-1.03\unecm.exe" %INPUTFILE% %OUTPUTFILE%

if [%OUTPUTEXT%]==[.txt] set TOOL=file2txt %INPUTFILE% %OUTPUTFILE%

if not defined TOOL set TOOL=echo %0: err: unsupported file formats conversion: %INPUTEXT% -^> %OUTPUTEXT%   1>&2

echo %0: converting %INPUTFILE% -^> %OUTPUTFILE%  1>&2
echo %0: executing "%TOOL%"
%TOOL%
exit /B %ERRORLEVEL%
REM END OF MAIN


: arg_error
echo syntax: %0 INPUT_FILE OUTPUT_FILE^|EXT
echo.
exit /B 1

:LoCase
:: Subroutine to convert a variable VALUE to all lower case.
:: The argument for this subroutine is the variable NAME.
:: by Jiri http://www.robvanderwoude.com/battech_convertcase.php
FOR %%i IN ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") DO CALL SET "%1=%%%1:%%~i%%"
GOTO:EOF
