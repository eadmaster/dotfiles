;= @echo off

;= REM http://ben.versionzero.org/wiki/Doskey_Macros

;= REM Call and use this file as the macrofile
;= doskey /macrofile="%~f0"

;= doskey time="%~dp0time.bat" $*
;= doskey rename="%~dp0rename.bat" $*

;= REM In batch mode, jump to the end of the file
;= goto :eof




;= DOS-style macros
deltree=rd /S /Q $*
scandisk=chkdsk /F /R $*
;= mem=systeminfo | findstr Memory -> MOVED IN free.bat
mem=free
;= keyb=...
;= join=... (mount a drive as a directory)

;= AmigaDOS-like commands  http://wiki.amigaos.net/index.php/AmigaDOS_Introduction  http://en.wikipedia.org/wiki/AmigaDOS  http://www.pcguru.plus.com/uae_amigados.html
list=dir $*
;= rename=ren $*
;= delete=del $*
;= protect=attrib $*
setenv=set $*
;= unsetenv=set $1=
getenv=set
;= get=echo %$1%
;= ask=choice $*
;= avail=mem
;= version=ver
;= changetaskpri=nircmdc setprocesspriority $*
;= endcli=exit
;= execute=call $*
;= filenote=...
;= NO(DIFFERENT UNIX COMMAND)? join=if [$2]==[] ( echo usage: join [piece1] + [piece2] + ... [output.ext] ) else ( copy /b $* )
;= makedir=md $*
;= makelink=ln $*
setkeyboard=intlcfg -inputlocale:$*
;= setmap=intlcfg -inputlocale:$*
;=  ALTERNATIVE: using config+xml file http://blogs.msdn.com/b/shawnste/archive/2007/04/12/configuring-international-settings-from-the-command-line.aspx
status=tasklist /V /fi "IMAGENAME eq $*.*" /FO list
why=echo ERRORLEVEL=%ERRORLEVEL%

;= OpenVMS-like commands  https://www.mpp.mpg.de/~huber/vmsdoc/vms-unix_cmd-equivalents.html  http://www.physnet.uni-hamburg.de/physnet/vms-unix-commands.html
;= directory=du $*
d=du $*
purge=find -name '*~' -delete
;= append=cat $* -> CONFLICTS WITH %WINDIR%\system32\append.exe
;= assign=set $*
;= define=set  $*
;= backup=tar $*
;= create=copy nul $*
dump=od $*
;= library=ar $*
;= link=ld $*
;= merge=sort -m $*
;= recall=history $*
;= search=grep $*
;= submit=at $*

;= Unix-style macros
;= http://en.wikipedia.org/wiki/List_of_Unix_utilities http://cb.vu/unixtoolbox.xhtml
clear=cls
pwd=cd
;= touch=nircmdc setfiletime $* now -> MOVED IN touch.bat
;= cat=type $* -> MOVED IN cat.bat
tac=busybox tac $*
;= rev=sed "/\n/!G;s/\(.\)\(.*\n\)/&\2\1/;//D;s/.//" $*
;= head=more $* -> MOVED IN head.bat
;= tail=type $* -> MOVED IN tail.bat
;= f=unix find $*
f=fd --hidden --color never --ignore-case --glob *$**
findext=fd -e $*
;= findlatestchanged=ls -a -R -t1 -l -p -h |  grep -v / |  head -n 10
findchangedtoday=busybox find -mtime -1
;= search=find $*
;= findname=find . -iname $*
;= ls=dir /b /w $*
ls=busybox ls --color $*
;= -F -h -w 150
cp=copy $*
;=cp=xcopy /F /H /E $**
mv=move $*
rm=del /p $*
chmod=attrib $*
cmp=comp $*
;= diff=fc $* -> MOVED IN diff.bat
env=set
;= printenv=if [$1]==[] ( set ) else ( echo %$1% )
;= export=set $*
;= locale=set LANG $T set LC
alias=doskey $*
unalias=doskey $1=
history=doskey /history
ps=tasklist $*
;= ps=bosybox ps $*
pgrep=bosybox pgrep $*
;= nice=start "" /$*
;= renice=nircmdc setprocesspriority $2.exe $1 -> MOVED IN renice.bat
;= pidof=tasklist /fi "IMAGENAME eq $*.exe"
kill=taskkill /f /pid $*
killall=wmic process where name='$1.exe' delete
lsof=handle $*
top=wmic process list brief /every:1
ifconfig=ipconfig $*
;= iwconfig=ipconfig /ALL $B filtrare NIC wifi
;= su=runas /user:Administrator "%~d0\PortableApps\Console\Console.exe" -> MOVED IN su.bat
;= sudo=runas /user:Administrator "$*" -> MOVED IN sudo.bat
;= share=net share $~n1=$~f1 /UNLIMITED -> MOVED IN share.bat
;= unshare=net share $~n1 /DELETE -> MOVED IN unshare.bat
whoami=echo %USERNAME%
;= logname=echo %USERNAME%
id=wmic useraccount where Name='%USERNAME%'
;= REM TODO: list group sid
getuid=wmic useraccount where Name='%USERNAME%' get SID
who=psloggedon $*
w=psloggedon $*
users=psloggedon $*
lsuser=net user $*
lsgroup=net localgroup $*
;= groups=net user %USERNAME% $B findstr "Local Group Memberships" -> MOVED IN groups.bat
;= getent=... -> query the system names db (users, groups, etc.)
uname=ver
time="%~dp0time.bat" $*
getdate=timestamps
source=call $*
;= ed=edlin $*
;= dd=dd --progress $*
;= lp=print $*
;= lpr=print $*
;= halt=shutdown -s
cancelshutdown=shutdown -a
;= softreboot=pkill explorer.exe ; explorer.exe
logout=exit
logoff=sudo shutdown -l
suspend=standby
;= hibernate=nircmdc hibernate
;= hibernate,standby=RunDll32.exe powrprof.dll,SetSuspendState
;= osinfo=SYSTEMINFO $* -> MOVED IN osinfo.bat
sysinfo=osinfo
ver=osinfo
;= bench=winsat $* -> MOVED IN cpubench.bat
;= cpubench=7z b -> MOVED IN cpubench.bat
bench=cpubench
gpubench=winsat d3d
diskbench=winsat disk -drive $*
;= cpuinfo=wmic cpu list full -> MOVED IN cpuinfo.bat
cpuid=cpuinfo
;= raminfo=wmic MEMORYCHIP list full
;= gpuinfo=winsat features -> MOVED IN gpuinfo.bat
gfxinfo=gpuinfo
cputemp=cpuinfo
gputemp=gpuinfo
sensor=sensors
smartscan=smartctl --scan
hdinfo=smartctl -a /dev/hda
hddinfo=smartctl -a /dev/hda
;= hddinfo2=smartctl -a /dev/hdb
hddtemp=smartctl -a /dev/hda $b findstr Celsius
;= hwinfo=devcon find * -> MOVED IN hwinfo.bat
;= hwls=devcon find $*
lsdev=devcon find *
;= lsmod=devcon status *
;= lsmod=driverquery
lspci=devcon find pci\*
lsusb=devcon find usb\*
;= lsblk=wmic diskdrive get Caption,DeviceID,Model,Partitions -> MOVED in lsblk.bat
traceroute=tracert $*
host=nslookup $*
;= dig=nslookup $*
;= route-n=route print
;= service=net $2 $1
;= service=sc $2 $1
stop=service $1 stop
insmod=sc start $1
rmmod=sc stop $1
;= free=systeminfo | findstr Memory
;= vmstat=mem
;= meminfo=wmic MEMORYCHIP get Capacity,DeviceLocator,BankLabel,Speed,PartNumber,Manufacturer -> MOVED IN hwinfo.bat
;= dmesg=psloglist -s -d 0 -> MOVED IN dmesg.bat
syslog=dmesg
smbtree=net view $*
smbmount=net use $2 $1
smbumount=net use $* /delete
wipe=srm $*
sdel=srm $*
shred=srm $*
zerofree=sfill $*
;= zerofill=format $1 /X /P:1
;= zerofill=dd if=/dev/zero of="$1" bs=$~z1 count=1
fdisk=diskpart $*
;= parted=diskpart $*
;= readelf=perdr $*
;= xwininfo=...
;= ntsysv, chkconfig=net...
;= dpkg=msiexec $*
at=schtasks $*
crontab=schtasks $*
mdconfig=imdisk $*
mkfs=format $*
mkfs.fat32=format /FS:FAT32 $*
mkfs.ntfs=format /FS:NTFS $*
mkfs.exfat=format /FS:exFAT $*
;= fdformat=format a: $*
fsck=chkdsk $*
;= xlock=RunDll32.exe user32.dll,LockWorkStation -> MOVED IN xlock.bat
;= flock=unix flock $*
flock=lock $*
;= lockf=flock $*
fuser=handle $*
wholock=handle $*
;= look=findstr /I /B /C:$* -> MOVED IN look.bat
;= wmctrl=nircmdc win $*
read=SET /P $1=
;= write=mailsend $*
;= send an INSTANT message to another user  https://stackoverflow.com/questions/42715392/pop-up-message-using-powershell
talk=msg console /server:$1 "$2"
write=msg console /server:$1 "$2"
;= watch=nircmdc loop 100000 2000 execmd $* -> MOVED IN watch.bat
;= type=... (describe a command: alias, builtin, file, etc.) http://ss64.com/bash/type.html
;= wait=nircmdc waitprocess $* -> MOVED IN wait.bat
;= pg=... http://en.wikipedia.org/wiki/Pr_(Unix)
;= link=ln $*
;= pax=tar $*

