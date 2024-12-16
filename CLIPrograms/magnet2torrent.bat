@echo off
setlocal

if [%1]==[] set _HELP=ON
if [%1]==[-h] set _HELP=ON
if [%1]==[/?] set _HELP=ON
if [%_HELP%]==[ON] (
	REM echo usage: %0 TORRENT_HASH
	echo usage: %0 MAGNET_URL
	goto :eof
)

set HASH=%*
REM echo %1 | find /i "magnet:\?xt"
REM if NOT %errorlevel%==0 
REM set HASH=%HASH:~21,64%
REM else
REM set "HASH=%~1"
REM alterative: parse magnet links
REM FOR /F "delims=: tokens=3" %%G IN (%*) DO echo "%%G"

REM TODO: avoid redirections (--max-redirect=0)
REM TODO: bypass cloudflare protection

echo "%0: trying http://itorrents.org/torrent/%HASH%.torrent"
call curl --fail --location -o %HASH%_itorrents.torrent "http://itorrents.org/torrent/%HASH%.torrent"
REM if %ERRORLEVEL%==0 goto :eof

echo "%0: trying http://torrage.info/torrent.php?h=%HASH%"
call curl --fail --location -o %HASH%_torrage.torrent "http://torrage.info/torrent.php?h=%HASH%"
REM if %ERRORLEVEL%==0 goto :eof

echo "%0: trying http://torcache.to/download/%HASH%.torrent"
call curl --fail --location -o %HASH%_torcache.torrent "http://torcache.to/download/%HASH%.torrent"
REM if %ERRORLEVEL%==0 goto :eof

echo "%0: trying http://btcache.me/torrent/%HASH%"
call curl --fail --location -o %HASH%_btcache.torrent "http://btcache.me/torrent/%HASH%"

echo "%0: trying https://tfiles.org/torrent/dbe/%HASH%"
call curl --fail --location -o %HASH%_btcache.torrent "https://tfiles.org/torrent/dbe/%HASH%.torrent"

echo "%0: trying tntvillage backup"
call curl --fail --location -o %HASH%_tntvillage.torrent  "https://archive.org/download/tntvillage_all_torrents/tntvillage_all_torrents.zip/tntvillage_all_torrents%%2%HASH%.torrent"

REM call curl --fail --location -U firefox -t 1 "http://thetorrent.org/%HASH%.torrent"

REM call aria2 --bt-metadata-only --bt-save-metadata %*
REM if %ERRORLEVEL%==0 goto :eof

REM if %ERRORLEVEL%==0 goto :eof
REM TODO: check if html output

REM offline: 
REM call wget -U firefox -t 1 "http://torrage.info/torrent.php?h=%HASH%"
REM call wget "http://torrent.cd/%HASH%.torrent"

REM else file not found, open in the browser
REM call xdg-open %*
exit /B 1
