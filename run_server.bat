@echo off
REM Activate virtualenv and start uvicorn (keep window open)
if exist ".venv\Scripts\activate.bat" (
  call .venv\Scripts\activate.bat
)
C:\Users\nusum\Downloads\coriolisproj\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
