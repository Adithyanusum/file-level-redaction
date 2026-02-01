🛡️ File-Level Redaction Web Application

A secure, web-based file redaction system built using FastAPI that enables users to detect and redact sensitive information from PDF, Image, DOCX, and XLSX files. The application supports manual, phrase-based, and automatic redaction, with preview and detection capabilities.

📌 Project Overview

Handling sensitive documents often requires masking or removing Personally Identifiable Information (PII) such as emails, phone numbers, IDs, and confidential text.
This project provides a file-level redaction platform that allows users to:

Upload documents

Detect sensitive data

Preview files

Apply redaction safely

Download redacted outputs

The system is designed for accuracy, robustness, and extensibility, making it suitable for real-world document processing workflows.

✨ Key Features
🔍 Detection

OCR-based detection for images

Text extraction from PDF, DOCX, and XLSX

Phrase-based sensitive data identification

Automatic PII detection fallback

✂️ Redaction

Region-based redaction (manual selection)

Phrase-based redaction

Automatic redaction

Supports blackout and blur modes

Multi-page PDF redaction

👀 Preview

PDF first-page preview

DOCX preview (image / HTML)

XLSX preview (image / HTML)

📁 Supported File Types

PDF

Images (PNG, JPG, JPEG, TIFF, BMP)

DOCX

XLSX

🧱 Technology Stack
Layer	Technology
Backend	FastAPI
ASGI Server	Uvicorn
OCR	Tesseract (via pytesseract)
PDF Processing	PyMuPDF
Image Processing	OpenCV, Pillow
Office Docs	python-docx, openpyxl
Frontend	HTML, CSS, JavaScript
Deployment	Render
Containerization	Docker (optional)
📂 Project Structure
file-level-redaction/
│
├── app/
│   ├── main.py              # FastAPI routes
│   ├── redact.py            # Detection & redaction logic
│   └── __init__.py
│
├── static/
│   ├── index.html
│   ├── docs.html
│   ├── styles.css
│   └── js/
│       ├── auth.js
│       └── selector.js
│
├── scripts/
│   ├── cleanup_and_remove.ps1
│   └── push_to_github.ps1
│
├── tests/                   # Test cases (optional/extendable)
├── tools/                   # Dev helpers (not required for deploy)
│
├── architecture.md
├── SoftwareRequirements.md
├── test.md
├── text.md
├── requirements.txt
├── render.yaml
├── Dockerfile
├── README.md
└── LICENSE

🚀 Deployment
🌐 Hosted on Render

The application is deployed using Render with Uvicorn.

Start Command

uvicorn app.main:app --host 0.0.0.0 --port 10000


Health Check

GET /health


Expected response:

{ "status": "ok" }

🧪 Testing Strategy

The project is tested using Positive, Negative, and Edge cases to ensure correctness and robustness.

✔️ Positive Tests

Valid file uploads

Successful redaction of emails and phone numbers

Preview generation

Auto-redaction across formats

❌ Negative Tests

Unsupported file types

Corrupt files

Invalid JSON inputs

Missing OCR dependencies

⚠️ Edge Tests

Large multi-page PDFs

High-resolution images

Overlapping redaction regions

Repeated sensitive data patterns

Detailed test cases are documented in test.md.

🔒 Security & Privacy Considerations

No user authentication (MVP scope)

Files processed in memory

No external storage by default

Redaction logs can be sanitized

Designed to avoid accidental PII leaks

⚠️ Limitations

PDF redaction is visual (text layer may still exist)

Encrypted PDFs are not supported

OCR accuracy depends on image quality

Large files may impact performance on free tiers

🔮 Future Enhancements

Permanent PDF redaction (apply_redactions)

Multilingual OCR support

Batch file uploads

Authentication & access control

Role-based redaction policies

Audit logs and redaction confidence scoring

Cloud storage integration

“This project implements a secure file-level redaction web application using FastAPI that supports detection, preview, and redaction of sensitive data across PDFs, images, DOCX, and XLSX files, validated using positive, negative, and edge-case testing.”

📜 License

This project is licensed under the MIT License.
See the LICENSE file for details.
