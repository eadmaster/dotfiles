@echo off
setlocal

if [%1]==[] goto usage
if [%1]==[-h] goto usage
if [%1]==[/?] goto usage

set NAME=%1
set CMD=%2

if [%2]==[] set CMD=status


REM name aliases
if [%NAME%]==[cups] set NAME=spooler
if [%NAME%]==[print] set NAME=spooler
if [%NAME%]==[printer] set NAME=spooler
REM TODO: implementare partial name matching (es. mat -> math)

if [%NAME%]==[list] (
	REM net start
	sc queryex type= service state= all
	goto :eof
)

if [%NAME%]==[internet] set NAME=networking
if [%NAME%]==[network] set NAME=networking
if [%NAME%]==[networking] if [%CMD%]==[start] (
	call sudo net start Dhcp

	REM refresh the ip address
	REM ipconfig /renew
	
	REM enable the default LAN card
	if not defined LAN_NAME call initenv
	call sudo netsh interface set interface "%LAN_NAME%" ENABLED
	
	REM poweron the wifi card if no wired connection is present
	call wifiswitch
	goto :eof
)
if [%NAME%]==[networking] if [%CMD%]==[stop] (
	call sudo net stop Dhcp
	
	REM release the ip address
	REM ipconfig /release
	
	REM poweroff the wifi card
	if not defined WIFIDEV call initenv
	call sudo devcon disable %WIFIDEV%
	
	REM disable the default LAN card
	if not defined LAN_NAME call initenv
	call sudo netsh interface set interface "%LAN_NAME%" DISABLED
	goto :eof
)

if [%NAME%]==[softap] (
	REM only available in Win >= 7
	REM TODO: start : netsh wlan set hostednetwork mode=allow ssid=SoftAP [key=<passphrase> keyUsage=persistent]
	REM TODO: stop : netsh wlan set hostednetwork mode=disallow
	call sudo netsh wlan %CMD% hostednetwork
	REM show the current settings
	netsh wlan show hostednetwork
	netsh wlan show hostednetwork setting=security
	goto :eof
)

if [%NAME%]==[reversetethering] (
	REM set "PATH=%~d0\SharedPrograms\gnirehtet;%~dp0"
	set "PATH=%PROGRAMFILES(X86)%\ClockworkMod\Universal Adb Driver;%~dp0"
	call java -jar %~d0\SharedPrograms\gnirehtet\gnirehtet.jar %CMD%
	goto :eof
)

if [%NAME%]==[adb] if [%CMD%]==[start] (
	if not defined ADB_HOME call initenv
	"%ADB_HOME%\adb.exe"  fork-server server
	goto :eof
)
if [%NAME%]==[adb] if [%CMD%]==[stop] (
	if not defined ADB_HOME call initenv
	"%ADB_HOME%\adb.exe"  kill-server
	goto :eof
)
if [%NAME%]==[adb] if [%CMD%]==[status] (
	"%ADB_HOME%\adb.exe" get-state
	goto :eof
)

if [%NAME%]==[ssh] set NAME=sshd

if [%NAME%]==[bluetooth] set NAME=bthserv
if [%NAME%]==[bluez] set NAME=bthserv

if [%NAME%]==[bittorent]  if [%CMD%]==[start] (
	echo %0: qBittorrent webui on "http://localhost:44940/"
	start c:\PortableApps\qBittorrent\qBittorrentPortable.exe --webui-port 44940
	REM default port 8080
	goto :eof
)

set TARGETDIR=%3
if [%TARGETDIR%]==[] set TARGETDIR=%CD%
set PASSWORD=%RANDOM%

if [%NAME%]==[sftpd] set NAME=sftp
if [%NAME%]==[sftps] set NAME=sftp
if [%NAME%]==[usftpd] set NAME=sftp
if [%NAME%]==[sftp] if [%CMD%]==[start] (
	echo %0: serving "%TARGETDIR%" to "sftp://%COMPUTERNAME%:2022"
	
	REM rclone  https://rclone.org/commands/rclone_serve_sftp/
	start rclone serve sftp --addr ":2022" --no-auth %TARGETDIR%  
	REM --vfs-cache-mode writes 
	REM --user %USERNAME% --pass %PASSWORD% 
	goto :eof
)
if [%NAME%]==[sftp] if [%CMD%]==[stop] (
	REM  TODO taskkill /f /im rclone.exe ...
	echo %0: unimplemented
	goto :eof
	REM TODO: alternative using window builtin service?
)

