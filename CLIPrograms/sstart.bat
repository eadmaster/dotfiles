@echo off
setlocal

set _DEFAULT_OPTIONS=/silent

if exist "%PROGRAMFILES%\Sandboxie\Start.exe" (
	"%PROGRAMFILES%\Sandboxie\Start.exe" %_DEFAULT_OPTIONS% %*
	goto :eof
)

if exist "%ProgramW6432%\Sandboxie\Start.exe" (
	"%ProgramW6432%\Sandboxie\Start.exe" %_DEFAULT_OPTIONS% %*
	goto :eof
)

REM TODO: Sandboxie stdout to console http://www.sandboxie.com/index.php?StartCommandLine
	
REM else
echo %0: Sandboxie not found
exit /b 9009
