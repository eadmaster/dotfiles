@echo off
setlocal

if not defined SYSINTERNALS_PATH call initenv.bat
if exist "%SYSINTERNALS_PATH%\sdelete.exe" (
	"%SYSINTERNALS_PATH%\sdelete.exe"  -r %*
	goto :eof
)

if exist "%PROGRAMFILES%\Eraser\Eraserl.exe" (
	"%PROGRAMFILES%\Eraser\Eraserl.exe" -folder %* -subfolders -method DoD_E -results
	goto :eof
)

if exist "%~d0\PortableApps\Eraser\App\eraserl.exe" (
	"%~d0\PortableApps\Eraser\App\eraserl.exe" -folder %* -subfolders -method DoD_E -results
	goto :eof
)

REM not recursive, also hide the filename, untested
call unix shred --iterations=2 --zero --remove --verbose --force %*
if not [%ERRORLEVEL%]==[9009] goto :eof

call unix srm -l -v -z %*
if not [%ERRORLEVEL%]==[9009] goto :eof

call unix wipe -r -q -R /dev/zero -S r %*
if not [%ERRORLEVEL%]==[9009] goto :eof

REM call nircmdc filldelete %*
REM if [%ERRORLEVEL%]==[0] goto :eof

REM else alternative using dd
REM ERRORLEVEL: 0=success, 1=FileSystem error (e.g. file does not exist or read only), 2=I/O error
if [%1]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if [%_HELP%]==[ON] (
	echo usage: %0 FILE_TO_WIPE
	echo.
	goto :eof
)

if not exist %1 (
	echo %0 error: "%1" does not exist  1>&2
	exit /b 1
)

REM TODO: if exist %1\NUL -> recurse into subdirs

REM TODO: read effective cluster size, assuming 64k
REM set CLUSTER_SIZE=4096
set CLUSTER_SIZE=65536
set OVERWRITE_PASSES=2

REM compute used clusters
set /A USEDCLUSTERS=%~z1/%CLUSTER_SIZE%
set /A USEDCLUSTERS+=1
REM echo %USEDCLUSTERS%

REM loop and overwrite the file with random data
for /L %%A in (1, 1, %OVERWRITE_PASSES%) do (
	call dd if=/dev/zero of=%1 bs=%CLUSTER_SIZE% count=%USEDCLUSTERS% >NUL 2>NUL
	if %ERRORLEVEL%==0 (
		echo %0: pass %%A... ok   1>&2
	) else (
		echo %0: pass %%A... ERROR   1>&2
		exit /b 2
	)
)
REM endfor

REM random rename
set RANDOMFILENAME=%RANDOM%
echo %0: renaming as "%RANDOMFILENAME%"...  1>&2
ren %1 %RANDOMFILENAME%

REM remove the file from the FS
del /Q "%~d1%~p1%RANDOMFILENAME%"
REM del exit codes seems not to be realiable..
if not exist "%~d1%~p1%RANDOMFILENAME%" (
	echo %0: file removed correctly from the file system  1>&2
	exit /b 0
) else (
	echo %0: unable to remove file from the file system ^(check attributes^)  1>&2
	exit /b 1
)
