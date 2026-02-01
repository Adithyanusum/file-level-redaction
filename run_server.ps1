# Run this in PowerShell to start the server (keeps window open)
if (Test-Path .venv\Scripts\Activate.ps1) { . .\.venv\Scripts\Activate.ps1 }
Write-Host "Starting server on http://127.0.0.1:8003/ (changed from 8000 to avoid conflicts)"
C:\Users\nusum\Downloads\coriolisproj\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8003
Write-Host "Server stopped"
Pause
