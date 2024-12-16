@echo off

call lsblk

echo "performing SMART checks..."
wmic diskdrive get status
call smartctl -a /dev/hda
call smartctl -a /dev/hdb
call smartctl -a /dev/hdc
