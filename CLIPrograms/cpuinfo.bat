@echo off

call unix cat /proc/cpuinfo
call unix cat /proc/stats

echo.

sudo WinSAT features | findstr Processor

echo.

if not defined SYSINTERNALS_PATH call initenv.bat
"%SYSINTERNALS_PATH%\Coreinfo.exe"

echo.

REM wmic cpu list brief /format:list
REM wmic cpu list full
REM wmic cpu get Name,Caption,Manufacturer,L2CacheSize,CurrentClockSpeed,MaxClockSpeed,CurrentVoltage,SocketDesignation /format:textvaluelist
wmic cpu get * /format:textvaluelist
REM see also: wmic MEMCACHE http://ss64.com/nt/wmic.html

echo.

REM TODO: ask to start openhardwaremonitor?
REM call openhardwaremonitor
WMIC /NameSpace:"\\root\OpenHardwareMonitor" path Sensor get Name,Parent,SensorType,Value | findstr cpu

echo.
