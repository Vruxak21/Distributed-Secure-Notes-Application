@echo off
REM Start Flask backend
cd back
start cmd /k ".venv\Scripts\activate && pip install -r .\requirements.txt && python -m flask --app app run"
REM Wait 10 seconds, then run init_test_data.py in the same venv
timeout /t 2 >nul
start cmd /k ".venv\Scripts\activate && python init_test_data.py"
start "" http://localhost:5000
cd ..
REM Start React frontend
cd front-app
start cmd /k "npm start"
cd ..