if [%NAME%]==[upnp] set NAME=dlna
if [%NAME%]==[dlna] (
	echo %0: serving "%TARGETDIR%" to "upnp://%COMPUTERNAME%:8080"
	
	REM rclone  https://rclone.org/commands/rclone_serve_dlna/
	start rclone serve dlna --addr ":8080" %TARGETDIR%
	goto :eof
	REM TODO: alternative using window builtin service?
)
REM TODO: daemon mode, start/stop command

if [%NAME%]==[boblight] set NAME=ambilight
if [%NAME%]==[ambilight] if [%CMD%]==[start] start ""  "%ProgramFiles(x86)%\AmbiBox\AmbiBox.exe"
if [%NAME%]==[ambilight] if [%CMD%]==[stop]  pkill AmbiBox
REM TODO: if [%NAME%]==[ambilight] if [%CMD%]==[pause]  nircmd sendmouse ...

if [%NAME%]==[docker] if [%CMD%]==[start] qemu -smp 2 -m 1024  -cdrom C:\VirtualMachines\boot2docker.iso
REM if [%NAME%]==[docker] if [%CMD%]==[stop] pkill ...

if [%NAME%]==[linux] set NAME=LxssManager
if [%NAME%]==[wsl] set NAME=LxssManager
::if [%NAME%]==[linux] if [%CMD%]==[start] (
	::REM TODO: fix usb mount https://superuser.com/questions/1412316/qemu-mount-a-virtual-fat32-folder-on-windows-host
	::REM qemu -m 256 -kernel %PUPPY_HOME%\vmlinuz -initrd %PUPPY_HOME%\initrd.gz -append root=/dev/ram0 -hda %PUPPY_HOME%\slackosave.2fs -hdb %PUPPY_HOME%\puppy_slacko_5.4.sfs
	::REM qemu -m 256 -usb -usbdevice ... -kernel %PUPPY_HOME%\vmlinuz -initrd %PUPPY_HOME%\initrd.gz -append "psubdir=/multiboot/slacko53 psubok=TRUE"
	::REM boot options  https://puppylinux.org/wikka/BootParametersPuppy
	::REM qemu  -k it -m 1024 -redir tcp:2222::22 -kernel %PUPPY_HOME%\casper\vmlinuz -initrd %PUPPY_HOME%\casper\initrd1.xz -append "pfix=nocopy,nox"  -hda %PUPPY_HOME%\casper\01-filesystem.squashfs  -hdb %PUPPY_HOME%\casper\02-opt-trinity.squashfs  -hdc %PUPPY_HOME%\casper\03-usr-part1.squashfs   -hdd  C:\VirtualMachines\fakeusb_drive_fat.img
	::REM -hdd %PUPPY_HOME%\casper\changes.dat 
	::REM -cdrom  c:\VirtualMachines\fakeusb_drive_fat.iso
	::REM -drive file.driver=vvfat,file.dir=%~d0\VirtualMachines,file.fat-type=32
	::REM TODO: FIX -drive file=fat:rw:fat-type=32:label=MULTIBOOT:%~d0\VirtualMachines,format=raw,if=virtio
	::REM  -accel whpx
	::REM -enable-hax  -> intel only?
	::REM -net user,smb=C:\
	::REM -hda \\.\PhysicalDrive1   -append root=/dev/ram0
	::REM   -localtime -no-acpi 
	
	::REM ALTERNATIVE:
	::call qemu -smp 2 -k it -m 1024 -boot d  -cdrom C:\VirtualMachines\mini.iso -hda C:\VirtualMachines\ubuntu-bionic-18.04-myos.qcow2  -redir tcp:2222::22  
	::echo %0: login via putty ubuntu@localhost:2222

	::REM call qemu  -k it -m 1024 -vga vmware -hda "C:\VirtualMachines\Ubuntu Server 18.04.2 (64bit).vmdk"  -hdb fat:rw:%SYSTEMDRIVE%\CLIPrograms\home  -redir tcp:2222::22   
	::REM 2FIX: interface autostart: sudo ip link set dev ens3 up
	::REM echo %0: login via putty osboxes@localhost:2222

	::goto :eof

::)
::if [%NAME%]==[linux] if [%CMD%]==[stop] (
	::REM TODO: send power off command via ssh
	::call ssh -P 2222 ubuntu@localhost power off
	::call pkill qemu
	::goto :eof
::)

