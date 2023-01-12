::settings
set DontClose=true

::setup
echo off
title Taskbar Aligner v1.0   (sc-tool suit)

:Choice
cls
echo.
echo [C=Center, L=Left]
set /p alignment=Align Win11 taskbar to: 
echo.
if /I "%alignment%" EQU "c" set changetoval=1 && goto :next
if /I "%alignment%" EQU "l" set changetoval=0 && goto :next
if /I "%alignment%" EQU "e" goto :eof
goto :Choice
:next

::reg-change
reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v TaskbarAl /t REG_DWORD /d %changetoval% /f

::end
if "%ERRORLEVEL%" NEQ "0" echo Failed to change alignment! && reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v TaskbarAl /t REG_DWORD /d 1 /f && pause
pause
if /I "%DontClose%" EQU "true" goto :Choice
exit
