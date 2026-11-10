@echo off
title House Cameras - One-Click Test
cd /d "%~dp0"

echo ============================================================
echo  HOUSE CAMERAS - ONE-CLICK TEST
echo.
echo  This test asks your camera unit two questions:
echo.
echo    1. Is the unit's password still blank?
echo    2. Which camera address form does the unit answer to?
echo.
echo  The translator program (go2rtc) is about to start in
echo  THIS window. In a few seconds a page will open in your
echo  web browser. That page lists the test streams.
echo.
echo  On that page, each test stands on its own line, with
echo  its name on the left and the word STREAM at the right
echo  end of the line. Click the word STREAM on the first
echo  line - that is the click that wakes its test. Count
echo  to ten, click Back, and do the same on each line.
echo  Clicking a name only ticks a box and starts nothing.
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

if not exist "%~dp0test-config.yaml" (
    echo STOP: the test settings file, test-config.yaml, is
    echo NOT in this folder.
    echo.
    echo That file has to sit in this same folder, next to
    echo this file. Put test-config.yaml here, then
    echo double-click this file again.
    echo.
    pause
    exit /b 1
)

echo Starting the translator now...
echo (The browser page opens in about five seconds.)
echo.

start "" /min cmd /c "ping -n 6 127.0.0.1 >nul & start http://localhost:1984"

"%~dp0go2rtc.exe" -config "%~dp0test-config.yaml"

echo.
echo ============================================================
echo  The test has stopped.
echo.
echo  If you have not sent them yet: send a picture of the
echo  browser page, and a picture of this black window.
echo ============================================================
pause
