@echo off
setlocal

if [%1]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[--help] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if [%_HELP%]==[ON] (
	echo usage: %0 romname
	goto :eof
)

REM set MAME_ROMS_SITE=
REM ALTERNATIVES: 

REM from archive.org (MEMO: no server date->unable to download newer files only)
REM call wget -N "https://archive.org/download/mame-merged/mame-merged/%1.zip"
call curl --fail --remote-time --time-cond "%1.zip" "https://archive.org/download/mame-merged/mame-merged/%1.zip" -o "%1.zip"

goto :eof

REM md R:\new_mame
REM copy %1.zip R:\new_mame\
REM goto :eof

md R:\new_mame\samples
md R:\new_mame\artwork

REM try to download the samples
call wget -N -U firefox http://samples.mameworld.info/wav/%1.zip -O ..\samples\%1.zip
if not %ERRORLEVEL%==0 del /F /Q ..\samples\%1.zip
copy ..\samples\%1.zip R:\new_mame\samples\

REM try to download the artworks
call wget -N -U firefox http://mrdo.mameworld.info/artwork/%1.zip -O ..\artwork\%1.zip
if not %ERRORLEVEL%==0 del /F /Q ..\artwork\%1.zip
copy ..\artwork\%1.zip R:\new_mame\artwork\

REM create a launcher and download a screenshot
call mamesnapget %1
copy %1.png R:\new_mame\
move %1.png ..\snap\
echo mame %1 > "R:\new_mame\%1 () ().bat"
copy %1.zip R:\new_mame\

REM TODO: download chd if necessary...
REM  http://bda.retroroms.net/downloads/mame/CHDs-outdated/