@echo off
setlocal

if [%3]==[] (
	REM echo help
	echo usage: shellex ftype NAME COMMAND [ICON_PATH]
	echo special ftyes are: * -^> all files, Unknown -^> unregistered file types, Directory/Folder -^> all directories
	exit /b 0
)

reg add "HKCU\Software\Classes\%1\shell\%~2" /f
reg add "HKCU\Software\Classes\%1\shell\%~2\command" /ve /f /d %3

REM add an icon http://www.winhelponline.com/blog/add-icon-to-right-click-menu-windows-7/
if not [%4]==[] reg add "HKCU\Software\Classes\%1\shell\%~2" /v Icon /f /d %4
