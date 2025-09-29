@echo off
echo 🚀 Starting Frontline Worker AI System - Local Development
echo =========================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements-local.txt

REM Create data directory if it doesn't exist
if not exist "data" mkdir data

REM Install frontend dependencies
echo 📥 Installing frontend dependencies...
cd frontend
call npm install
cd ..

REM Start backend
echo 🚀 Starting backend server...
start "Backend Server" python app.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo 🚀 Starting frontend server...
cd frontend
start "Frontend Server" npm run dev
cd ..

echo.
echo ✅ System started successfully!
echo 📍 Backend:  http://localhost:5000
echo 📍 Frontend: http://localhost:3000
echo 🔗 Health:   http://localhost:5000/health
echo 🧪 Test:     http://localhost:5000/api/test-agents
echo.
echo Press any key to stop all services...
pause >nul

REM Kill processes (basic cleanup)
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo ✅ Services stopped