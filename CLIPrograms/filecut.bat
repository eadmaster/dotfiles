@echo off
setlocal

REM call execext pdfcut %*
REM if not [%ERRORLEVEL%]==[9009] goto :eof

if [%1]==[] goto arg_error
if [%1]==[-h] goto arg_error
if [%1]==[--help] goto arg_error
if [%1]==[/?] goto arg_error
if [%2]==[] goto arg_error
if not exist %1 goto arg_error

REM syntax: pdftk in.pdf cat 1-12 14-end output out1.pdf
call pdftk %1 cat %2 output "%~n1_cut.pdf" verbose
if not [%ERRORLEVEL%]==[9009] goto :eof

FIRST_PAGE=$(echo $PAGES_RANGE | cut -f1 -d'-')
LAST_PAGE=$(echo $PAGES_RANGE | cut -f2 -d'-')
call gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER -dFirstPage=$FIRST_PAGE -dLastPage=$LAST_PAGE -sOutputFile="$OUTPUTFILE" "$INPUTFILE"
if not [%ERRORLEVEL%]==[9009] goto :eof

imconvert "$INPUTFILE[$PAGES_RANGE]" $OUTPUTFILE
if not [%ERRORLEVEL%]==[9009] goto :eof

REM else
exit /b 9009


:arg_error
echo usage: %0 INPUT.PDF PAGE_RANGE
echo.
echo MEMO: PAGE_RANGE starts from 1
