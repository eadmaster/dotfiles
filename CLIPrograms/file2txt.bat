@echo off
setlocal

set INPUTEXT=%~x1

REM 2FIX: double extensions: .tar.gz->.tgz, .tar.bz2->.tbz, .tar.lz|lzma->.tlz, ...


set ARCEXTLIST=zip rar 001 7z
REM wim  arj bz2 cab cpio gz lha lzh tar tgz tbz
FOR %%G IN (%ARCEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G]  7z e -so %1 2>NUL | tee
	REM http://superuser.com/questions/148498/7zip-how-to-extract-to-std-output
)

set IMAGEEXTLIST=jpg gif png tiff tif bmp xpm pbm pgm ppm tga ico
FOR %%G IN (%IMAGEEXTLIST%) DO (
	if [%INPUTEXT%]==[.%%G]  tesseract %1 stdout
	REM TODO: try more OCRs
)

if [%INPUTEXT%]==[.gz] gzip -dc %*
if [%INPUTEXT%]==[.bz2] bzip2 -dc %*
if [%INPUTEXT%]==[.lz] lzma -dc %*
if [%INPUTEXT%]==[.lzma] lzma -dc %*
if [%INPUTEXT%]==[.lzo] lzop -dc %*
if [%INPUTEXT%]==[.xz] xz -dc %*
if [%INPUTEXT%]==[.lz] lzip -dc %*

if [%INPUTEXT%]==[.hi] "%~dp0hi2txt-1.10\hi2txt.exe" -ra %*

if [%INPUTEXT%]==[.json] python -m json.tool  %*
REM if [%INPUTEXT%]==[.json] jq .  %*

if [%INPUTEXT%]==[.xml] xml fo %*

if [%INPUTEXT%]==[.html] pandoc -f html -t plain  %*

if [%INPUTEXT%]==[.pdf] pdftotext %*

if [%INPUTEXT%]==[.rdf] loffice --cat --headless %*

REM try with tika (lot of supported formats) https://github.com/apache/tika
call tika --text %*

REM else
echo %0 err: unsupported file type: %INPUTEXT%
