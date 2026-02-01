🛡️ File-Level Redaction Web Application

A secure, extensible, and production-ready web application for detecting and redacting sensitive information from digital documents.
Built using FastAPI, the system supports PDFs, Images, Word (DOCX), and Excel (XLSX) files with manual, phrase-based, and automatic redaction capabilities.

1️⃣ Executive Summary

Organizations frequently handle documents containing Personally Identifiable Information (PII) such as email addresses, phone numbers, government IDs, and confidential text.
Improper handling of such data can lead to privacy breaches and compliance violations.

This project delivers a file-level redaction platform that enables users to:

Upload documents securely

Detect sensitive information automatically or manually

Preview content before redaction

Apply redaction reliably

Download sanitized documents

The system is designed with a focus on security, accuracy, modularity, and future scalability.

2️⃣ Core Capabilities
🔍 Sensitive Data Detection

OCR-based text extraction for image files

Native text extraction from PDFs, DOCX, and XLSX

Phrase-based detection using custom patterns

Automatic fallback detection for common PII types

✂️ Redaction Methods

Manual region-based redaction

Phrase-based redaction

Fully automatic redaction

Supports blackout and blur styles

Handles multi-page PDF redaction

👀 Preview & Validation

PDF first-page preview

DOCX preview (HTML/Image rendering)

XLSX preview (HTML/Image rendering)

Ensures user confirmation before final redaction

3️⃣ Supported File Formats
Category	Formats
Documents	PDF, DOCX, XLSX
Images	PNG, JPG, JPEG, TIFF, BMP
4️⃣ System Architecture Overview

The application follows a clean, layered architecture:

Frontend Layer
HTML, CSS, and JavaScript for upload, preview, and redaction selection

API Layer
FastAPI handles routing, validation, and orchestration

Processing Layer

OCR engine for images

PDF and Office document parsers

Redaction logic and masking engine

Deployment Layer
Hosted using Uvicorn on Render with optional Docker support

5️⃣ Technology Stack
Layer	Technology
Backend Framework	FastAPI
Server	Uvicorn
OCR Engine	Tesseract (pytesseract)
PDF Processing	PyMuPDF
Image Processing	OpenCV, Pillow
Document Handling	python-docx, openpyxl
Frontend	HTML, CSS, JavaScript
Deployment	Render
Containerization	Docker (optional)
6️⃣ Project Structure
file-level-redaction/
│
├── app/
│   ├── main.py              # FastAPI routes and API logic
│   ├── redact.py            # Detection and redaction engine
│   └── __init__.py
│
├── static/
│   ├── index.html           # Upload & preview UI
│   ├── docs.html            # Documentation UI
│   ├── styles.css
│   └── js/
│       ├── auth.js
│       └── selector.js
│
├── scripts/
│   ├── cleanup_and_remove.ps1
│   └── push_to_github.ps1
│
├── tests/                   # Extendable test cases
├── tools/
│   ├── architecture.md
│   ├── SoftwareRequirements.md
│   ├── test.md
│   └── text.md
│
├── requirements.txt
├── render.yaml
├── Dockerfile
├── README.md
└── LICENSE

7️⃣ Deployment Details

Hosting Platform: Render

ASGI Server: Uvicorn

Start Command

uvicorn app.main:app --host 0.0.0.0 --port 10000


Health Check Endpoint

GET /health
Response: { "status": "ok" }

8️⃣ Testing Strategy
✅ Functional Tests

Valid document uploads

Accurate detection of emails and phone numbers

Successful preview rendering

Cross-format auto-redaction

❌ Negative Tests

Unsupported file formats

Corrupted or invalid files

Missing OCR dependencies

Invalid request payloads

⚠️ Edge Case Tests

Large, multi-page PDFs

High-resolution images

Overlapping redaction regions

Repeated sensitive data patterns

(Detailed test cases available in test.md)

9️⃣ Security & Privacy Design

No user authentication (MVP scope)

Files processed in memory only

No external or persistent file storage

Redaction logs can be sanitized

Designed to prevent accidental PII exposure

🔟 Known Limitations

PDF redaction is visual (text layer may still exist)

Encrypted PDFs are not supported

OCR accuracy depends on input quality

Large files may affect performance on free hosting tiers

1️⃣1️⃣ Future Enhancements

Permanent PDF redaction using native APIs

Multilingual OCR support

Batch file processing

Authentication & role-based access control

Audit logs and confidence scoring

Cloud storage integration (S3, GCS)

1️⃣2️⃣ License

This project is released under the MIT License.
Refer to the LICENSE file for full terms.
