@echo off

del /F /Q "%~d0\Games\MAME\roms\%1.zip"
del /F /Q "%~d0\Games\MAME\artwork\%1.zip"
del /F /Q "%~d0\Games\MAME\samples\%1.zip
del /F /Q "%~d0\Games\MAME\snap\%1.png

if not defined PENDRIVE call initenv

del /F /Q "%PENDRIVE%\temp\playing\mame\%1.zip
del /F /Q "%PENDRIVE%\temp\playing\mame\artwork\%1.zip
del /F /Q "%PENDRIVE%\temp\playing\mame\samples\%1.zip
