@echo off
cd /d "%~dp0.."
echo ========================================
echo InerScan Pro - Installer Build Script
echo ========================================
echo.

:: Check if Inno Setup is installed
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%INNO_PATH%" (
    echo ERROR: Inno Setup not found!
    echo.
    echo Please install Inno Setup 6 from:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo Default installation path: C:\Program Files ^(x86^)\Inno Setup 6
    echo.
    pause
    exit /b 1
)

:: Check if executable exists
if not exist "dist\InerScanPro.exe" (
    echo ERROR: InerScanPro.exe not found in dist folder!
    echo.
    echo Please build the application first:
    echo   cd scripts
    echo   build_exe.bat
    echo.
    pause
    exit /b 1
)

:: Create output directory
if not exist "installer_output" mkdir installer_output

:: Build installer
echo Building installer...
echo.
"%INNO_PATH%" "installer\InerScanPro.iss"

:: Check if build succeeded
if exist "installer_output\InerScanPro_Setup_v3.1.exe" (
    echo.
    echo ========================================
    echo Build succeeded!
    echo ========================================
    echo.
    echo Installer location: installer_output\InerScanPro_Setup_v3.1.exe
    echo.
    dir installer_output\InerScanPro_Setup_v3.1.exe | find "InerScanPro_Setup"
    echo.
    echo You can now distribute this installer!
    echo.
) else (
    echo.
    echo ========================================
    echo Installer build failed!
    echo ========================================
    echo Check the output above for errors.
    echo.
    exit /b 1
)

pause
