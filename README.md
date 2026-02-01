🛡️ FILE-LEVEL REDACTION WEB APPLICATION

====================================================================

A secure, extensible, and production-ready web application for detecting and redacting sensitive information from digital documents.
Built using FastAPI, the system supports PDF, Image, DOCX, and XLSX files with manual, phrase-based, and automatic redaction.

====================================================================

🔷 1️⃣ EXECUTIVE SUMMARY

Organizations frequently handle documents containing Personally Identifiable Information (PII) such as email addresses, phone numbers, government IDs, and confidential text.
Improper handling of such data can lead to privacy breaches, compliance violations, and data leaks.

This project provides a file-level redaction platform that allows users to:

📤 Upload documents securely

🔍 Detect sensitive information

👀 Preview content before redaction

✂️ Apply redaction reliably

📥 Download sanitized documents

The system is designed with security, accuracy, modularity, and scalability as core principles.

====================================================================

🔷 2️⃣ CORE CAPABILITIES
🔍 Sensitive Data Detection

OCR-based text extraction for image files

Native text extraction from PDF, DOCX, and XLSX

Phrase-based detection using custom patterns

Automatic fallback detection for common PII types

✂️ Redaction Methods

Manual region-based redaction

Phrase-based redaction

Fully automatic redaction

Supports blackout and blur styles

Multi-page PDF redaction support

👀 Preview & Validation

PDF first-page preview

DOCX preview (HTML / Image rendering)

XLSX preview (HTML / Image rendering)

User confirmation before final redaction

====================================================================

🔷 3️⃣ SUPPORTED FILE FORMATS
Category	Formats
Documents	PDF, DOCX, XLSX
Images	PNG, JPG, JPEG, TIFF, BMP

====================================================================

🔷 4️⃣ SYSTEM ARCHITECTURE OVERVIEW

The application follows a layered, modular architecture:

Frontend Layer
HTML, CSS, and JavaScript for file upload, preview, and redaction selection

API Layer
FastAPI handles routing, validation, and orchestration

Processing Layer

OCR engine for images

PDF and Office document parsers

Redaction and masking engine

Deployment Layer
Uvicorn-based deployment on Render with optional Docker support

====================================================================

🔷 5️⃣ TECHNOLOGY STACK
Layer	Technology
Backend Framework	FastAPI
ASGI Server	Uvicorn
OCR Engine	Tesseract (pytesseract)
PDF Processing	PyMuPDF
Image Processing	OpenCV, Pillow
Document Handling	python-docx, openpyxl
Frontend	HTML, CSS, JavaScript
Deployment	Render
Containerization	Docker (optional)

====================================================================

🔷 6️⃣ PROJECT STRUCTURE
file-level-redaction/
├── app/
│   ├── main.py              # FastAPI routes
│   ├── redact.py            # Detection & redaction logic
│   ├── init.py
│   └── static/
│       ├── index.html
│       ├── docs.html
│       ├── styles.css
│       ├── js/
│       │   ├── auth.js
│       │   └── selector.js
│       └── scripts/
├── cleanup_and_remove.ps1   # Dev script
├── push_to_github.ps1       # Dev script
├── tests/                   # Test cases (optional/extendable)
├── tools/                   # Dev helpers
│   ├── architecture.md
│   ├── SoftwareRequirements.md
│   ├── test.md
│   └── text.md
├── requirements.txt         # Python dependencies
├── render.yaml              # Render deployment config
├── Dockerfile               # Containerization config
├── README.md                # Project documentation
└── LICENSE                  # MIT License

====================================================================

🔷 7️⃣ DEPLOYMENT DETAILS

Hosting Platform: Render

ASGI Server: Uvicorn

▶️ Start Command
uvicorn app.main:app --host 0.0.0.0 --port 10000

❤️ Health Check
GET /health
Response: { "status": "ok" }


====================================================================

🔷 8️⃣ TESTING STRATEGY
✅ Functional Tests

Valid document uploads

Accurate detection of emails and phone numbers

Successful preview rendering

Cross-format auto-redaction

❌ Negative Tests

Unsupported file formats

Corrupted files

Invalid request payloads

Missing OCR dependencies

⚠️ Edge Case Tests

Large multi-page PDFs

High-resolution images

Overlapping redaction regions

Repeated sensitive data patterns

====================================================================

🔷 9️⃣ SECURITY & PRIVACY DESIGN

No authentication (MVP scope)

Files processed entirely in memory

No persistent external storage

Sanitized redaction logs

Designed to minimize PII exposure risks

====================================================================

🔷 🔟 KNOWN LIMITATIONS

PDF redaction is visual-only

Encrypted PDFs not supported

OCR accuracy depends on image quality

Large files may impact performance

====================================================================

🔷 1️⃣1️⃣ FUTURE ENHANCEMENTS

Permanent PDF redaction

Multilingual OCR

Batch file uploads

Authentication & RBAC

Audit logs and confidence scoring

Cloud storage integration

====================================================================

🔷 1️⃣2️⃣ LICENSE

This project is licensed under the MIT License.
See the LICENSE file for full details.

====================================================================
