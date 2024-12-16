@echo off

curl -o NUL "http://servoni.eu/webtests/100mb.test"
if [%ERRORLEVEL%]==[0] goto :eof

curl -o NUL "http://speedtest.sea01.softlayer.com/downloads/test100.zip"
if [%ERRORLEVEL%]==[0] goto :eof

curl -o NUL "http://speedtest.qsc.de/1GB.qsc"
if [%ERRORLEVEL%]==[0] goto :eof

REM more urls: https://raw.githubusercontent.com/blackdotsh/curl-speedtest/master/speedtest.sh


REM ALTERNATIVES:
REM ttcp (req. server) http://en.wikipedia.org/wiki/Ttcp
REM iperf (lin only) https://sourceforge.net/projects/iperf/
REM tcpbench (BSD?)
REM https://github.com/Janhouse/tespeed
REM https://github.com/teeks99/speed_check (in python)
REM pchar http://www.kitchenlab.org/www/bmah/Software/pchar/
REM %~dp0_CANCELLARE\WindowsServer2003-ResourceKitTools-28.04.2003\Linkspeed.exe
REM nirsoft DownTester  http://www.nirsoft.net/utils/download_speed_tester.html

