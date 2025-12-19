@echo off
cd /d "%~dp0"

:: Launch the application using pythonw.exe (no console window)
call venv\Scripts\activate.bat >nul 2>&1
pythonw.exe main.py

:: If pythonw.exe fails (e.g. venv not activated or packages missing), show error
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the converter.
    echo Possible causes:
    echo   - Virtual environment not activated properly
    echo   - Missing dependencies (run in terminal: pip install pydub-ng watchdog mutagen)
    echo.
    echo Press any key to close this window...
    pause >nul
)