@echo off

call unix pwgen %*
if not [%ERRORLEVEL%]==[9009] goto :eof

call execext pwgen %*
if not [%ERRORLEVEL%]==[9009] goto :eof

REM ALTERNATIVES:

echo.

call gpg --armor --gen-random 1 32

echo.

call dd if=/dev/random bs=8 count=1 | base64
call dd if=/dev/urandom bs=8 count=1 | base64

echo.

REM sh -c "tr -dc '[:graph:]' < /dev/urandom | head -c ${1:-16}; echo;"

REM echo.

REM unsafe?
REM date /t | md5sum

REM echo.

REM using CryptGenRandom 
REM https://gist.github.com/jbergantine/1119284
REM call python -c "''.join(__import__('random').sample(__import__('string').printable[:62],8))"

REM echo.

REM powershell.exe -command "(1..8 | % { [char](( ('0','9'),('A','Z'),('a','z')) | % { [char]$_[0]..[char]$_[1] } )[(random)%62] }) -join """

echo.

call openssl rand -base64 32

REM mimencode

REM keepass ... http://keepass.info/help/base/cmdline.html

REM  ... http://www.commandlinefu.com/commands/tagged/1903/entropy

