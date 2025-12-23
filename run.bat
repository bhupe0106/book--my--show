@echo off
REM BookMyShow - Startup Script for Windows
echo.
echo ================================
echo   BookMyShow Application
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version

echo.
echo [2/3] Installing/Updating dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/3] Starting BookMyShow application...
echo.
echo ================================
echo   Streamlit is starting...
echo   Open your browser to:
echo   http://localhost:8501
echo ================================
echo.

streamlit run frontend/app.py

pause
