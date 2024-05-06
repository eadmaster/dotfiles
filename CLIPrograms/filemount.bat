@echo off
setlocal

if [%1]==[] (
	call lsblk
	goto :eof
)

REM read input file extension
set INPUTEXT=%~x1
call :LoCase INPUTEXT

REM detect and mount compressed archives
REM http://www.winmount.com/command.html
REM if [%INPUTEXT%]==[.zip] if exist "%PROGRAMFILES%\WinMount\WinMount.exe" set TOOL=start "" "%PROGRAMFILES%\WinMount\WinMount.exe" -m %*
REM if [%INPUTEXT%]==[.rar] if exist "%PROGRAMFILES%\WinMount\WinMount.exe" set TOOL=start "" "%PROGRAMFILES%\WinMount\WinMount.exe" -m %*

REM WIM images (mount in a subfolder)
set MOUNTPATH=%~n1
REM MOUNTPATH must reside on NTFS
if [%INPUTEXT%]==[.wim] (
	mkdir "%MOUNTPATH%"
	REM if exist "%PROGRAMFILES%\Windows AIK\Tools\..."
	REM set TOOL=imagex /MOUNTRW %* 1 %FILENAME%
	set TOOL=dism /Mount-Image /ImageFile:%* /Name:"%~n1" /MountDir:"%MOUNTPATH%" /Optimize 2> NUL
	REM  internal image name must match the filename
)

REM HD images
set _HD_IMAGES_EXT_LIST=vhd vdi vmdk
FOR %%G IN (%_HD_IMAGES_EXT_LIST%) DO (
	if [%INPUTEXT%]==[.%%G] (
		if exist "%WinDir%\system32\imdisk.exe" set TOOL=imdisk -a -t file -f %* -o hd,rw -m #:
		REM ^& start "" C:\WINDOWS\system32\imdisk.cpl
		if exist "%PROGRAMFILES%\WinMount\WinMount.exe" set TOOL=start "" "%PROGRAMFILES%\WinMount\WinMount.exe" -m %*
	)
)

REM detect and mount CD images
REM http://www.daemon-help.com/en/windows_integration_lite/command_line_parameters.html
set _CD_IMAGES_EXT_LIST=iso isz nrg mdf mds ccd cdi bin cue
REM b5t b6t bwt pdi
FOR %%G IN (%_CD_IMAGES_EXT_LIST%) DO (
	if [%INPUTEXT%]==[.%%G] (
		REM if exist "%PROGRAMFILES%\WinMount\WinMount.exe" set TOOL=start "" "%PROGRAMFILES%\WinMount\WinMount.exe" -m %*
		REM if exist "%PROGRAMFILES%\DAEMON Tools Lite\DTLite.exe" set TOOL="%PROGRAMFILES%\DAEMON Tools Lite\DTLite.exe" -mount dt,0,"%~f1"
		REM if exist "%~d0\PortableApps\DTLite\DTLitePortable.bat" set TOOL=start "" "%~d0\PortableApps\DTLite\DTLitePortable.bat" -mount dt,0,"%~f1"
		REM set TOOL=dtlite -mount dt,0,"%~f1"
		REM set TOOL=%~d0\PortableApps\WinCDEmu\batchmnt.exe "%~f1"
		set TOOL=imdisk -f "%1"
	)
)
if [%INPUTEXT%]==[.iso] if exist "%WinDir%\system32\imdisk.exe" set TOOL=imdisk -a -t file -f %* -o cd -m #:
REM ^& start "" C:\WINDOWS\system32\imdisk.cpl

REM detect and mount FD images
set _FD_IMAGES_EXT_LIST=ima img fd flp vfd raw
FOR %%G IN (%_FD_IMAGES_EXT_LIST%) DO (
	if [%INPUTEXT%]==[.%%G] (
		if exist "%WinDir%\system32\imdisk.exe" set TOOL=imdisk -a -t file -f %* -o fd,rw -m #:
	)
)

if not defined TOOL set TOOL=echo %0: unsupported file format: "%INPUTEXT%"

REM echo %0: executing "%TOOL%"
%TOOL%
goto :eof


:LoCase
:: Subroutine to convert a variable VALUE to all lower case.
:: The argument for this subroutine is the variable NAME.
:: by Jiri http://www.robvanderwoude.com/battech_convertcase.php
FOR %%i IN ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") DO CALL SET "%1=%%%1:%%~i%%"
GOTO:EOF
