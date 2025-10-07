@echo off
REM Sales Data Processing Script - Quick Installation Script for Windows
REM This script provides a quick way to install dependencies on Windows

echo 🚀 Sales Data Processing Script - Quick Install
echo ==============================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo ✓ Python is available
python --version

REM Check if pip is installed
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available. Please install pip.
    pause
    exit /b 1
)

echo ✓ pip is available

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies from requirements.txt...
python -m pip install -r requirements.txt

echo.
echo ✅ Installation completed successfully!
echo.
echo 📋 Next steps:
echo    1. Make sure you have 'sales_data.csv' in the current directory
echo    2. Run: python process_sales_data.py
echo.
echo 💡 For more options, run: python setup.py --help

pause