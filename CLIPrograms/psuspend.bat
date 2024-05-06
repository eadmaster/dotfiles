@if not defined SYSINTERNALS_PATH call initenv.bat
@"%SYSINTERNALS_PATH%\pssuspend.exe" -accepteula %*.exe
