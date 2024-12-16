@echo off
setlocal

REM call mynotes mess

REM set MESSCMD="%~d0\PortableApps\MESS\mess.exe" -inipath "%~d0\PortableApps\MESS\ini"
if exist %~d0\Games\MAME\negamame64.exe set MESSCMD=start "MESS" /D "%~d0\Games\MAME" /B negamame64.exe -cfg_directory "%~d0\Games\MAME\cfg"
if exist %~d0\PortableApps\MESS\mess.exe set MESSCMD=start "MESS" /D "%~d0\PortableApps\MESS" /B mess.exe -inipath "%~d0\PortableApps\MESS\ini"
if exist %~d0\PortableApps\MESS\messpp.exe set MESSCMD=start "MESS" /D "%~d0\PortableApps\MESS" /B messpp.exe -inipath "%~d0\PortableApps\MESS\ini"
if exist "%ProgramFiles(x86)%" if exist %~d0\PortableApps\MESS\mess64.exe set MESSCMD=start "MESS" /D "%~d0\PortableApps\MESS" /B mess64.exe -inipath "%~d0\PortableApps\MESS\ini"

if not exist %1 goto classic_launch
echo ok
REM read input file extension
set "INPUTEXT=%~x1"

REM convert extension to lowercase
call :LoCase INPUTEXT

REM check extension from input file and set system and device
REM see also: mess -listdevices
if [%INPUTEXT%]==[.v64] (
    set SYSTEM=n64
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.z64] (
    set SYSTEM=n64
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.n64] (
    set SYSTEM=n64
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.vb] (
    set SYSTEM=vboy
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.gb] (
    set SYSTEM=gbcolor
    REM set SYSTEM=supergb
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.gbc] (
    set SYSTEM=gbcolor
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.gba] (
    set SYSTEM=gba
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.gen] (
    set SYSTEM=genesis
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.smd] (
    set SYSTEM=genesis
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.32x] (
    set SYSTEM=32x
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.sms] (
    set SYSTEM=smsj
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.gg] (
    set SYSTEM=gamegear
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.nes] (
    set SYSTEM=nes
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.fds] (
    set SYSTEM=famicom
    set DEVICE=flop
    )
if [%INPUTEXT%]==[.smc] (
    set SYSTEM=snes
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.sfc] (
    set SYSTEM=snes
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.fig] (
    set SYSTEM=snes
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.swc] (
    set SYSTEM=snes
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.pce] (
    set SYSTEM=tg16
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.sgx] (
    set SYSTEM=sgx
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.ws] (
    set SYSTEM=wswan
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.wsc] (
    set SYSTEM=wscolor
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.ngp] (
    set SYSTEM=ngp
    set DEVICE=cart
	echo MEMO: Press 'Q' to power on the console!
    )
if [%INPUTEXT%]==[.ngc] (
    set SYSTEM=ngpc
    set DEVICE=cart
	echo MEMO: Press 'Q' to power on the console!
    )
if [%INPUTEXT%]==[.sv] (
    set SYSTEM=svision
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.a26] (
    set SYSTEM=a2600
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.lnx] (
    set SYSTEM=lynx
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.jag] (
    set SYSTEM=jaguar
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.col] (
    set SYSTEM=coleco
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.int] (
    set SYSTEM=intv
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.vec] (
    set SYSTEM=vectrex
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.chf] (
    set SYSTEM=channelf
    set DEVICE=cart
    )
if [%INPUTEXT%]==[.d64] (
    set SYSTEM=c64
    set DEVICE=flop1
    )
if [%INPUTEXT%]==[.crt] (
    set SYSTEM=c64
    set DEVICE=cart1
    )
if [%INPUTEXT%]==[.prg] (
    set SYSTEM=c64
    set DEVICE=quik
    )
if [%INPUTEXT%]==[.t64] (
    set SYSTEM=c64
    set DEVICE=quik
    )
if [%INPUTEXT%]==[.adf] (
    set SYSTEM=a500n
    set DEVICE=flop1
    )
if [%INPUTEXT%]==[.z80] (
    set SYSTEM=spectrum
    set DEVICE=dump
    )
if [%INPUTEXT%]==[.sp] (
    set SYSTEM=spectrum
    set DEVICE=dump
    )
if [%INPUTEXT%]==[.mx1] (
    set SYSTEM=msx2p
    set DEVICE=cart1
    )
if [%INPUTEXT%]==[.mx2] (
    set SYSTEM=msx2p
    set DEVICE=cart1
    )
if [%INPUTEXT%]==[.dsk] (
    set SYSTEM=msx2p
    set DEVICE=flop1
    )
REM 2ADD: Amstrad CPC
if [%INPUTEXT%]==[.d88] (
    set SYSTEM=pc8801mk2sr
    set DEVICE=flop1
    )
if [%INPUTEXT%]==[.fdi] (
     set SYSTEM=pc9821
     set DEVICE=flop1
     )
REM 2ADD: PC-9801: .fdi, .fdd, .hdi
if [%INPUTEXT%]==[.dim] (
    set SYSTEM=x68000
    set DEVICE=flop1
    )
if [%INPUTEXT%]==[.xdf] (
    set SYSTEM=x68000
    set DEVICE=flop1
    )
if [%INPUTEXT:~0,3%]==[.85] (
    set SYSTEM=ti85
    set DEVICE=serl
    )
if [%INPUTEXT:~0,3%]==[.86] (
    set SYSTEM=ti86
    set DEVICE=serl
    )
	
if not defined SYSTEM goto noext

echo %0: detected system: %SYSTEM%
echo %0: detected device: %DEVICE%

REM start the emulator with detected system and device
echo %0: starting emulator: %MESSCMD% %SYSTEM% -%DEVICE% "%~f1" %2 %3 %4 %5 %6 %7 %8 %9
%MESSCMD% %SYSTEM% -%DEVICE% "%~f1" %2 %3 %4 %5 %6 %7 %8 %9
exit /B %ERRORLEVEL%

:classic_launch
%MESSCMD% %*
goto :eof

:noext
echo %0: unknown ROM extension
goto :eof

:LoCase
:: Subroutine to convert a variable VALUE to all lower case.
:: The argument for this subroutine is the variable NAME.
:: by Jiri http://www.robvanderwoude.com/battech_convertcase.php
FOR %%i IN ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") DO CALL SET "%1=%%%1:%%~i%%"
GOTO:EOF
