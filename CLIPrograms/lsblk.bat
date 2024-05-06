@echo off

REM call df
REM echo.
mountvol | findstr \
echo.
REM wmic diskdrive list brief
wmic diskdrive get Caption,DeviceID,Model,Partitions
REM wmic diskdrive get bytespersector, caption, DeviceID, InterfaceType, Size
wmic logicaldisk get caption,description,volumename,FileSystem,VolumeDirty
REM wmic partition get BlockSize, Size, Name
echo.
REM echo.
REM MORE ALTERNATIVES:
REM   NO(REQ. ADMIN)? echo LIST Volume | diskpart  http://ss64.com/nt/diskpart.html
REM   ? call smartctl --scan
REM   ? sudo fsutil fsinfo ...
REM   (NOT AVAILABLE)? fdisk /status
REM   NO? listdosdevices http://www.uwe-sieber.de/drivetools_e.html
REM   NO? dosdev http://blogs.msdn.com/b/adioltean/archive/2005/10/04/477164.aspx -> C:\CLIPrograms\_TESTING\MPSReports-tools\x64\dosdev.exe
REM
