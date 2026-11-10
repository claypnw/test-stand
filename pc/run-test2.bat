@echo off
title House Cameras - Second Test
cd /d "%~dp0"

echo ============================================================
echo  HOUSE CAMERAS - SECOND TEST
echo.
echo  The first test found your unit alive, but its camera
echo  door refused - the unit's own stream switch stands off,
echo  and the first test never tried this family's true
echo  stream form, nor the family's own talking road.
echo.
echo  This test asks the unit, all in one run, camera 1 only:
echo.
echo    Forms 1 and 2 - the family's own stream form. These
echo    need the unit's "Enable RTSP Server" switch ticked
echo    on the unit first.
echo    Forms 3, 4 and 5 - the family's own talking road, on
echo    three doors. These need no switch.
echo.
echo  The translator program (go2rtc) is about to start in
echo  THIS window. In a few seconds a page will open in your
echo  web browser. That page lists the second test streams.
echo.
echo  On that page, click the word STREAM beside each
echo  test2-form name - the word "stream" stands at the right
echo  side of the page, on the same line as the name, and
echo  that click is the one that wakes the test. Clicking
echo  the name itself only ticks a box and starts nothing.
echo  Leave the tick boxes alone.
echo.
echo  Then send a picture of the page and a picture of this
echo  black window. The words in the two pictures say what
echo  the test found.
echo.
echo  LEAVE THIS WINDOW OPEN the whole time. Closing it
echo  stops the test.
echo ============================================================
echo.

if not exist "%~dp0go2rtc.exe" (
    echo STOP: the translator program, go2rtc.exe, is NOT in
    echo this folder.
    echo.
    echo The program has to sit in this same folder, next to
    echo this file. Put go2rtc.exe here, then double-click
    echo this file again.
    echo.
    pause
    exit /b 1
)

if not exist "%~dp0test2-config.yaml" (
    echo STOP: the second test settings file,
    echo test2-config.yaml, is NOT in this folder.
    echo.
    echo That file has to sit in this same folder, next to
    echo this file. Put test2-config.yaml here, then
    echo double-click this file again.
    echo.
    pause
    exit /b 1
)

echo Starting the translator now...
echo (The browser page opens in about five seconds.)
echo.

start "" /min cmd /c "ping -n 6 127.0.0.1 >nul & start http://localhost:1984"

"%~dp0go2rtc.exe" -config "%~dp0test2-config.yaml"

echo.
echo ============================================================
echo  The test has stopped.
echo.
echo  If you have not sent them yet: send a picture of the
echo  browser page, and a picture of this black window.
echo ============================================================
pause
