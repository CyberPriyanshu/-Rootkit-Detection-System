@echo off
title Rootkit Detection System - GUI Launcher
color 0A

echo.
echo ================================================
echo    ROOTKIT DETECTION SYSTEM - GUI LAUNCHER
echo ================================================
echo.
echo Starting GUI application...
echo If the Terms dialog appears, click I ACCEPT
echo Then the main GUI will open
echo.
echo IMPORTANT: Look for windows that may have opened!
echo Check your taskbar and use Alt+Tab if needed
echo.

cd /d "%~dp0"
".venv\Scripts\python.exe" GUI_Rootkit_Detector.py

if errorlevel 1 (
    echo.
    echo ================================================
    echo ERROR: Failed to start GUI application!
    echo ================================================
    echo.
    pause
) else (
    echo.
    echo ================================================
    echo GUI closed normally.
    echo ================================================
    echo.
    echo Press any key to close this window...
    pause >nul
)
