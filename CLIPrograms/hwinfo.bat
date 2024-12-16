@echo off

call cpuinfo

call gpuinfo

echo RAM:
wmic MEMORYCHIP get Capacity,DeviceLocator,BankLabel,Speed,PartNumber,Manufacturer
REM %CYGWIN_HOME%\bin\cat.exe /proc/meminfo

REM biosinfo
systeminfo | findstr BIOS

call openhardwaremonitor
WMIC /NameSpace:"\\root\OpenHardwareMonitor" path Hardware get HardwareType,Name

REM list temperatures
call sensors

REM list other devices
call devcon find *

REM TODO: list Windows performance counters  https://blogs.msdn.microsoft.com/powershell/2009/04/21/v2-quick-tip-monitoring-performance-counters-with-powershell/
REM powershell -Command "Get-Counter –listSet * | Select-Object -ExpandProperty Paths"
