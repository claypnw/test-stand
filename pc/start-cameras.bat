@echo off
rem ============================================================
rem  START THE HOUSE CAMERAS
rem
rem  Double-click this file. It does two things:
rem    1. Starts the translator program (go2rtc) with the
rem       settings file that sits in this same folder.
rem       A black window opens for it. LEAVE THAT WINDOW OPEN
rem       the whole time you are watching the cameras.
rem    2. Opens the house camera page in Chrome.
rem
rem  To stop: close the black go2rtc window. That is all.
rem  Nothing here changes any setting on your PC.
rem ============================================================

rem Work from the folder this file lives in, wherever it is.
cd /d "%~dp0"

rem Start the translator in its own window, using the
rem settings file (go2rtc.yaml) from this folder.
start "House cameras - leave this window open" "%~dp0go2rtc.exe" -config "%~dp0go2rtc.yaml"

rem Give the translator a few seconds to get going,
rem then open the camera page in Chrome. The ?t= part of the
rem page address tells the page where the translator lives:
rem on this PC itself (localhost), port 1984. Without that
rem part the page would only show test pictures.
timeout /t 3 /nobreak >nul
start "" chrome "https://claypnw.github.io/test-stand/cameras.html?t=http://localhost:1984"