watchfile=tail -F


;= Shortcuts

;= todo=start %PENDRIVE%\Documents\TODO.txt
;= wanted=start %PENDRIVE%\Documents\WANTED.txt
;= wishlist=start %PENDRIVE%\Documents\wishlist.txt
;= shoplist=start %PENDRIVE%\Documents\shoplist.txt

;= note=mynotes $*
notes=mynotes $*
mynote=mynotes $*
;= memo=mynotes $*

up=cd ..
..=cd ..
...=cd ..\..
....=cd ..\..\..
;= e=start .
;= ALTERNATIVE: e=explorer %CD%
open=xdg-open $*
;= view=fileview $*
;= load=start "" $*
;= run=start "" $*
;= display=start "" $*
;= xdg-open=start "" $*
;= xdg-mime=file $*
l=busybox ls -AFh --color=auto $*
ll=busybox ls -AFh --color=auto $*
c=calc $*
h=doskey /history
d=busybox du -shx $*
;= f=busybox find $*
g=busybox grep $*
;= rg=unix grep -r -I -n -H  --exclude \*.min.js --color=always $*

unmount=umount $*
eject=umount $*

;= setro=attrib +R $*
ro=attrib +R $*
rw=attrib -R $*
hide=attrib +H $*
unhide=attrib -H $*

perms=cacls $*
;= own=chown %USERNAME% $*
;= chacl=... $*
;= resetacl=... $*
;= reacl=... $*
;= protect=echo s| cacls $* /P "%USERNAME%":R
;= unprotect=echo s| cacls $* /P "%USERNAME%":F
;= unprotect=cacls $* /E /R "%USERNAME%"
;= ro=echo s| cacls $* /P "%USERNAME%":R
;= rw=echo s| cacls $* /P "%USERNAME%":F

;= bincat=if [$2]==[] ( echo usage: bincat [piece1] + [piece2] + ... [output.ext] ) else ( copy /b $* )
;= NO(DIFFERENT UNIX COMMAND)? merge=if [$2]==[] ( echo usage: merge [piece1] + [piece2] + ... [output.ext] ) else ( copy /b $* )

;= stego=steghide $*
;= steg=if [$2]==[] ( echo usage: steg [image.jpg] + [hide.rar] [newimage.jpg] ) else ( copy /b $* )
;= unsteg=ren $* $*.rar
;= unsteg=7z x $*

;= screensaver=start "" "%WinDir%\System32\ssmarque.scr" /S -> MOVED IN xdg-screensaver.bat
screensaver=xdg-screensaver

;= unlock="%~d0\PortableApps\NirLauncher\NirSoft\openedfilesview.exe" /filefilter $* -> MOVED IN unlock.bat
;= forcedel=...

;= pwd=pwsafe $*
;= pass=pwsafe $*
;= password=pwsafe $*
getpass=mypass $*

;= register=regsvr32 $*
;= regdll=regsvr32 $*
;= unregdll=regsvr32 /u $*
;= infinstall=rundll32 setupapi,InstallHinfSection DefaultInstall 132 $*
;= infuninstall=rundll32.exe setupapi.dll,InstallHinfSection DefaultUninstall 132 $*

;= tc=%~d0\PortableApps\TotalCommander\TOTALCMD.EXE /N "%CD%" -> MOVED IN tc.bat
;= dc=%~d0\PortableApps\DoubleCommander\doublecmd.exe ... "%CD%"

;= empty=copy nul $*
;= new=copy nul $* -> MOVED IN filenew.bat
;= newsz=fallocate $1 -l $2
createsz=truncate $*
trunc=truncate $*
;= chsize=truncate $*

;= fcp=dd if=$1 of=$2 bs=1 conv=sync,noerror -> MOVED IN fcp.bat
forcecopy=fcp $*
;= safecp=fcp $*
;= safecopy=fcp $*

;= partcp=dd bs=1 count=$3 if=$1 of=$2
;= partcopy=dd bs=1 count=$3 if=$1 of=$2

;= fixmbr=...
;= ms-sys=...
;= bakmbr=dd if=/dev/hda of=$1 count=1 bs=512
;= cleanmbr=dd if=/dev/zero of=$1 count=1 bs=512

;= ntfsinfo=fsutil fsinfo ntfsinfo $*
;= ALTERNATIVE: %SYSINTERNALS_PATH%\ntfsinfo.exe $*
;= ntfscleardirty=CHKNTFS /X $* -> clear the dirty bit)
;= ntfsfix=... (part of ntfsprogs: set the dirty bit)
;= ntfscluster=... (part of ntfsprogs: Given a cluster, or sector, find the file) | Microsoft nfi.exe | sleuthkit http://waynes-world-it.blogspot.it/2008/03/viewing-ntfs-information-with-nfi-and.html
;= ntfsdiskedit=... (part of ntfsprogs: Walk the tree of NTFS ondisk structures (and alter them))

;= sector=nfi $*
;= sectorsize=wmic DISKDRIVE get bytespersector, caption, DeviceID, InterfaceType
getclustersize=SIZDIR32 /L /Q $*
bestclustersize=SIZDIR32 $*
;= ntfscompress=compact /c /s $*
;= MEMO: NTFS compression req. cluster size <= 4096

mail=start "" "http://mail.google.com"
;= mailx=mailcheck $*
;= email=mailcheck $*
;= send=mailsend $*
;= sendmail=mailsend $*
;= sendemail=mailsend $*
checkmail=myemailcheck $*
emailcheck=myemailcheck $*
;= xdg-email=%MAILER% -compose "mailto:$*"

sqlite=sqlite3 $*
sqls=echo .tables | sqlite3 $*
sqlcat=echo .dump | sqlite3 $*
;= http://www.sqlite.org/sqlite.html

;= cdinfo=cdrdao disk-info --device %CDR_DEVICE%
;= ALTERNATIVE: cdrecord -atip -media-info
;= dvdinfo=dvd+rw-mediainfo %CD_DRIVE% -> DO NOT PRINT DVD BURN DATE
;= ALTERNATIVE: cdrecord -atip
;= cdcheck=dvdisaster -d %CD_DRIVE% -s
;= cdscan=cdread -v -c2scan
;= dvdscan=cdread -fulltoc -pifscan -pi8scan
;= isols=isoinfo -f -i $*
;= isols=isoinfo $*
;= cd-read=cdread $*
;= readcd=cdread $*
;= cdparanoia=cdda2wav $*
;= bin2iso=fileconvert $*

;= scanbus=cdrecord -scanbus
;= cdblank=cdrecord -v blank=fast
;= burniso=cdrecord -v -sao driveropts=burnfree,noforcespeed $*
;= burnisosim=cdrecord -v -sao driveropts=burnfree,noforcespeed -dummy $*
mkiso=mkisofs $*
;= genisoimage=mkisofs $*
;= mkiso=if [$2]==[] ( echo usage: mkiso [output file] [root dir] ) else ( 7z a -tiso $* )
;= mkudf=if [$2]==[] ( echo usage: mkiso [output file] [root dir] ) else ( 7z a -tudf $* )
;= mkiso=if [$2]==[] ( echo usage: mkiso [options] [output file] [root dir] ) else ( mkisofs -l -iso-level 3 -J -o $* )

