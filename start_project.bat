@echo off

echo Activating virtual environment...
call venv\Scripts\activate

echo Moving to app folder...
cd app

echo Starting DisasterIQ server...
start cmd /k python run.py

timeout /t 5

start http://127.0.0.1:3001

pause