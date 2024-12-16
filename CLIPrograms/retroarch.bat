@echo off
setlocal

set INPUTEXT=%~x1
REM convert extension to lowercase
call :LoCase INPUTEXT

set RETROARCH_BASE_PATH=%~d0\PortableApps\RetroArch
REM installed from the windows store
REM if exist "%~d0\PortableApps\RetroArch\retroarch.exe" set RETROARCH_BASE_PATH=%~d0\PortableApps\RetroArch

set RETROARCH_CORES_PATH=%RETROARCH_BASE_PATH%\cores
set RETROARCH_CONFIGS_PATH=%RETROARCH_BASE_PATH%\configs

if ["%INPUTEXT%"]==[".nes"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\nestopia_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\nestopia.cfg
if [%2]==[mesen] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mesen_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mesen.cfg
REM TODO: if [%2]==[fceu] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\...
if ["%INPUTEXT%"]==[".fds"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\nestopia_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\nestopia.cfg
if ["%INPUTEXT%"]==[".smc"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\snes9x_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\snes9x.cfg
REM if ["%INPUTEXT%"]==[".smc"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\bsnes_hd_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\bsnes.cfg
if [%2]==[snes9x] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\snes9x_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\snes9x.cfg
if ["%INPUTEXT%"]==[".sfc"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\snes9x_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\snes9x.cfg
if ["%INPUTEXT%"]==[".vb"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_vb_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-vb.cfg

REM if ["%INPUTEXT%"]==[".gb"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\gambatte_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\gambatte.cfg
if ["%INPUTEXT%"]==[".gb"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mgba_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\gambatte.cfg
REM TODO: SGB ROMs autodetection
REM if not x%filename:[S]=%==x%filename%  
REM TODO:FIX  if [%2]==[sgb]  set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\bsnes_performance_libretro.dll" -c %RETROARCH_CONFIGS_PATH%\bsnes.cfg "%RETROARCH_BASE_PATH%\..\system\bsnes\Super Gameboy (J) (V1.2) [R-Euro+USA][!].sfc"  --subsystem sgb  
if [%2]==[sgb]  set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mgba_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mgba.cfg

REM if ["%INPUTEXT%"]==[".gbc"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\gambatte_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\gambatte.cfg
if ["%INPUTEXT%"]==[".gbc"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mgba_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\gambatte.cfg

if ["%INPUTEXT%"]==[".n64"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mupen64plus_next_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mupen64.cfg
if ["%INPUTEXT%"]==[".z64"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mupen64plus_next_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mupen64.cfg
REM NO WIDESCREEN HACK  if ["%INPUTEXT%"]==[".z64"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\parallel_n64_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\parallel_n64.cfg
REM https://github.com/libretro/parallel-n64/issues/387

if ["%INPUTEXT%"]==[".gba"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mgba_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mgba.cfg
REM OLD: if ["%INPUTEXT%"]==[".gba"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\vbam_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\vba.cfg
if ["%INPUTEXT%"]==[".nds"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\melonds_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\melonds.cfg
REM if ["%INPUTEXT%"]==[".nds"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\desmume_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\desmume.cfg
if ["%INPUTEXT%"]==[".3ds"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\citra_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\citra.cfg
REM if ["%INPUTEXT%"]==[".pce"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_pce_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-pce.cfg
if ["%INPUTEXT%"]==[".pce"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_pce_fast_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-pce.cfg
if ["%INPUTEXT%"]==[".sgx"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_sgx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-pce.cfg
if ["%INPUTEXT%"]==[".sms"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\genesis_plus_gx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\genplus.cfg
if ["%INPUTEXT%"]==[".gg"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\genesis_plus_gx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\genplus-gg.cfg
if ["%INPUTEXT%"]==[".gen"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\genesis_plus_gx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\genplus.cfg
if ["%INPUTEXT%"]==[".smd"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\genesis_plus_gx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\genplus.cfg
REM if ["%INPUTEXT%"]==[".32x"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\picodrive_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\picodrive.cfg
if [%2]==[blastem] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\blastem_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\blastem.cfg

if ["%INPUTEXT%"]==[".ws"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_wswan_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-wswan.cfg
if ["%INPUTEXT%"]==[".wsc"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_wswan_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-wswan.cfg
if ["%INPUTEXT%"]==[".ngp"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_ngp_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-ngp.cfg
if ["%INPUTEXT%"]==[".ngc"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_ngp_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-ngp.cfg
if ["%INPUTEXT%"]==[".lyx"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_lynx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-lynx.cfg
if ["%INPUTEXT%"]==[".lnx"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_lynx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-lynx.cfg

if ["%INPUTEXT%"]==[".zip"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\fbneo_libretro.dll"   -c %RETROARCH_CONFIGS_PATH%\fbneo.cfg
if [%2]==[fba] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\fbneo_libretro.dll"   -c %RETROARCH_CONFIGS_PATH%\fbneo.cfg

if [%2]==[mame] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mame_libretro.dll"   -c %RETROARCH_CONFIGS_PATH%\mame.cfg
REM TODO: if [%2]==[fmt] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mame_libretro.dll"   -c "%RETROARCH_CONFIGS_PATH%\mame.cfg

if ["%INPUTEXT%"]==[".dim"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\px68k_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\px68k.cfg
if ["%INPUTEXT%"]==[".hdf"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\px68k_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\px68k.cfg
if ["%INPUTEXT%"]==[".xdf"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\px68k_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\px68k.cfg
if [%2]==[x68k]  set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\px68k_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\px68k.cfg

if ["%INPUTEXT%"]==[".d88"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\quasi88_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\quasi88.cfg
if [%2]==[pc88] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\quasi88_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\quasi88.cfg

if ["%INPUTEXT%"]==[".fdi"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\np2kai_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\np2kai.cfg
if ["%INPUTEXT%"]==[".hdi"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\np2kai_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\np2kai.cfg
if [%2]==[pc98] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\np2kai_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\np2kai.cfg

if ["%INPUTEXT%"]==[".dsk"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\bluemsx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\bluemsx.cfg
if ["%INPUTEXT%"]==[".mx1"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\bluemsx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\bluemsx.cfg
if ["%INPUTEXT%"]==[".mx2"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\bluemsx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\bluemsx.cfg
if [%2]==[msx] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\bluemsx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\bluemsx.cfg

if ["%INPUTEXT%"]==[".d64"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\vice_x64sc_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\vice.cfg
if ["%INPUTEXT%"]==[".t64"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\vice_x64sc_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\vice.cfg
if [%2]==[c64] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\vice_x64sc_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\vice.cfg

if ["%INPUTEXT%"]==[".adf"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\puae_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\uae.cfg
if ["%INPUTEXT%"]==[".hdf"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\puae_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\uae.cfg
if [%2]==[amiga] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\puae_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\uae.cfg

REM TODO: show a core select menu, remove "if [%2]==[..."
if ["%INPUTEXT%"]==[".cue"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_psx_hw_libretro.dll"   -c "%RETROARCH_CONFIGS_PATH%\mednafen-psx.cfg"
if ["%INPUTEXT%"]==[".chd"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_psx_hw_libretro.dll"   -c "%RETROARCH_CONFIGS_PATH%\mednafen-psx.cfg"
REM TODO: switch psx->swanstation
REM if ["%INPUTEXT%"]==[".cue"] if [%COMPUTERNAME%]==[OLDBOSS2] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_psx_libretro.dll"   -c "%RETROARCH_CONFIGS_PATH%\mednafen-psx.cfg"
if [%2]==[ss] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_saturn_libretro.dll"  -c "%RETROARCH_CONFIGS_PATH%\mednafen-saturn.cfg"
if [%2]==[sat] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_saturn_libretro.dll"  -c "%RETROARCH_CONFIGS_PATH%\mednafen-saturn.cfg"
if [%2]==[yaba] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\yabause_libretro.dll"  -c "%RETROARCH_CONFIGS_PATH%\yabause.cfg"
if [%2]==[kronos] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\kronos_libretro.dll"  -c "%RETROARCH_CONFIGS_PATH%\kronos.cfg"
if [%2]==[scd]  set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\genesis_plus_gx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\genplus.cfg
if [%2]==[pcecd] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_pce_fast_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-pce.cfg
REM if [%2]==[pcecdfast] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\_OLD\mednafen_pce_fast_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-pce.cfg
if [%2]==[pcfx] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\mednafen_pcfx_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\mednafen-pcfx.cfg
if [%2]==[3do] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\opera_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\opera.cfg
if [%2]==[3d0] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\opera_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\opera.cfg
if [%2]==[ngcd] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\neocd_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\neocd.cfg
if [%2]==[neocd] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\neocd_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\neocd.cfg
if [%2]==[dc] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\flycast_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\flycast.cfg
if ["%INPUTEXT%"]==[".gdi"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\flycast_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\flycast.cfg
if ["%INPUTEXT%"]==[".cdi"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\flycast_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\flycast.cfg
if ["%INPUTEXT%"]==[".lst"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\flycast_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\flycast.cfg
if [%2]==[ps2] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\play_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\play.cfg
if [%2]==[play] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\play_libretro.dll"  -c %RETROARCH_CONFIGS_PATH%\play.cfg

if ["%INPUTEXT%"]==[".exe"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\dosbox_pure_libretro.dll"   -c "%RETROARCH_CONFIGS_PATH%\dosbox.cfg
if ["%INPUTEXT%"]==[".bat"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\dosbox_pure_libretro.dll"   -c "%RETROARCH_CONFIGS_PATH%\dosbox.cfg
if ["%INPUTEXT%"]==[".com"] set _APPENDED_OPTIONS=-L "%RETROARCH_CORES_PATH%\dosbox_pure_libretro.dll"   -c "%RETROARCH_CONFIGS_PATH%\dosbox.cfg

REM if [%COMPUTERNAME%]==[BOSS2]   set _APPENDED_OPTIONS=%_APPENDED_OPTIONS%  --appendconfig  "%RETROARCH_CONFIGS_PATH%\shaders_enabled.cfg"

REM quick fix for full path needed
if exist %1 set _ARGS=%_APPENDED_OPTIONS% "%~f1"
if not exist %1 set _ARGS=-c "%RETROARCH_CONFIGS_PATH%\retroarch.cfg %*

REM launch retroarch
REM temp workaround for backup memory save in system dir
REM move R:\*.bcr  "%RETROARCH_BASE_PATH%\..\system\"
REM move R:\*.bkr  "%RETROARCH_BASE_PATH%\..\system\"
REM move R:\*.smpc  "%RETROARCH_BASE_PATH%\..\system\"

REM echo "%RETROARCH_BASE_PATH%" retroarch.exe %_ARGS%
start "" /D "%RETROARCH_BASE_PATH%" retroarch.exe --verbose  %_ARGS% 

REM DEBUG: start "" /WAIT /D "%RETROARCH_BASE_PATH%" retroarch.exe  --verbose --log-file R:\retroarch_log.txt  %_ARGS% 

REM move "%RETROARCH_BASE_PATH%\..\system\*.bcr"  R:\
REM move "%RETROARCH_BASE_PATH%\..\system\*.bkr" R:\
REM move "%RETROARCH_BASE_PATH%\..\system\*.smpc" R:\
goto :eof


REM else 
REM echo RetroArch not found
REM exit /b 9009


:LoCase
:: Subroutine to convert a variable VALUE to all lower case.
:: The argument for this subroutine is the variable NAME.
:: by Jiri http://www.robvanderwoude.com/battech_convertcase.php
FOR %%i IN ("A=a" "B=b" "C=c" "D=d" "E=e" "F=f" "G=g" "H=h" "I=i" "J=j" "K=k" "L=l" "M=m" "N=n" "O=o" "P=p" "Q=q" "R=r" "S=s" "T=t" "U=u" "V=v" "W=w" "X=x" "Y=y" "Z=z") DO CALL SET "%1=%%%1:%%~i%%"
GOTO:EOF