if [%NAME%]==[av] set NAME=antivirus
if [%NAME%]==[antivirus] (
	if exist "%PROGRAMFILES%\Avira\AntiVir Desktop" set NAME=AntiVirService
	if exist "%PROGRAMFILES%\Microsoft Security Client" set NAME=MsMpSvc
	if exist "%ProgramW6432%\Microsoft Security Client" set NAME=MsMpSvc
	if exist "%ProgramFiles%\Windows Defender\MpCmdRun.exe" set NAME=WinDefend
	if exist "%ProgramFiles%\AVAST Software\Avast" set NAME="Avast Antivirus"
REM  WinDefent must be set Manual for this to work
REM avg http://www.ehow.com/how_8439576_manually-turn-off-avg.html
REM   net stop AVGIDSAgent
REM   net stop "AVG WatchDog"
REM ...
)
REM if [%ERRORLEVEL%]==[2] -> disable the option "Prevent AntiVir processes from being terminated" under "Configuration" - "General" - "Security" http://forum.avira.de/wbb/index.php?page=Thread&threadID=73291
if [%NAME%]==[antivirus] (
	REM else
	echo %0: err: no known antivirus found  1>&2
	exit /b 9009
)

if [%NAME%]==[http] set NAME=httpd
REM if [%NAME%]==[https] set NAME=httpd
if [%NAME%]==[httpd] set NAME=httpd
if [%NAME%]==[uhttpd] set NAME=httpd
if [%NAME%]==[httpd] if [%CMD%]==[start] (
	echo %0: serving "%TARGETDIR%" on "http://%COMPUTERNAME%:8000"

	REM rclone  https://rclone.org/commands/rclone_serve_http/
	start rclone serve http --addr ":8000" %TARGETDIR%
	if [%ERRORLEVEL%]==[0] goto :eof

	REM python 2.x:
	REM start "python SimpleHTTPServer" /D %TARGETDIR% python -m SimpleHTTPServer 80
	start python2 -m SimpleHTTPServer 8000
	if [%ERRORLEVEL%]==[0] goto :eof
	REM ALTERNATIVE: python %PYTHONHOME%\Tools\Scripts\serve.py %TARGETDIR% 80 -> directory listing is not supported
	REM python 3.x:
	REM start "" /D %TARGETDIR% 
	start python3 -m http.server 8000
	if [%ERRORLEVEL%]==[0] goto :eof

	REM using PHP >=5.4.0 (no file listing)  http://php.net/manual/en/features.commandline.webserver.php
	start php -S 0.0.0.0:8000 -t %TARGETDIR%
	if [%ERRORLEVEL%]==[0] goto :eof

	REM using netwox (no file listing)
	REM start "%~dp0netwox-5.39.0\netwox539.exe" 125 -P 8000 --rootdir %TARGETDIR%
	REM if [%ERRORLEVEL%]==[0] goto :eof

	REM using busybox  https://busybox.net/downloads/BusyBox.html#httpd
	REM 2FIX: httpd missing in busybox windows build
	REM  -c "%~dp0uhttps.conf"
	start busybox httpd -f -v -p 0.0.0.0:8000  -h %TARGETDIR%
	if [%ERRORLEVEL%]==[0] goto :eof

	REM using sfk  http://stahlworks.com/dev/index.php?tool=httpserv
	REM MEMO: only the CURRENT DIRECTORY is made accessible, without subdirs 
	cd %TARGETDIR%
	start "%~dp0sfk.exe" httpserv -port=8000 -rw
	if [%ERRORLEVEL%]==[0] goto :eof
	goto :eof
)
REM TODO: if [%NAME%]==[httpd] if [%CMD%]==[stop] (

if [%NAME%]==[ftp] set NAME=ftpd
if [%NAME%]==[ftps] set NAME=ftpd
if [%NAME%]==[uftpd] set NAME=ftpd
if [%NAME%]==[ftpd] if [%CMD%]==[start] (
	echo %0: serving "%TARGETDIR%" on "ftp://%COMPUTERNAME%:2121"
	
	REM using rclone v>1.44  https://rclone.org/commands/rclone_serve_ftp/
	REM By default this will serve files without needing a login. You can set a single username and password with the --user and --pass flags
	start "" rclone serve ftp --addr ":2121" %TARGETDIR%
	goto :eof
)
REM TODO: if [%NAME%]==[ftpd] if [%CMD%]==[stop] (

if [%NAME%]==[vnc] if [%CMD%]==[start] (
	start "" "%~d0\PortableApps\TigerVNC\TigerVNCServerPortable.bat"
	goto :eof
)
REM TODO: if [%NAME%]==[vnc] if [%CMD%]==[stop] (

if [%NAME%]==[camera] set NAME=webcam
if [%NAME%]==[webcam] if [%CMD%]==[start] (
	REM start webcam streaming with VLC:
	REM  http://www.lavrsen.dk/foswiki/bin/view/Motion/FeatureRequest2009x07x14x150700
	echo %0: starting VLC camera streaming to "http://%COMPUTERNAME%:8082/go.mjpg"...
	start "VLC" vlc dshow:// :dshow-size=640x480 :sout=#transcode{vcodec=MJPG,vb=800,fps=5}:std{access=http{mime=multipart/x-mixed-replace;boundary=--7b3cc56e5f51db803f790dad720ed50a},mux=mpjpeg,dst=0.0.0.0:8082/go.mjpg,delay=0} 
	goto :eof
)

if [%NAME%]==[motion] if [%CMD%]==[start] (
	call service webcam start
	REM wait for VLC to start
	call sleep 5

	echo %0: starting motion server, check the web interface at "http://%COMPUTERNAME%:8080"
	start "Motion" "%~dp0motion-3.2.12\motion.exe" -c "%~dp0motion-3.2.12\.motion\motion.conf"  %*
	goto :eof
)

if [%NAME%]==[motion] if [%CMD%]==[stop] (
	taskkill /f /im motion.exe
	REM taskkill /f /im vlc.exe
	del /F /Q "%~dp0motion.exe.stackdump"
	del /F /Q "motion.exe.stackdump"
	REM disable cygwin stackdump creation -> ulimit -c 0  http://cygwin.com/cygwin-ug-net/ov-new1.7.html
	goto :eof
)

if [%NAME%]==[tor] if [%CMD%]==[start] (
	if exist "%~d0\PortableApps\AdvOR\AdvOR.exe" (
		start "" "%~d0\PortableApps\AdvOR\AdvOR.exe" --start --minimize 
		if [%ERRORLEVEL%]==[0] goto :eof
	)
	
	sudo tor
	if [%ERRORLEVEL%]==[0] goto :eof
)
if [%NAME%]==[tor] if [%CMD%]==[stop] (
	sudo taskkill /IM tor.exe /F
	if [%ERRORLEVEL%]==[0] goto :eof

	taskkill /IM AdvOR.exe /F
	if [%ERRORLEVEL%]==[0] goto :eof
)
REM else
if "%NAME%"=="tor" set NAME="Tor Win32 Service"

if [%NAME%]==[pcap] set NAME=npf
if [%NAME%]==[winpcap] set NAME=npf

if [%NAME%]==[smb] set NAME=samba
if [%NAME%]==[samba] (
	call sudo net %CMD% server
	call sudo net %CMD% browser
	goto :eof
)

if [%NAME%]==[rdp] set NAME=TemService

if [%NAME%]==[nbz] set NAME=nzbget
if [%NAME%]==[nzb] set NAME=nzbget
if [%NAME%]==[nzbget] if [%CMD%]==[start] (
	echo %0: nzbget webui on "http://localhost:6789/"
	start nzbget -s
	goto :eof
)
if [%NAME%]==[nzbget] if [%CMD%]==[stop] (
	nzbget -Q 
	goto :eof
)
if [%NAME%]==[nzbget] if [%CMD%]==[status] (
	nzbget -L
	goto :eof
)

if [%CMD%]==[info] set CMD=status
if [%CMD%]==[find] set CMD=status
if [%CMD%]==[status] (
	REM UNRELIABLE: if [%ERRORLEVEL%]==[0] goto :eof
	call wmic service where Name="%NAME%" get * /format:textvaluelist
	echo.
	call sc query %NAME%
	goto :eof
)

if [%CMD%]==[enable] (
	sudo sc config %NAME% start= auto
	goto :eof
)

if [%CMD%]==[disable] (
	sudo sc config %NAME% start= demand
	goto :eof
)


REM else try with system services

call sudo net %CMD% %NAME%
if %ERRORLEVEL%==0 goto :eof

call sudo sc %CMD% %NAME%
if %ERRORLEVEL%==0 goto :eof

REM try alternative names

REM 2FIX: recursive call
REM if [%NAME%]==[npcap] (
REM	call %0 npf %CMD%
REM	goto :eof
REM )

REM print the status if cmd was start or stop
if [%CMD%]==[start] call %0 %NAME% status
if [%CMD%]==[stop] call %0 %NAME% status

REM else
exit /B 1


:usage
echo usage: %0 service_name start^|stop^|status^|enable^|disable
echo.
exit /B 0
