@echo off
title Mezclador Imagenes
cd /d "%~dp0"

echo =============================================
echo              Mezclador Imagenes
echo =============================================
echo.

:: Activate virtual environment (Windows)
call .venv\Scripts\activate

:: Run the Python script
python main.py

echo.
echo =============================================
echo              Process completed.
echo =============================================
pause
