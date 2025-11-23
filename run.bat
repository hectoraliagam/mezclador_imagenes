@echo off
title Mezclador Imagenes TFS
cd /d "%~dp0"

echo =============================================
echo            Mezclador Imagenes - TFS
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
