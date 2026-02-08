@echo off
:: Build script for Windows (x64)
echo ========================================
echo InerScan Pro - Windows Build Script
echo ========================================
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install/upgrade dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

:: Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

:: Build executable
echo.
echo Building executable...
pyinstaller --clean InerScanPro.spec

:: Check if build succeeded
if exist "dist\InerScanPro.exe" (
    echo.
    echo ========================================
    echo ✅ Build succeeded!
    echo ========================================
    echo.
    echo Executable location: dist\InerScanPro.exe
    echo Size: 
    dir dist\InerScanPro.exe | find "InerScanPro.exe"
    echo.
    echo You can now distribute dist\InerScanPro.exe
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ Build failed!
    echo ========================================
    echo Check the output above for errors.
    echo.
    exit /b 1
)

pause
