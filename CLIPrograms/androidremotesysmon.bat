@echo off

call androidunlock

REM enable web server autostart via  "Options->Remote Web Server->Run"
start "" /MIN /B LibreHardwareMonitor.bat

echo %0: server started on http://localhost:8085/"

REM https://stackoverflow.com/questions/9887621/accessing-localhost-of-pc-from-usb-connected-android-mobile-device
REM https://stackoverflow.com/questions/4779963/how-can-i-access-my-localhost-from-my-android-device#46795769
call adb reverse tcp:8085 tcp:8085

REM increase brightness
call adb shell settings put system screen_brightness 150

REM TODO: set forced portrait mode  https://stackoverflow.com/questions/77417911/forced-screen-orientation-when-connecting-via-adb

REM disable lockscreen  https://android.stackexchange.com/questions/233921/adb-bypass-lock-screen
call adb shell settings put secure lockscreen.disabled 1

call sleep 2

call adb shell am start -a android.intent.action.VIEW -d 'http://localhost:8085'

echo %0: press ENTER to quit
pause

call sudo taskkill /IM "LibreHardwareMonitor.exe"

REM restore low brightness
call adb shell settings put system screen_brightness 0

REM lock again
call adb shell input keyevent 26

