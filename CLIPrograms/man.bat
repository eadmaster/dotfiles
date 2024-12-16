@echo off
setlocal

if exist %1 (
	REM try to parse a local file with groff
	unix groff -Tascii -mm %* | less
	if not [%ERRORLEVEL%]==[9009] goto :eof
	REM alternatives: rman.exe http://gnuwin32.sourceforge.net/packages/polyglotman.htm
	sed -e "s/.`echo \\\b`//g;s/.^H//g;s/.\x08//g" < %1 | less
	goto :eof
)

REM set MANPATH=%GNUWIN32_HOME%\man
REM set MANPATH=/usr/share/man:/cygdrive/c/CLIPrograms/GnuWin32/man
REM set MANPAGER=less
REM call unix man %*
REM if not [%ERRORLEVEL%]==[9009] goto :eof

REM else show help of a command
REM %* /? | less
REM %* --help | less
REM help %* | less

echo %0: downloading online man for "%1"...   1>&2

call pandoc -f html -t plain "http://linux.die.net/man/1/%1" | less
if not [%ERRORLEVEL%]==[9009] goto :eof

call wget --quiet -O- "http://manpages.ubuntu.com/manpages.gz/xenial/en/man1/%1.1.gz" | gzip -dc | pandoc -f man -t plain - | less
REM TODO: colorize output

REM ALTERNATIVES:
REM html2txt --ignore-links --decode-errors=ignore -ignore-emphasis http://man.cx/%1
REM wget --quiet -O - "http://www.openbsd.org/cgi-bin/man.cgi?query=%1&apropos=0&sektion=0&manpath=OpenBSD+Current&arch=i386&format=ascii" | less
REM wget --quiet -O - "http://manpages.debian.net/cgi-bin/man.cgi?query=%1&apropos=0&sektion=0&manpath=Debian+unstable+sid&format=txt&locale=en" | less
REM FOR /L %%C IN (1,1,9) DO wget --quiet -O - "http://manpages.ubuntu.com/manpages.gz/xenial/en/man%C/%1.%%C.gz" | gzip -dc | less
