@echo off
setlocal

echo %0: local (system):
echo %date% %time%
REM date /t
REM time/t

echo.

echo %0: local (unix timestamp):
call busybox date +%%%%s

echo.

echo %0: local (locale format):
call busybox date

echo.

echo %0: local (ISO 8601 format):
call busybox date +%%%%Y-%%%%m-%%%%dT%%%%H:%%%%M:%%%%S%%%%z

echo.

echo %0: local (hardware):
call unix hwclock -r

echo.

set TZ=America/New_York
echo %0: %TZ% time:
call unix date

echo.

set TZ=Asia/Tokyo
echo %0: %TZ% time:
call unix date

set TZ=

echo .

echo %0: local remote:
call unix rdate -p time.nist.gov
if [%ERRORLEVEL%]==[0] goto :eof
call unix rdate -p tick.greyware.com
if [%ERRORLEVEL%]==[0] goto :eof
call unix rdate -p rdate.cpanel.net
if [%ERRORLEVEL%]==[0] goto :eof
