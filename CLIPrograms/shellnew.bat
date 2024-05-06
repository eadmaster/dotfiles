@echo off
setlocal

REM syntax: shellnew [ftype|.ext] [filename|NullFile]
REM ...
REM see also:
REM http://mc-computing.com/WinExplorer/WinExplorerRegistry_ShellNew.htm

if [%1]==[] goto :eof

reg delete "HKCR\%1\ShellNew" /f
reg add "HKCR\%1\ShellNew" /f

if [%2]==[NullFile] (
reg add "HKCR\%1\ShellNew" /f /v NullFile
) else (
reg add "HKCR\%1\ShellNew" /f /v FileName /d "%~2"
)