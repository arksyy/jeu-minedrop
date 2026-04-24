./start.bat@echo off
start "Frontend" cmd /k "cd frontend && npm run dev"
start "Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload"
