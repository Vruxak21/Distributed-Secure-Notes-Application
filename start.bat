@echo off
REM Start Flask backend
cd back
start cmd /k ".venv\Scripts\activate && python -m flask --app app run"
start "" http://localhost:5000
cd ..
REM Start React frontend
cd front-app
start cmd /k "npm start"
cd ..
