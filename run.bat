@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python main.py
if errorlevel 1 (
    echo.
    echo ОШИБКА! Проверь, установлен ли pydub-ng в venv.
    echo Выполни в терминале: venv\Scripts\Activate.ps1 затем pip install pydub-ng
    pause
)