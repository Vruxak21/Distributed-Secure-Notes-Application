@echo off
REM Start Flask backend
cd back
start cmd /k ".venv\Scripts\activate && pip install -r .\requirements.txt && .\scripts\windows\run_master.bat"
start cmd /k ".venv\Scripts\activate && pip install -r .\requirements.txt && .\scripts\windows\run_replica.bat"
REM Wait 10 seconds, then run init_test_data.py in the same venv
timeout /t 5 >nul
start cmd /k ".venv\Scripts\activate && python init_test_data.py"
cd ..
REM Start React frontend
cd front-app
start cmd /k "npm start"
cd ..
