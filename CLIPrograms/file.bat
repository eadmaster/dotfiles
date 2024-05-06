@echo off
setlocal

call unix file %*
if not [%ERRORLEVEL%]==[9009] goto :eof

if exist "%~dp0file-5.16\file.exe" (
	set MAGIC=%~dp0file-5.16\magic\magic
	"%~dp0file-5.16\file.exe" %*
	goto :eof
)

if exist %~d0\PortableApps\UniversalExtractor\bin\file\bin\file.exe (
	set MAGIC=%~d0\PortableApps\UniversalExtractor\bin\file\share\misc\magic
	"%~d0\PortableApps\UniversalExtractor\bin\file\bin\file.exe" %*
	goto :eof
)

if exist "%~dp0libextractor-1.0.0\bin\file.exe" (
	REM set MAGIC=%~dp0file-5.16\magic\magic
	"%~dp0libextractor-1.0.0\bin\file.exe" %*
	goto :eof
)

REM else
echo unable to find file
exit /b 9009
