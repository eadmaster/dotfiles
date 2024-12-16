@echo off

call unix md5sum %*
if not [%ERRORLEVEL%]==[9009] goto :eof

REM ALTERNATIVE using rhash
if [%1]==[] (
	echo syntax: md5sum [-c hash_to_check.md5] [-d input_text] file_to_hash
	goto :eof
)
if [%1]==[-d] (
	REM echo MD5 hash for "%2"
	echo|set /p=%2| rhash --md5 -
	goto :eof
)

call rhash --md5 %*
if not [%ERRORLEVEL%]==[9009] goto :eof

call openssl dgst -md5 -r %*
if not [%ERRORLEVEL%]==[9009] goto :eof

sfk md5 %*
if not [%ERRORLEVEL%]==[9009] goto :eof

CertUtil -hashfile %* MD5
if not [%ERRORLEVEL%]==[9009] goto :eof

REM else
exit /B 9009
