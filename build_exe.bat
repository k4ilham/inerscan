@echo off
echo Building InerScan Pro...
echo Ensure PyInstaller is installed: pip install pyinstaller

rmdir /s /q build
rmdir /s /q dist

pyinstaller --noconfirm --noconsole --onefile ^
    --name "InerScanPro" ^
    --hidden-import "PIL._tkinter_finder" ^
    --collect-all "customtkinter" ^
    --add-data "README.md;." ^
    "scanner_app.py"

echo.
echo Build Complete!
echo You can find the executable in the 'dist' folder.
pause
