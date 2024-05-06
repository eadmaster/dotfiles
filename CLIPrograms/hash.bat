@echo off
setlocal

REM TODO: detect if invoked from Windows shell or console -> goto :end

if exist "%~dp0rhash.*" (
	REM "%~dp0rhash.exe" --printf "%%p\n CRC32: %%C\n MD5: %%M\n SHA1: %%H\n ED2K: %%E\n TTH: %%T\n" %*
	rhash --all --bsd %*
	goto :eof
)

if exist "%~dp0gpg.bat" (	
	echo CRC32:
	call "%~dp0gpg.bat" --print-md CRC32 %*
	echo MD5:
	call "%~dp0gpg.bat" --print-md MD5 %*
	echo SHA1:
	call "%~dp0gpg.bat" --print-md SHA1 %*
	REM call "%~dp0gpg.bat" --print-md RIPEMD160 %*
	REM call "%~dp0gpg.bat" --print-md SHA256 %*
	REM call "%~dp0gpg.bat" --print-md SHA384 %*
	REM call "%~dp0gpg.bat" --print-md SHA512 %*
	REM call "%~dp0gpg.bat" --print-md SHA224 %*
	goto :eof
)

if exist "%~dp0openssl.bat" (	
	call "%~dp0openssl.bat" md5 %*
	call "%~dp0openssl.bat" sha1 %*
	REM call "%~dp0openssl.bat" md2 %*
	REM call "%~dp0openssl.bat" md4 %*
	REM call "%~dp0openssl.bat" rmd160 %*
	REM call "%~dp0openssl.bat" sha %*
	goto :eof
)

call unix md5sum %*
if not [%ERRORLEVEL%]==[9009] goto :eof

REM ALTERNATIVES: ed2k_hash, http://directory.fsf.org/project/cksfv/, %PROGRAMFILES%\aMule\alcc.exe

REM else
echo cannot find any hash program
exit /b 9009

REM :end
REM necessary if invoked from the GUI to keep the window opened
REM pause
