@echo off
cd /d "%~dp0.."
echo ========================================
echo InerScan Pro - Complete Build Pipeline
echo ========================================
echo.
echo This script will:
echo 1. Build the executable (InerScanPro.exe)
echo 2. Create the installer (InerScanPro_Setup.exe)
echo.
pause

:: Step 1: Build Executable
echo.
echo ========================================
echo STEP 1: Building Executable
echo ========================================
echo.

call scripts\build_exe.bat
if errorlevel 1 (
    echo.
    echo ❌ Executable build failed! Stopping pipeline.
    pause
    exit /b 1
)

:: Step 2: Build Installer
echo.
echo ========================================
echo STEP 2: Building Installer
echo ========================================
echo.

call scripts\build_installer.bat
if errorlevel 1 (
    echo.
    echo ❌ Installer build failed!
    pause
    exit /b 1
)

:: Success!
echo.
echo ========================================
echo ✅ COMPLETE BUILD SUCCESSFUL!
echo ========================================
echo.
echo Output files:
echo   - Executable: dist\InerScanPro.exe
echo   - Installer:  installer_output\InerScanPro_Setup_v3.1.exe
echo.
echo Ready for distribution! 🚀
echo.

pause
