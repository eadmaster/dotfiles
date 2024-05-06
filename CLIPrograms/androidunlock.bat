@echo off

REM check if already unlocked
REM https://stackoverflow.com/questions/35275828/is-there-a-way-to-check-if-android-device-screen-is-locked-via-adb
call adb shell dumpsys display | findstr mScreenState=ON >NUL
if %ERRORLEVEL%==0 (
    echo $0: unlocked already
    goto ;eof
fi

call adb shell input keyevent 26
REM adb shell input touchscreen swipe 200 500 200 0
call adb shell input keyevent 82
sleep 2
call adb shell input text %MY_ANDROID_PASSCODE%
call adb shell input keyevent 66
