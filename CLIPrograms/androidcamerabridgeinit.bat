@echo off
setlocal

REM start the ip camera app + and begin streaming
call adb shell am start -n com.pas.webcam/com.pas.webcam.Rolling

REM TODO: enable tethering for faster speed?  https://android.stackexchange.com/questions/29954/is-it-possible-to-activate-the-usb-tethering-android-setting-from-the-command

REM TODO: autoconfigure  http://ip-webcam.appspot.com/static/doc.html
""%ProgramFiles(x86)%\IP Camera Adapter\Configure.exe"

REM TODO: use scrcpy  https://github.com/Genymobile/scrcpy/pull/4213
REM scrcpy --video-source=camera --no-audio --camera-facing=front