# Project Plan (MVP) – File Redaction System  
**Development Methodology: Agile Software Development**

The File Redaction System was developed using an **Agile, sprint-based approach**, focusing on delivering a working MVP quickly and iterating based on testing and feedback.

---

## 1) Agile Milestones (Sprints)

### 🟢 Sprint 0: Discovery & Planning (Day 1)
- Finalize project scope and MVP goals
- Identify supported file formats (PDF, Image, DOCX, XLSX)
- Define sensitive data categories (email, phone, ID, etc.)
- Finalize API endpoints and redaction modes
- Prepare sample test files

---

### 🟢 Sprint 1: Core Backend Setup (Day 1–2)
- Initialize FastAPI project structure
- Implement `/health` endpoint
- Configure CORS and static file hosting
- Setup redaction utility module (`redact.py`)
- Add basic error handling

---

### 🟢 Sprint 2: Core Redaction Features (Day 2–3)
- Implement image redaction (blackout & blur)
- Implement PDF redaction (region-based and phrase-based)
- Implement DOCX text masking
- Implement XLSX cell, row, and column masking
- Handle multi-page PDFs and coordinate mapping

---

### 🟢 Sprint 3: Detection & Automation (Day 3)
- Implement sensitive data detection (email, phone, ID patterns)
- Integrate OCR for images using Tesseract
- Implement `/detect` API
- Implement `/redact/auto` endpoint
- Add fallback detection logic

---

### 🟢 Sprint 4: Preview & UX Support (Day 4)
- Implement PDF preview generation
- Implement DOCX preview (image + HTML)
- Implement XLSX preview
- Implement text extraction endpoint
- Validate canvas-to-PDF coordinate conversion

---

### 🟢 Sprint 5: Testing, Optimization & Polish (Day 4–5)
- Execute positive, negative, and edge test cases
- Fix OCR and PDF redaction bugs
- Improve error resilience and fail-safe behavior
- Optimize performance for large files
- Finalize project documentation

---

## 2) Task Breakdown (Agile Backlog)

### 🔹 Backend (FastAPI)
- Define REST APIs for redaction, preview, detect, and extract
- Implement file upload handling
- Implement redaction logic for each file type
- Implement auto-redaction workflow
- Add response headers and metadata

---

### 🔹 Redaction Engine
- Regex-based sensitive data detection
- Context-aware filtering to avoid false positives
- OCR-based text extraction for images
- Region mapping for PDFs
- Blur and blackout image processing

---

### 🔹 Preview & Utility Services
- PDF to image preview conversion
- DOCX to HTML/image preview
- XLSX table preview generation
- Safe fallback handling for unsupported files

---

### 🔹 Data & Configuration
- In-memory processing (no persistent file storage)
- Configurable redaction modes
- Optional OCR availability detection

---

### 🔹 DevOps & Deployment
- Define requirements.txt
- Local development using Uvicorn
- Dockerfile for containerized execution (future-ready)
- README and run instructions

---

## 3) MVP Deliverables

- Functional File Redaction Web API
- Support for PDF, Image, DOCX, and XLSX files
- Manual, phrase-based, and auto redaction
- Preview before redaction
- Comprehensive testing documentation
- Demo-ready application

---

## 4) Risks & Mitigations

| Risk | Mitigation |
|----|----|
| Time constraints | Focus on MVP features first |
| OCR inaccuracies | Use context-based detection & fallback |
| Large file performance | Limit file size & optimize processing |
| False positives | Context-aware regex filtering |
| PDF text not permanently removed | Document as limitation |
| Dependency issues (OCR) | Graceful fallback if unavailable |

---

## 5) Testing Checklist (Sprint Validation)

- Upload and preview file
- Detect sensitive data
- Redact manually selected regions
- Perform phrase-based redaction
- Run auto-redaction
- Validate output file integrity
- Test invalid and edge inputs

---

## 

> **“The File Redaction System was developed using Agile methodology, delivering an MVP through incremental sprints that focused on core redaction, detection, preview, and testing, ensuring flexibility, rapid feedback, and continuous improvement.”**
