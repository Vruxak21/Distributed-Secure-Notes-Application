@echo off
REM Start Flask backend
cd back

REM Create venv if it doesn't exist and install dependencies once
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate
pip install -r .\requirements.txt

REM Start master and replica servers
start cmd /k ".venv\Scripts\activate && .\scripts\windows\run_master.bat"
start cmd /k ".venv\Scripts\activate && .\scripts\windows\run_replica.bat"

REM Wait 10 seconds, then run init_test_data.py
timeout /t 5 >nul
start cmd /k ".venv\Scripts\activate && python init_test_data.py"

cd ..

REM Start React frontend
cd front-app
start cmd /k "npm install && npm start"
cd ..