@echo off

ver

echo.

wmic os get * /format:textvaluelist

echo.

SYSTEMINFO

echo.

REM https://github.com/fastfetch-cli/fastfetch
fastfetch

REM ALTERNATIVES:
REM  MSINFO32 (GUI ONLY?)
REM  WINMSD
REM  WinSAT features