qemuimg=qemu-img $*
;= raw2vmdk=qemu-img convert -f raw -O vmdk $*
;= vmdk2raw=qemu-img convert -f vmdk -O raw $*
;= qemu-img-vdi http://lists.gnu.org/archive/html/qemu-devel/2008-07/msg00430.html
;= vdi2raw="%PROGRAMFILES%\Sun\VirtualBox\VBoxManage.exe" convertdd $*
;= vdi2raw="%PROGRAMFILES%\Sun\VirtualBox\VBoxManage.exe" internalcommands converttoraw $*
;= raw2vdi="%PROGRAMFILES%\Sun\VirtualBox\VBoxManage.exe" convertfromraw --format VDI $*

;= QEMU in console mode
;= cemu=qemu -vga none -nographic $*

;= boot=qemu -boot c -hda //./$*
bootfd=qemu -boot a -fda //./a: $*
bootfdi=qemu -boot a -fda $*
;= boothd=qemu -snapshot -boot c -hda \\.\PhysicalDrive1 ;= admin requested
boothdi=qemu -snapshot -boot c -hda $*
bootcd=if [$1]==[] ( echo usage: bootcd [drive]: - WARNING! you must be admin ) else ( qemu -boot d -cdrom $* )
bootcdi=qemu -boot d -cdrom $*
bootiso=qemu -boot d -cdrom $*
;= bootusb=if [$1]==[] ( echo usage: bootusb [drive]:  - WARNING! you must be admin ) else ( qemu -boot c -hda //./$* )
;= bootusb=qemu -snapshot -boot menu=on -usb -usbdevice disk:\\.\PhysicalDrive1
;= bootsdi=qemu -boot ? -sd $*
;= bootnet=qemu -boot n ...
;=  -net user -tftp dir

;= device dump using cygwin's dd | GnuWin32's dd | chrysocome.net's dd --> readfdi=dd if=//./a: of=$*
;= readhdi=dd if=??? of=$*
;= readfdi=dd if=\\.\a: of=$* --progress
;= readiso=dd if=\\?\Device\CdRom1 of=$* --progress
;= writefdi=dd if=$* of=/dev/fd0
;= ALTERNATIVE: rawrite -> http://www.chrysocome.net/rawwrite

;= ascii=findstr $* %GNUWIN32_HOME%\share\misc\ascii -> MOVED IN ascii.bat

;= dircmp=rsync $* -> MOVED IN dircmp.bat
dirdiff=dircmp $*
cmpdir=dircmp $*
;= uwd=dircmp

flush=sync $*

;= synergys=%~d0\PortableApps\Synergy\SynergyServerPortable.bat $*
;= synergyc=%~d0\PortableApps\Synergy\SynergyClientPortable.bat $*

gpglskeys=gpg --list-keys $*
;= keyring=gpg --fingerprint $*
;= gpgi=gpg -a --import $*
;= gpge=gpg -a --export $*
gpggetkey=gpg --recv-keys $*
gpgupdatekeys=update_keys
gpgrefreshkeys=update_keys

;= simmetric encryption (default algo: CAST5) - password is prompted
;= encrypt=crypt $*
;= cipher=crypt $*
;= aes=crypt --cipher-algo AES256 $*
;= des=...
;= 3des=crypt --cipher-algo 3DES $*

;= asimmetric encryption (algo depends on key) - recipient public key is requested
;= secret=if [$2]==[] ( echo usage: secret [recipient] [plaintext] ) else ( gpg -v -a -r $1 -o $2.pgp -e $2 )
gpgverify=gpg --verbose --verify $*
;= pwgen=gpg --armor --gen-random 1 32 -> MOVED TO pwgen.bat
mkpass=pwgen $*
mkpwd=pwgen $*

exif=exiftool $*

tzip=trrntzip $*
zipappend=zip -j --grow $*
zippreview=gzip -c $1  $B  wc -c  $B  unix numfmt --to=iec
7zpreview=xz --format=lzma -c $1   $B  wc -c  $B  unix numfmt --to=iec

bytes2human=unix numfmt --to=iec $*

;= atool-style macros:
als=7z l $*
pack=filepack $*
compress=filepack $*
aunpack=fileunpack $*
unpack=fileunpack $*
uncompress=fileunpack $*
decompress=fileunpack $*
extract=fileunpack $*
;= acat=7z e -so $*
zcat=gzip -d -c $*
atest=filecheck $*
acd=mount $*
pprint=file2txt

scite=geany $*
npp=geany $*

;= ii=%MAGICK_HOME%\identify $*
;= cc=%MAGICK_HOME%\identify -format %k $*
;= im=%MAGICK_HOME%\$*
;= im=imconvert $*
magick=imconvert $*
;= imconvert=%MAGICK_HOME%\convert.exe -monitor $* -> MOVED IN imconvert.bat
mogrify=%MAGICK_HOME%\mogrify
;= display=%MAGICK_HOME%\display -> NO? REQ. X SERVER
display="C:\PortableApps\IrfanView\i_view32.exe" $*
;= convert=imconvert $*
png2ico=img2ico $*
ico2png=ico2img $*
;= icmp="%MAGICK_HOME%\compare.exe" $*
;= idiff="%MAGICK_HOME%\compare.exe" $*
;= shot=nircmdc savescreenshot $* -> MOVED IN shot.bat
snap=shot $*
screenshot=shot $*
screencap=shot $*

;= gimp=execext gimp $* -> MOVED IN gimp.bat

;= svg2png=inkscape "$*" --without-gui --export-png="$*.png" --export-use-hints  -> MOVED IN fileconvert.bat
;= bmp2svg=potrace -s $* -> MOVED IN fileconvert.bat
;= wmf2svg=unix wmf2svg $* -> MOVED IN fileconvert.bat
;= swfextract=%~dp0_swftools-0.9.0\swfextract.exe $*

;= raw2png=dcraw -c -n 200 -w $* | imconvert ppm:- $*.png  -> MOVED IN fileconvert.bat
;= dng2png=dcraw -c -n 200 -w $* | imconvert ppm:- $*.png  -> MOVED IN fileconvert.bat
;= white balance: -a, -p embed

;= pdfpageresize=java %~dp0Multivalent.jar tool.pdf.Impose -dim 1x1 -paper $*
;= pdfprint="%PROGRAMFILES%\PDFCreator\PDFCreator.exe" /PF"$*"
;= tex2pdf=pdflatex $* -> MOVED IN fileconvert.bat
;= unpdfimg=pdfimages $* | mupdfextract (from mupdf-tools)
;= pdf2ppm=pdftoppm $* .
pdf2html=pdftohtml $*

;= pdfcat=pdftk $* cat output "$* COMBINED.pdf"  -> MOVED IN pdfcat.bat
pdfjoin=pdfcat $*
catpdf=pdfcat $*

;= pdfcut=pdftk $1 cat $2 output $3  -> MOVED IN pdfcut.bat
pdfcut=filecut $*
pdfcat=filecat $*
audiocmp=filecmp $*
audiohash=mediahash $*

;= clit=ebook-convert $*
;= econvert=ebook-convert $*
;= epub2pdf=ebook-convert "$*" "$*.pdf"  -> MOVED IN fileconvert.bat
;= pdf2chm=ebook-convert "$*" "$*.chm"  -> MOVED IN fileconvert.bat
;= pdfmanipulate=%~d0\PortableApps\Calibre\App\pdfmanipulate.exe $*

;= qvlc=vlc -I Qt $*
;= svlc=vlc -I skins2 $*
;= winamp=vlc -I skins2 --skins2-last=%MYDOCUMENTS%\Skins\Winamp\UltraClean_Original.wsz $*
;= winamp=execext winamp $*
;= wa=execext winamp $*
wa=winamp $*

mp=mplayer $*
me=mencoder $*

;= play=mplayer $*
;= ALTERNATIVES: sox $*, start "" $*
;= soxi=sox --info $*
recmic=rec $*
micrec=rec $*

;= mpc=%~d0\PortableApps\MPC\mpc-hc.exe $*

;= decode=fileconvert $* wav
;= ALTERNATIVE NAMEs: towav, any2way, 2wav, mdec

;= loseless video container conversions
;= toavi=mencoder -ovc copy -oac copy -of avi -o $*.avi $*
;= tomp4=mencoder -ovc copy -oac copy -of lavf -o $*.mp4 $*
;= tomkv=%~d0\PortableApps\MKVtoolnix\App\mkvmerge.exe -o $*.mkv $*
;= ALTERNATIVE: tomkv=mencoder -ovc copy -oac copy -of lavf -o $*.mkv $*
;= toogm= -> use ogmtools?
;= ALTERNATIVE: toogm=mencoder -ovc copy -oac copy -of lavf -o $*.ogm $*

;= mtrim=mencoder -oac copy -ovc copy $* -o $*_TRIM -ss hh:mm:ss -endpos hh:mm:ss 
;= audiotrim=
;= mp3trim=if [$2]==[] ( echo usage: mp3trim [input file] [start position] [lenght]) else ( ffmpeg -ss $2 -t $3 -i "$1" -acodec copy "$~n1_TRIM.$~x1" )
;= mp3splt=...
;= oggtrim

;= timidity=pmidi $*
;= fluidsynth=pmidi $*
pm=pmidi $*

;= i=info.bat $*
mi=mediainfo $*
;= mid=mplayer -identify -vo null -ao null -frames 0 $* 2^> nul | findstr ID

;= id3edit, id3tool, tag

;= oggenc=oggenc2 $*
;= aacenc=faac $*
;= aacdec=faad $*
;= toolame=twolame $*
;= mp2enc=twolame $*
;= mp3enc=lame $*
;= mp3dec=lame --decode $*
;= ape=mac $*
;= unape=mac $*
;= axxenc=aften $*
;= axxdec=ffmpeg -i $* -target wav $*.wav

mp3gainall=mp3gain /r /c /T *.mp3
;= mp3gaintrack=mp3gain /r /k /T /p *.mp3
;= mp3gainalbum=mp3gain /a *.mp3
;= normalize=aacgain $*
;= wavgain=wavegain $*

;= splitcuemp3=mp3splt -c $*.cue -o "@a - @b - @n - @t" $*.mp3
;= splitcueogg=mp3splt -c $*.cue -o "@a - @b - @n - @t" $*.ogg
;= splitcuemp3=shntool split $*.mp3 -f $*.cue -t "%p - %a - %n - %t" -d . -o 'cust ext=mp3 lame --quiet -  %f' ;= MEMO: mp3 input unsupported?
cuesplitflac=shntool split *.flac -f *.cue -t "%p - %a - %n - %t" -o flac
;= cuesplitape=shntool split *.ape -f *.cue -t "%p - %a - %n - %t" -o flac
;= splitcuewav=shntool split *.wav -f $*.cue -t "%p - %a - %n - %t" -o flac

2chd=chdman createcd -i $*

ff=firefox $*
;= iceweasel=firefox $*
;= wp=firefox "http://en.wikipedia.org/w/index.php?title=Special%3ASearch&search=$1+$2+$3+$4+$5+$6+$7+$8+$9"
;= google=html2txt "http://www.google.com/search?q=$*" | head
google=firefox -new-tab "http://www.google.com/search?q=$*"
;= wiki=html2txt "http://en.m.wikipedia.org/wiki/$*" | less
wiki=firefox "http://en.wikipedia.org/w/index.php?title=Special%3ASearch&search=$1+$2+$3+$4+$5+$6+$7+$8+$9"

;= httrack=execext httrack $*

;= youtube-dl=clive $*
;= youtubedl=clive $*
youtubedl=youtube-dl $*
ytdl=youtube-dl $*
mediaurlget=youtube-dl --get-url $*
videourlget=youtube-dl --get-url $*

;= ip=netsh $*
;= ip=ipget
;= myip=ipget
getip=ipget
;= showip=ipget
;= newip,renewip=ipconfig /flushdns ^& ipconfig /release ^& ipconfig /renew

wake=power on $*
shut=power off $*
shutmon=power off monitor
;= dpmsoff=power off monitor
;= monoff=power off monitor
;= status=power status $*
lshosts=power status all

;= avscan=av $*
;= avcls=av $*
;= clamscan=av $*
;= avmem=... $t clamscan --memory

plot=gnuplot -persist -e "plot $*"
;= maxima=pylab $*
;= simpy=isympy $*
;= sympy=isympy $*
;= isimpy=isympy $*
;= isympy=bc $*
;= pylab=ipython --pylab $*

;= bash=sh $*
;= csh=sh $*
;= ksh=sh $*
;= zsh=sh $*

;= set BOXES=%~dp0boxes-1.1\boxes.cfg
;= boxes=boxes -f "%~dp0boxes-1.1\boxes.cfg" $*
;= cowsay=boxes ...
;= figlet=banner $*
;= toilet=banner $*

;= edit=%EDITOR% $*
edit=%VISUAL% $*
;= mcedit=mc -e $*

;= qb=fbc -lang qb $*
;= basic=fbc -lang deprecated -x "%TEMP%\a.exe" $* ^& "%TEMP%\a.exe"
;= qbasic=fbc -lang qb -x "%TEMP%\a.exe" $* ^& "%TEMP%\a.exe"

;= pascal=fpc $*
;= tpc=fpc -Mtp $*
;= dcc32=fpc -Mdelphi $*

;= javac="%JDK_HOME%\bin\javac.exe" $* -> MOVED IN javac.bat
;= applet=%JDK_HOME%\bin\appletviewer.exe $*
;= javadoc=%JDK_HOME%\bin\javadoc.exe $*
;= ant="%~d0\PortableApps\Eclipse\plugins\org.apache.ant_1.7.1.v20100518-1145\bin\ant.bat" $*

;= java2=%MINGW_HOME%\bin\gij $*
;= gcj=%MINGW_HOME%\bin\gcj -C $*
;= java2exe=%MINGW_HOME%\bin\gcj $*.java --main=$* -o $*.exe
;= class2exe=%MINGW_HOME%\bin\gcj $*.class --main=$* -o $*.exe

;= doxy=echo EXTRACT_ALL=YES $b doxygen -
;= javadoc=doxygen $*

;= dosemu=dosbox $*
;= mameinfo=mame -listroms $*
;= mamecmp=mame -romident $*
oldmame=mameold $*
fastmame=mameold $*

mednafen=execext mednafen $*
desmume=execext desmume $*
;= nestopia=execext nestopia .\$* -> MOVED IN nestopia.bat
;= snes9x=%~d0\PortableApps\Snes9x\snes9x.exe %CD%$*
;= gens=start "Gens32" /D "%~d0\PortableApps\Gens32" /B "Gens32 Surreal.exe" %CD%$*
;= regen=%~d0\PortableApps\Regen\Regen.bat %CD%\$*
;= vbam=%~d0\PortableApps\VisualBoyAdvance\VisualBoyAdvance-M.exe $*
;= epsxe=%~d0\PortableApps\ePSXe\ePSXePortable.bat %CD%$*
;= mupen64=%~d0\PortableApps\Mupen64Plus\Mupen64PlusPortable.bat $*
dolphin=execext dolphin $*
;= x64=vice $*
;= zzt=%~d0\PortableApps\DreamZZT\DreamZZTPortable.bat %CD%$*
uae=execext WinUAE $*
openmsx=execext openmsx $*
;= ssnes=retroarch $*
ra=retroarch $*

good="%~dp0GoodTools\good$1.exe" $2 $3 $4 $5 $6 $7 $8 $9 nodb
;= goodgba="%~dp0GoodTools\goodgba.exe" $2 $3 $4 $5 $6 $7 $8 $9 nodb
;= ...

ips=if [$2]==[] ( echo usage: ips [rom file] [ips file] ) else ( ucon64 --nbak -i $* )
aps=if [$2]==[] ( echo usage: aps [rom file] [aps file] ) else ( ucon64 --nbak -a $* )
ppf=if [$2]==[] ( echo usage: ppf [rom file] [ppf file] ) else ( ucon64 --nbak --ppf $* )
mkips=if [$2]==[] ( echo usage: mkips [original] [patched] ) else ( ucon64 --mki=$* )
mkppf=if [$2]==[] ( echo usage: mkips [original] [patched] ) else ( ucon64 --mkppf=$* )
;= more patch formats:
;=  .pat -> fc /b >output.pat
;=  BSDiff -> http://www.daemonology.net/bsdiff/
;=  rup (NINJA 2.0) -> http://www.romhacking.net/utilities/329/  https://github.com/sobodash/ninja2
;=  UPS (discont.) -> byuu's upset http://www.romhacking.net/utilities/677/
;=  bps -> byuu's beat http://www.romhacking.net/utilities/893/
;=  JFP -> http://www.romhacking.net/utilities/767/
;=  FFP, FPM (FireFlower Patches)
;=  rxl (discont.) -> http://www.romhacking.net/utilities/7/ http://segaretro.org/RXL
;=  pds (NDS only) http://www.romhacking.net/utilities/320/
bps=if [$2]==[] ( echo usage: bps [rom file] [bps file] ) else ( %~dp0flips-1.31\flips.exe  --apply $2 $1 )
gg=ucon64 --nbak --gg=$*
fixhead=ucon64 --nbak --chk $*
fixrom=ucon64 --nbak --chk $*
fixromhead=ucon64 --nbak --chk $*
;= mkdat=ucon64 --mkdat=$*
REM byte swap: 1234 -> 2143
byteswap=ucon64 --nbak --swap $*
REM word swap: 1234 -> 3412
byteswap2=ucon64 --nbak --swap2 $*
wordswap=ucon64 --nbak --swap2 $*

;= dldi=dlditool $*
;= dldir4=dlditool r4tf.dldi $*
;= dldiez5=dlditool EZ5V2.dldi $*
;= dldiez5i=dlditool EZ5V2.dldi $*
;= dldiezvi=dlditool EZ5V2.dldi $*
;= dldifcsr=... -> ...\fcsr.dldi.cmd

speak=say $*
parla=di $*
;= ALTERNATIVE NAMES: voice, talk
;= readfile=espeak -v en -f $*
;= txt2wav=espeak -f $1 -w $2 $3 $4 $5 $6

;= del=del /p $*

;= geturl=wget $*
get=wget $*
;= fetch=wget $*
;= download=wget $*
;= wcat=wget --quiet -O - $* -> MOVED IN wcat.bat
winfo=wget -S --spider $*
wheaders=wget -S --spider $*
;= winfo=curl --head --verbose --output NUL $*
wput=curl --upload-file $*
;= put=curl --upload-file $*
;= get=curl $*
;= upload=publish $*
upload=curl --upload-file $*
;= getmd5=curl --head $* | findstr "Content-MD5" -> MOVED in whash.bat
getmd5=whash $*
gethash=whash $*
ftpls=curl --list-only $*
;= lsftp=curl --list-only $*

netcat=nc $*
ncat=nc $*
sock=nc $*
socket=nc $*
server=nc -v -l $*
;= listen=nc -v -l $*
client=nc -v $*
connect=nc -v $*

;= hdoff=hdparm -y hda
;= slowcd=hdparm -E1 scd0 ;= unsupportd?
;= cdspeed -> read/modify current cd speed

;= fake logical drives:
;= floppy:=a:
;= fd:=a:
;= cd:=%CD_DRIVE%
;= dvd:=%CD_DRIVE%
;= mem:=r:
;= ram:=r:

ispell=spell $*
aspell=spell $*
hunspell=spell $*
speel=spell $*

;= desc=file $*
;= describe=file $*
getmime=file --mime-type $*

info=fileinfo $*
finfo=fileinfo $*
check=filecheck $*
filetest=filecheck $*
verify=filecheck $*
test=filecheck $*
valid=filecheck $*
fix=filefix $*
repair=filefix $*
new=filenew $*
create=filenew $*
crack=filecrack $*
convert=fileconvert $*
taggrep=filetaggrep
id3grep=filetaggrep

;= massconvert=dir /B $1 $B xargs -I {} fileconvert {} $2
;= massconvert=FOR /F "delims=" %F IN ('dir /B $1') DO @fileconvert "%F" $2
convertall=FOR /F "delims=" %F IN ('dir /B $1') DO @fileconvert "%F" $2
recursive=FOR /F "delims=" %F IN ('dir /B .') DO @$* "%F"
;= recursive=find . -exec $* "{}" \;
;= recursive=find . $B xargs $*
;= recursive=dir /B /S $B xargs $*

;= sum=busybox sum $*
;= cksum=busybox cksum $*

;= if exist "%~dp0rhash.*" (
;= hash=rhash --printf "%p\n CRC32: %C\n MD5: %M\n SHA1: %H\n ED2K: %E\n TTH: %T\n" $* -> MOVED IN hash.bat
sfv=rhash --crc32 --sfv $*
;= crc32=rhash --crc32 --simple $*
;= md5=rhash --md5 $* -> MOVED IN md5.bat
sha1=sha1sum $*
sha256=rhash --sha256 $*
ed2k=rhash --ed2k-link $*
;= magnet=rhash --magnet $*
;= sum=rhash --crc32 ... $*
;= cksum=rhash --crc32 ... $*
;= )

par=par2 $*
parv=par2 v $*
parcreate=par2 c $*
par2verify=par2 v $*
par2repair=par2 r $*

;= xdelta=xdelta3 $* -> NOT COMPATIBLE http://code.google.com/p/xdelta/issues/detail?id=40
;= vcdiff=xdelta3 $*

;= dialup=rasdial Tiscali cm2005 tiscali /PHONE:7023456789
;= dialoff=rasdial $1 /DISCONNECT

ocr=file2txt $*
;= gocr=%MAGICK_HOME%\convert.exe $* pnm:- | gocr -
;= ocrad=%MAGICK_HOME%\convert.exe $* -depth 8 pnm:- | ocrad -
;= tesseract=%MAGICK_HOME%\convert.exe $* tif:- | tesseract -
;= ocr=%MAGICK_HOME%\convert.exe $* pnm:- | gocr -
;= img2txt=ocr $*
;= img2txt=jave $*
;= txt2img=cat $* $B %MAGICK_HOME%\convert.exe label:@- $*.png
;= http://www.imagemagick.org/Usage/text/

;= txt2htm=txt2tags -v -t html $*
;= txt2html=txt2tags -v -t html $*
;= html2text=html2txt $*
;= html2markdown=html2txt $*
;= lynx=html2txt $*
;= links=html2txt $*
;= w3m=html2txt $*

;= xplanet=start "XPlanet" /d "%PROGRAMFILES%\XPlanet" /b xplanet.exe -searchdir "%HOME%\Documenti\Immagini\Astronomia\Mappe" -starmap BSC -label -num_times 1 $*

;= starthi=start "" /HIGH $*
;= startlo=start "" /LOW $*


;= http://djvu.sourceforge.net/doc/index.html
;= djvu encoders
;= NO? http://djvu.sourceforge.net/doc/man/djvudigital.html
	;= djvu compression in high color (for photos)
	;= ppm2djvu-hi=%DJVULIBRE_HOME%\c44.exe $*
	;= djvu compression for low colors (paletted)
	;= ppm2djvu-lo=%DJVULIBRE_HOME%\cpaldjvu.exe $*
	;= djvu compression for black and white (bitonal)
	;= pbm2djvu-bw=%DJVULIBRE_HOME%\cjb2.exe $*
;= djvu decoders
;= ddjvu=%DJVULIBRE_HOME%\ddjvu.exe $*
;= djvu2tiff=%DJVULIBRE_HOME%\ddjvu.exe -format=tiff $* $*.tif
;= djvu2ps=%DJVULIBRE_HOME%\djvups.exe
;= djvu2pdf=

;= mantoxhasitup=ftp -s:%~dp0mantoxhasitup.ftp mantox.altervista.org

;= silent=quiet $*

findup=dupfind $*
;= dupfinde=dupfind $*
fdupes=dupfind $*
fdup=dupfind $*
;= dupefind=dupfind $*
finddup=dupfind $*

;= zbar=zxing $*
;= zint=zxing --encode $*
;= barcoded=zxing $*
;= barcodec=zxing $*
;= bardecode=zxing $*
;= barcodenc=zxing --encode $*

cf=codfisc $*

;= renointro2good=rennointro2good $*
;= nointro2good=rennointro2good $*
;= renn2g=rennointro2good $*

;= wificrack=wifikeygen $*
;= crackwifi=wifikeygen $*

;= arj=7z $*
uharc=arc $*
unuharc=arc $*

;= od=hexdump $*
;= dump=hexdump $*
;= xxd=od $*
hexview=hexdump $*
;= hexcat=hexdump $*
;= bincat=hexdump $*
;= hexfind=sfk hexfind $*
hexfind=hexgrep $*
bingrep=hexgrep $*
binreplace=hexreplace $*
hexhead=hexdump -n 200 $* $B head
;= SLOW: hextail=hexdump $* $B tail
hextail=tail $* $B hexdump
;=                               http://stackoverflow.com/questions/232212/binary-tail-a-file
;= hexedit=vim -c ":%!xxd" $*
;= hexedit=vim -b $*
;= hexedit=most $*
;= hexedit=hex $*
;= subfile=dd if=$1 of=$1.sub bs=1 skip=$2 count=$3 -> extract part of a file
;=                                            ^ offset  ^ bytes to extract
hexdiff=hexcmp $*
diffhex=hexcmp $*

;= extract a part of a file
;= bincut=dd if=$1 of=$1.sub bs=1 skip=$2 count=$3
;= fcut=dd if=$1 of=$1.sub bs=1 skip=$2 count=$3

addromhead=ucon64 --nbak --ins $*
delromhead=ucon64 --nbak --stp $*
;= trim=trimrom $*
romtrim=autotrimrom $*
trimrom=autotrimrom $*

addhead=ucon64 --nbak --insn=$2 $1
;= ALTERNATIVEs: dd if=$1 of=$1.head bs=1 seek=$2, type ..., NO(only for text files)? sfk addhead $*

rmhead=ucon64 --nbak --stpn=$2 $1
delhead=ucon64 --nbak --stpn=$2 $1
strphead=ucon64 --nbak --stpn=$2 $1
trunchead=ucon64 --nbak --stpn=$2 $1
;= ALTERNATIVEs: dd if=$1 of=$1.nohead bs=1 skip=$2

addtail=truncate -c -s+$2 $1
pad=truncate -c -s+$2 $1
grow=truncate -c -s+$2 $1
grown=truncate -c -s+$2 $1
;= ALTERNATIVEs: ucon64 --padn=$2 $1, echo $2 ^>^> $1, NO(only for text files)? sfk addtail $*

rmtail=truncate -c -s-$2 $1
strip=truncate -c -s-$2 $1
;= ALTERNATIVEs: ucon64 --strip=$2 $1

;= savegames file formats converters:
;= gcs2gci= ucon64 --stpn=272 -> MOVED IN fileconvert.bat
;= TODO: xps2sav, sps2sav -> need to look for binary delimiters? -> use http://www.oocities.org/xps2sav/
;= xps2sav=%~dp0_TESTING\xps2sav.exe $*
;= sps2sav=%~dp0_TESTING\xps2sav.exe $*
;= TODO: gsv2sav=...
;= TODO: more http://www.gamefaqs.com/ps2/920640-wwe-smackdown-vs-raw/faqs/34492

ximage=dism $*
imagex=dism $*

findcolor=colorsearch $*
;= colors=colorsearch $*
;= color=colorsearch $* -> ovverides console buitin command
colorname=colorsearch $*

;= colorize=grc $*
;= ping=grc ping $*
;= traceroute=grc traceroute $*
;= netstat=grc netstat $*
;= ports=grc netstat $*
;= connections=grc netstat $*
;= colorgcc=grc gcc $*
;= colordiff=grc diff $*

;= ansiecho=ansicon -e *$
;= colorecho=ansicon -e $*
;= ALTERNATIVE: sfk echo ... http://stahlworks.com/dev/index.php?tool=echo

oo=loffice $*
lo=loffice $*

py=python $*
;= python2=python $*
;= python3=unix python3 $*
pyton=python $*
pithon=python $*
piton=python $*
pydoc=python -c "help('$*')"
pyman=python -c "help('$*')"
pyhelp=python -c "help('$*')"
;= ALTERNATIVE: python "%PYTHONHOME%\Lib\pydoc.py" $*

;= play=computer play $*
;= pause=computer pause
;= stop=computer stop
;= next=computer next
;= prev=computer prev
;= weather=computer weather
;= news=computer news
news=start "" "http://eadmaster.altervista.org/pub/index.php?page=feeds"
calendar=start "" "http://calendar.google.com"
;= events=computer calendar
;= today=computer today
;= day=computer date
;= date=computer date
;= week=computer today
;= clock=computer time
;= hour=computer time
;= tv=computer tv $*
;= cinema=computer cinema $*
;= shoplist=computer shoplist $*
;= wall=computer wallpaper $*
;= wallpaper=computer wallpaper $*

;= tv=start "" ""

;= voipcall=sipcall $*
;= call=sipcall $*
;= tel=sipcall $*
;= phone=sipcall $*

;= cellcall=gammu nothing --dialvoice $*
;= cellsendsms=gammu nothing --sendsms $*
;= cellreadsms=gammu nothing --geteachsms
;= cellstatus=gammu nothing --getdisplaystatus
;= cellmonitor=gammu nothing --monitor
;= altri nomi: mcall, msms, telcall, telsmsm, pcall, psms
;= TODO: forzare lettura profili da "%~dp0gammurc" ?

contactsearchs=contactsearch $*
contact=contactsearch $*
contacts=contactsearch $*
rub=contactsearch $*
tel=contactsearch $*
;=    ALTERNATIVE: %MAILER% -addressbook

;= findrfc=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\standard\ietf\rfc-ref.txt"
;= rfc=wget --quiet -O - "http://www.ietf.org/rfc/rfc$1.txt" $B less
;= findiso=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\standard\iso\_List.txt"
;= findieee=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\standard\ieee\OPACStdList.txt"
findport=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\standard\iana\port-numbers"
;= findposix=for %F in (%PENDRIVE%\Documents\db\standard\posix\*.zip) do @filegrep $* "%F"
findstandard=findstr /S /I /P /C:"$*" "%PENDRIVE%\Documents\db\standard\*.*"

listen=play $*
;= tunein=play $*
webradio=play radio $*

;= load=set$*
;= init=set$*

;= setenv=...
unset=set $1=

igrep=grep -i $*
rgrep=grep -r $*
egrep=grep -E $*
fgrep=grep -F $*
zgrep=filegrep $*
fuzzygrep=ugrep --ignore-binary --ignore-case --hidden -Z2 $*

catalog=rhash --crc32 --sfv -r --ansi $*
;= ALTERNATIVE: datutil ..., ucon64 --mkdat=$*
locate=havesearch $*
finddisk=havesearch $*
findbackup=havesearch $*
whereis=havesearch $*
;= ALTERNATIVE NAMES: where, whereisit, ...

datfind=dumpsearch $*
datsearch=dumpsearch $*
;= findrom=dumpsearch $*
;= findgame=dumpsearch $*
;= findiso=dumpsearch $*
;= romfind=dumpsearch $*
;= romsearch=dumpsearch $*
;= romsfind=dumpsearch $*
;= isofind=dumpsearch $*
;= gamesearch=vgsearch $*
vgsearch=filegrep $* %PENDRIVE%\Documents\db\vg
downloadsearch=filegrep -l $* %PENDRIVE%\Documents\db\download
geosearch=filegrep $* %PENDRIVE%\Documents\db\geo

;= findarcade=for %F in (%PENDRIVE%\Documents\db\datfile\arcade\*.zip) do @filegrep $* "%F"
;= findgb=for %F in (%PENDRIVE%\Documents\db\datfile\GameBase\*.zip) do @filegrep $* "%F"
;= findscene=for %F in (%PENDRIVE%\Documents\db\datfile\scene\*.zip) do @filegrep $* "%F"
;= findscene=filegrep $* "%PENDRIVE%\Documents\db\datfile\scene\PREDATE.zip"
magsearch=for %F in (%PENDRIVE%\Documents\db\index\*.zip) do @filegrep $* "%F"
magssearch=for %F in (%PENDRIVE%\Documents\db\index\*.zip) do @filegrep $* "%F"
goodsearch=for %F in (%PENDRIVE%\Documents\db\datfile\GoodTools\*.zip) do @filegrep $* "%F"
nointrosearch=filegrep $* "%PENDRIVE%\Documents\db\datfile\No-Intro*.zip"
tosecsearch=for %F in (%PENDRIVE%\Documents\db\datfile\tosec*.zip) do @filegrep $* "%F"
redumpsearch=for %F in (%PENDRIVE%\Documents\db\datfile\redump*.zip) do @filegrep $* "%F"

psxsearch=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\ps1\sonyindex_PSone*.txt"
ps1search=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\ps1\sonyindex_PSone*.txt"
ps2search=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\ps2\sonyindex_PS2*.txt"
ps3search=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\ps3\ps3tdb.txt"
ps4search=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\ps4\*.*"
pspsearch=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\psp\sonyindex_PSP*.txt"
ngcsearch=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\wii\wiitdb_titles.txt"
wiisearch=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\wii\wiitdb_titles.txt"
wiiusearch=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\wiiu\wiiutdb_titles.txt"
;= wiifindgameid=findstr /I /C:"$*" ""%~dp0wit-2.31a\titles.txt"
3dssearch=busybox awk -v "IGNORECASE=1" -v RS="{" "/$*/" "%PENDRIVE%\Documents\db\vg\3ds\list_*.json"
nswsearch=busybox awk -v "IGNORECASE=1" -v RS="{" "/$*/" "%PENDRIVE%\Documents\db\vg\nsw\*.json"
;= wiitdb=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\wii\wiitdb_titles.txt"
xboxsearch=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\xbox\xbox_titleids.tsv"
xb360search=findstr /I /C:"$*" "%PENDRIVE%\Documents\db\vg\xb360\gamesdatabase_*.tsv"
gbasearch=filegrep $* "%PENDRIVE%\Documents\db\datfile\ADVANsCEne_Release_Dat_2792.zip"
;= wadsearch=filegrep $* "%PENDRIVE%\Documents\db\datfile\Wads.zip"
;= mamesearch=for %F in (%PENDRIVE%\Documents\db\datfile\arcade\MAME*.zip) do @filegrep $* "%F"
messsearch=mame -listsoftware $1 | awk -v 'IGNORECASE=1' -v RS="<software" '/'"$2"'/ { print $0 }'

;= findgog=...
;= findcheat=... %PENDRIVE%\Documents\db\cheat

extsearch=findstr /I $* %PENDRIVE%\Documents\db\file\headers.ini
headersearch=findstr /I $* %PENDRIVE%\Documents\db\file\headers.ini

unitsearch=findstr /I $* %PENDRIVE%\Documents\db\misc\units.dat
langsearch=findstr /I $* %PENDRIVE%\Documents\db\dict\languages.csv
;= domsearch=findstr /I $* %PENDRIVE%\Documents\db\dict\languages.csv
countrysearch=findstr /I $* %PENDRIVE%\Documents\db\geo\countries.csv
currencysearch=findstr /I $* %PENDRIVE%\Documents\db\finance\currency.csv
moneysearch=findstr /I $* %PENDRIVE%\Documents\db\finance\currency.csv
;= citysearch=grep -A 8 -B4 $* %PENDRIVE%\Documents\db\geo\cities.dat -> MOVED IN findcity.bat
abbrsearch=findstr /I $* %PENDRIVE%\Documents\db\dict\abbrevs.*

findnote=notesearch $*

mailsearch=emailsearch $*
findemail=emailsearch $*

findproto=findcproto $*
findfunc=findcproto $*

findhdext=finddoc $*
findoc=finddoc $*

;= splint=lint $*
cppcheck=lint $*
;= pylint=lint $*
;= xmllint=lint $*
xmlint=xmllint $*
xmlstarlet=xml $*

;= astyle=%PROGRAMFILES%\UniversalIndentGUI\indenters\astyle.exe $*
;= indent=%PROGRAMFILES%\UniversalIndentGUI\indenters\indent.exe $*
;= htmltidy=tidy $*
;= tidyhtml=tidy $*
;= ...=%PROGRAMFILES%\UniversalIndentGUI\indenters\....exe

;= dialect=talkfilter $*
;= slang=talkfilter $*
;= filter=talkfilter $*
;= leet=talkfilter warez $*
;= l33t=talkfilter warez $*
;= chat=talkfilter b1ff $*
;= german=talkfilter kraut $*
;= pirate=talkfilter pirate $*

;= 2FIX: cannot use redirection? "< input.txt"
;= filter=sed -e "s/$1/$2/g"
;= replace=sed -e "s/$1/$2/g"

frag=defrag -a $*
frags=defrag -a $*

;= NO(clash with %WINDIR%\System32\recover.exe)? recover=undelete $*

zipcrack=crack $*
rarcrack=crack $*
7zcrack=crack $*
pdfcrack=crack $*

;= fslint=detox $*
saferen=detox $*
rensafe=detox $*
sren=detox $*
;= renfix=detox $*

;= nbzget=nzbget $*

;= mkbook=pdfbook $*
;= booklet=pdfbook $*

bb=busybox $*
;= gnu=unix $*
;= util=unix $*
;= coreutil=unix $*
;= gnuwin32=unix $*
;= mingw=unix $*
;= cygwin=unix $*
;= uwin=unix $*
strlen=expr length "$*"
length=expr length "$*"
;= file2c=sfk bin-to-src $*

;= df=df -h -T -P $*
;= du=du -hac $*
;= dirsize=du -hs $*

;= timer=sleep $* -> MOVED IN timer.bat

;= cvsget=...
;= svnget=...
hgget=hg clone $*
hget=hg clone $*
gitget=git clone $*

aria=aria2 $*

gawk=awk $*

;= sound=nircmd beep $*
;= filter=grep $*

;= stamp=touch $*
;= timestamp=touch $*
;= redate=touch -c -d $*
;= restamp=touch -c -d $*
setdate=touch -c -d $*
chdate=touch -c -d $*
;= supported timestamp formats: "2004-02-29  16:21:42" , "YYYYMMDDhhmm"
cpdate=touch -c -r $*
datecp=touch -c -r $*

;= 4dir=if exist descript.ion ( type descript.ion ) else ( dir /b ) -> MOVED IN 4dir.bat
;= nfo=type file_id.diz descript.ion

;= mktgz=tar -cvzf $*
;= mktgz=filepack $*

;= iniman=%~dp0_CANCELLARE\WindowsServer2003-ResourceKitTools-28.04.2003\iniman.exe $*
;= Instsrv=%~dp0_CANCELLARE\WindowsServer2003-ResourceKitTools-28.04.2003\Instsrv.exe $*

;= ttcp=curl -o NUL "http://speedtest.qsc.de/1GB.qsc"
;= netbench=curl -o NUL "http://speedtest.qsc.de/1GB.qsc" -> MOVED IN netbench.bat
netspeed=netbench $*
nspeed=netbench $*
iperf=netbench $*

;= binpack=ssbp $*
;= fit=ssbp $*

;= xattr=dir /r $* -> MOVED IN xattr.bat
;= adscat=more < $* -> MOVED IN xattr.bat
;= rmads=%SYSINTERNALS_PATH%\streams.exe -d $* -> MOVED IN xattr.bat
;= ALTERNATIVES: %~d0\PortableApps\NirLauncher\NirSoft\alternatestreamview.exe, altstreamdump.exe (view only)

;= bluez=control /name Microsoft.BluetoothDevicesnager
;= hcitool=control /name Microsoft.BluetoothDevicesnager
;= hciconfig=control /name Microsoft.BluetoothDevicesnager
;= ... (see bluez-utils)
;= ALTERNATIVES: (DISCONT.)? https://sourceforge.net/projects/forkbeard/ , BluetoothCLTools (closed source) http://bluetoothinstaller.com/bluetooth-command-line-tools/ , %~d0\PortableApps\NirLauncher\NirSoft\bluetoothcl.exe (list infos only), http://www.nirsoft.net/utils/bluetooth_viewer.html /try_to_connect <MAC Address>
;= btftp=%~dp0_TESTING\BluetoothCLTools-1.2.0.56\bin\btftp.exe $*
;= btftp=%~dp0_TESTING\forkbeard-0607\opptool.exe $*

;= un=units $*
unit=units $*
;= uconvert=units $*

;= recode=iconv $*
;= uconv=iconv $*
toutf=iconv -t UTF-8 $*
;= u2d=unix2dos $*
todos=unix2dos $*
;= d2u=dos2unix $*
tounix=dos2unix $*

;= csvgrep=csv grep $*
;= csvcut=csv cut $*
;= csvsort=csv sort $*

inigrep=awk '/$1/' RS=[ $2
;= xmlgrep=awk '/$1/' ...

;= avconv=ffmpeg $*

;= appendnote=mynoteappend $*
;= na=mynoteappend $*
np=mynoteappend $*

lsservices=service list
;= network=service networking $*
;= netstart=networking start
;= netstop=networking stop
nstart=service networking start
nstop=service networking stop
smbstart=service samba start
smbstop=service samba stop
pcapstart=service pcap start
pcapstop=service pcap stop
;= tapstart=service tap start
;= tapstop=service tap stop
avstart=service antivirus start
avstop=service antivirus stop
setsoftap=service softap start

;= httpd=uhttpd $*
;= https=uhttpd $*
uhttpd=service http $*
;= serve=uhttpd $*
;= ftpd=uftpd $*
;= ftps=uftpd $*
uftpd=service ftp $*
usftpd=service sftp $*

;= respool=sudo net stop spooler ^& sudo net start spooler
respool=printflush
;= ALTERNATIVE: %~dp0_CANCELLARE\WindowsServer2003-ResourceKitTools-28.04.2003\cleanspl.exe

;= cdstart=sudo devcon enable %CD_DEVICE_ID%
;= cdstop=sudo devcon disable %CD_DEVICE_ID%

;= parallel port disable|enable (requires reboot)
;= ppstart=devcon enable "ACPI\PNP0401"
;= ppstopt=devcon disable "ACPI\PNP0401"

;= linux=colinux $*
;= linuxstart=colinux start
;= colinuxstart=colinux start
;= colinuxstop=colinux start
lxstart=service linux start
lxstop=service linux stop
;= TODO: lstart|lrun

;= win31=qemu_win31 $*
;= win31=dosbox_win31 $*
;= win98=qemu_win98 $*
;= macos=qemu_macos $*

;= cleanup=cleansys

;= clip=pbcopy $*
putclipboard=pbcopy $*
getclipboard=pbpaste $*

;= nw=netwox $*

;= fatdir=dir /... (list unsorted)
;= udir=dir

resetip=ipset dynamic
resetdns=dnsset default

setres=nircmdc setdisplay $1 $2 24
;= resetres=MultiMonitorTool /setmax 1
setgamma=gamma $*

setrotation=MultiMonitorTool /SetOrientation 1 $*
resetrotation=MultiMonitorTool /SetOrientation 1 0 2 0 
;= setportrait=MultiMonitorTool /SetOrientation 1 90

dec2hex=printf "%%x\n" $1
dec2oct=printf "%%o\n" $1
bin2hex=python -c "print(hex(int(\"$1\", base=2))[2:]);"
bin2dec=python -c "print(int(\"$1\", base=2));"
dec2bin=python -c "print(bin(int(\"$1\"))[2:]);"
hex2dec=SET /A _Result = 0x$1
;= ALTERNATIVE: hex2dec=printf "%%d\n" 0x$1
oct2dec=SET /A _Result = 0$1
dec2sci=printf "%%e\n" $1
sci2dec=printf "%%.96f\n" $1 ^| sed "s/0\+$//"

recmic=record mic $*
micrec=record mic $*

trans=translate $*

;= sr=record $*

setvol=volumeset $*
unmute=umute

csv=csvtool $*
sumlines=csvtool sum 1

phpinfo=php -r "phpinfo();"

setds2=setds3

gdrivels=rclone ls gdrive:$* --max-depth 1 -q
gdrivelsl=rclone lsl gdrive:$* --max-depth 1
;= gdrivecp=rclone copy $* -v
gdriveget=rclone copy gdrive:$* . -v
;= gdriveput=rclone copy $1 gdrive:$2 -v  -> MOVED IN SCRIPT
gdrivefind=rclone ls  gdrive:  --ignore-case --include "*$**"
gdriverm=rclone delete gdrive:$* -v
gdrivedel=rclone delete gdrive:$* -v
gdrivecat=rclone cat gdrive:$*
gdrivemount=rclone mount gdrive: G: --vfs-cache-mode writes
;= TODO: --daemon;
;= gdriveumount=
eadmastertkput=rclone copy $1 eadmastertk:$2 -v

share=smbshare $*
unshare=smbsharerm $*

pkg=package $*
install=package install $*
uninstall=package uninstall $*
update=package update $*
upgrade=package update $*
debinfo=package info $*
debfind=package search $*
lsdeb=package list $*
apt=winget $*

portscan=nmap -v -p1-65535 $*
findport=findstr /I $* %WINDIR%\System32\drivers\etc\services
checkport=netstat -aon | findstr :$1
wholisten=netstat -aon | findstr :$1
;= checkport=sudo netstat -ab | findstr :$1
lsports=sudo netstat -ntb -p TCP $*
lsfd=handle $*
;= lsap=wifiscan

gettimestamps=timestamps
getepochtime=busybox date +%s
getunixtime=busybox date +%s
epochtime2human=busybox date -d @$1
epochtime2local=busybox date -d @$1
strftime=busybox date -d $2  +$1

loaddrv=sc create $*

;= getratio=echo $2 / $1 * 100 ^| bc -l 

routes=route PRINT

androiddevices=adb devices -l $*
androidls=adb shell ls -lis $*
androidget=adb pull $*
androidput=adb push $*
androidrm=adb shell rm $*
androidsh=adb shell $*
androidinstall=adb install $*
androidpower-button=adb shell "input keyevent 26"
androidvibrate=adb shell "echo 200 > /sys/devices/virtual/timed_output/vibrator/enable"
androidtype=adb shell input keyboard text $*
androidapps=adb shell pm list packages
androidrun=adb shell monkey -p $1 -c android.intent.category.LAUNCHER 1
androidshot=adb shell screencap $*
androidrecord=adb shell screenrecord $*
androidbattery=adb shell dumpsys batterymanager $*
androidsensors=adb shell dumpsys sensorservice $*
androidmount=rclone mount adb: A: --vfs-cache-mode writes
;= TODO: --daemon
;= android-umount=taskkill /f /im rclone.exe ..

;= findlatest=ls -R -t1 -l -p -h $* |  grep -v / |  head -n 5
zipfindlatest=7z l $* | findstr /L "....A" | sort | tail -n2
7zfindlatest=7z l $* | findstr /L "....A" | sort | tail -n2

countchars=tr -cd + < $* | wc -c

xmlencode=sh %~dp0bin\xmlencode $*
xmldecode=sh %~dp0bin\xmldecode $*
urlencode=sh %~dp0bin\urlencode $*
urldecode=sh %~dp0bin\urldecode $*

chromeapp=chrome -app=$*

;= search=websearch $*

;= Wireless Network Watcher (fing alternative, GUI only) https://www.nirsoft.net/utils/wireless_network_watcher.html
findnearby=%SYSINTERNALS_PATH%\..\NirSoft\wnetwatcher.exe
;= Nirsoft CurrPorts  (opened ports lister) https://www.nirsoft.net/utils/cports.html
portsopenls=%SYSINTERNALS_PATH%\..\NirSoft\x64\cports.exe
;= SmartSniff (Win only) http://www.nirsoft.net/utils/smsniff.html
snifftraffic=%SYSINTERNALS_PATH%\..\NirSoft\x64\smsniff.exe
;= DnsLookupView (monitor DNS queries, GUI only) https://www.nirsoft.net/utils/dns_lookup_view.html
sniffdns=%SYSINTERNALS_PATH%\..\NirSoft\dnslookupview.exe
;= sniffdns=%SYSINTERNALS_PATH%\..\NirSoft\x64\dnsquerysniffer.exe
sniffpass=%SYSINTERNALS_PATH%\..\NirSoft\x64\sniffpass.exe
;= setdns=%SYSINTERNALS_PATH%\..\NirSoft\quicksetdns.exe
wifiscan=%SYSINTERNALS_PATH%\..\NirSoft\wifiinfoview.exe

