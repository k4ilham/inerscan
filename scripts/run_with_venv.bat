@echo off
cd /d "%~dp0.."
REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the application
echo Starting Scanner App...
python main.py

pause
