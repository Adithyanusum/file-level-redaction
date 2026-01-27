# File Redaction Hackathon

Minimal scaffold for the hackathon project.

Quick start (Windows):

1. Create and activate venv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app

```powershell
uvicorn app.main:app --reload --port 8000
```

3. Open browser: http://localhost:8000/ (redirects to the redaction UI at `/static/indexx.html`)

Authentication
- This simplified scaffold does not require sign-in. Open `/static/index.html` to use the redaction UI.

Notes
- `app/main.py` contains API endpoints for image/pdf/docx/xlsx redaction.
- `app/redact.py` contains simple implementations using PyMuPDF, OpenCV, python-docx and openpyxl.
- Frontend is a tiny static demo in `static/index.html`.

This is a starting point — extend UI and add authentication, audit logs, and more robust redaction strategies.
