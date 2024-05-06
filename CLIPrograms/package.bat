@echo off
setlocal

if [%1]==[] goto usage
if [%1]==[-h] goto usage
if [%1]==[--help] goto usage
if [%1]==[/?] goto usage

REM TODO: set CHOCO=%PROGRAMDATA%\chocolatey\bin\choco.exe
REM TODO: set SCOOP=powershell  -noprofile -ex unrestricted "& 'C:\Users\a.mantoni\scoop\apps\scoop\current\bin\scoop.ps1'  list;exit $lastexitcode"

set CMD=%1

if [%NAME%]==[.] set CMD=list
if [%CMD%]==[list] (
	echo %0: list installed packages...
	
	winget list
	
	choco list --local-only
	
	scoop list
	
	REM using oneget https://github.com/OneGet/oneget/wiki/cmdlets
	REM tip: make sure chocolatey package provider is installed
	REM powershell -Command "get-packageprovider -name chocolatey"

	call powershell -Command "Get-Package"
	
	%~d0\PortableApps\NirLauncher\SysinternalsSuite\PsInfo.exe -s

	call wmic product get * /format:textvaluelist

	REM TODO: ALTERNATIVE USING https://www.nirsoft.net/utils/installed_packages_view.html
	
	goto :eof
)

if [%CMD%]==[clear] set CMD=clean
if [%CMD%]==[clean] (
	echo %0: clearing packages cache...
	scoop cache rm *
	if exist "%LocalAppData%\Nuget\Cache"  del /F /Q  "%LocalAppData%\Nuget\Cache\*.nupkg"
	goto :eof
)


REM 2nd arg required check:
if [%2]==[] goto usage
REM else
set NAME=%2


if [%CMD%]==[install] (
	echo %0: installing %NAME%...
	
	REM TODO: if exist %1 -> install directly?
	
	winget install %NAME%
	if [%ERRORLEVEL%]==[0] goto :eof
	
	choco install %NAME%
	if [%ERRORLEVEL%]==[0] goto :eof
	
	call powershell -ExecutionPolicy RemoteSigned -Command "Install-Package %NAME%"
	REM -ExecutionPolicy Bypass  
	if not [%ERRORLEVEL%]==[1] goto :eof
	
	scoop install %NAME% --global
	if [%ERRORLEVEL%]==[0] goto :eof
	
	echo %0: unable to find any package installer
	exit /b 9009
)

if [%CMD%]==[remove] set CMD=uninstall
if [%CMD%]==[uninstall] (
	echo %0: uninstalling %NAME%...

	winget uninstall %NAME%
	if [%ERRORLEVEL%]==[0] goto :eof
	
	choco uninstall %NAME%
	if [%ERRORLEVEL%]==[0] goto :eof
	
	call powershell -Command "Uninstall-Package %NAME%"
	if not [%ERRORLEVEL%]==[1] goto :eof

	scoop uninstall %NAME% --global
	if [%ERRORLEVEL%]==[0] goto :eof
	
	REM alternative using  http://www.nirsoft.net/utils/myuninst.html
	%~d0\PortableApps\NirLauncher\NirSoft\MyUninstaller.exe /uninstall %*
	if not [%ERRORLEVEL%]==[9009] goto :eof
	
	REM alternative using  https://www.nirsoft.net/utils/uninstall_view.html
	%~d0\PortableApps\NirLauncher\NirSoft\UninstallView.exe /uninstall %*
	if not [%ERRORLEVEL%]==[9009] goto :eof

	echo %0: unable to find any package uninstaller
	exit /b 9009
)

if [%CMD%]==[upgrade] set CMD=update
if [%CMD%]==[update] (
	echo %0: updating %NAME%...

	winget upgrade %NAME%
	if [%ERRORLEVEL%]==[0] goto :eof
	
	choco upgrade %NAME%
	if [%ERRORLEVEL%]==[0] goto :eof
	
	scoop update %NAME% --global
	if [%ERRORLEVEL%]==[0] goto :eof
	
	REM 2FIX: unsupported by oneget https://github.com/OneGet/oneget/issues/6
	REM workaround:
	call %0 remove %NAME%
	call %0 install %NAME%
	goto :eof
)


if [%CMD%]==[find] set CMD=search
if [%CMD%]==[search] (
	echo %0: searching for packages with name "%NAME%"...
	
	winget search %NAME%
	
	choco search %NAME%
	
	scoop search %NAME%
	
	conda search %NAME%
	
	call powershell -Command "Find-Package %NAME%"

	goto :eof
)

if [%CMD%]==[info] set CMD=show
if [%CMD%]==[show] (
	echo %0: package details...

	winget show %NAME%

	choco info %NAME%
	
	REM scoop ... %NAME%
	
	call powershell -Command "Find-Package %NAME% | Format-List -Property *"
	REM TODO: list installed files
	
	call wmic product where "Name like %%NAME%%" get * /format:textvaluelist
	
	goto :eof
)


REM else fallback
:usage
echo usage: %0 install^|remove^|update^|search^|list^|clean^|info [PACKAGENAME]
echo.
exit /B 0

