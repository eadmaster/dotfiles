@echo off

winsat features

echo.

call openhardwaremonitor
WMIC /NameSpace:"\\root\OpenHardwareMonitor" path Sensor get Name,Parent,SensorType,Value | findstr gpu

echo.
