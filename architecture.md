# Architecture – File Redaction Web Application

## 1) Overview

The **File Redaction Web Application** is a lightweight, web-based system designed to **detect and redact sensitive information (PII)** from documents and images.  
The MVP targets **single-user, stateless operation**, prioritizing privacy, safety, and robustness.

The backend is implemented using **FastAPI**, while the frontend uses **HTML/CSS/JavaScript**.  
Files are processed **in-memory** without persistence, and the system can be containerized using **Docker** for consistent deployment.

---

## 2) High-Level System Architecture

### Logical Components
- **User Interface**
  - File upload
  - Preview
  - Redaction controls
  - Download

- **API Layer (FastAPI)**
  - Upload & validation endpoints
  - Preview endpoints
  - Detection & redaction endpoints

- **Processing Layer**
  - Detection Engine (regex + context)
  - OCR Engine (optional – Tesseract)
  - Redaction Engine (PDF, Image, DOCX, XLSX)

---

## 3) System Context Diagram

```mermaid
graph TD
    User -->|Uploads File| UI
    UI -->|HTTP Requests| FastAPI
    FastAPI --> DetectionEngine
    FastAPI --> RedactionEngine
    RedactionEngine -->|Redacted File| User
```

4) Container / Component Diagram
```mermaid
graph LR
    Browser[Web Browser] --> API[FastAPI Server]

    API --> PDF[PDF Processor]
    API --> IMG[Image Processor]
    API --> DOCX[DOCX Processor]
    API --> XLSX[XLSX Processor]

    API --> OCR[OCR Engine (Optional)]
```

5) Frontend Architecture
Pages

Upload & Redaction Page

Preview Page

Download Confirmation

UI Modules

FileUploader

PreviewViewer

RedactionCanvas (manual regions)

PhraseInputPanel

AutoRedactButton

DownloadPanel

6) User Flow Diagram
```mermaid
flowchart TD
    A[User Uploads File] --> B[File Validation]
    B --> C[Preview Generated]
    C --> D{Redaction Type}
    D -->|Manual| E[Select Regions]
    D -->|Phrase-Based| F[Enter Phrases]
    D -->|Auto| G[Auto Detect PII]
    E --> H[Apply Redaction]
    F --> H
    G --> H
    H --> I[Download Redacted File]
```

7) Use Case Diagram
```mermaid
graph TD
    User --> UploadFile
    User --> PreviewFile
    User --> DetectSensitiveData
    User --> RedactFile
    User --> DownloadFile
```

8) Sequence Diagram – Preview Flow
```mermaid
sequenceDiagram
    User->>UI: Upload file
    UI->>API: POST /preview
    API->>Processor: Generate preview
    Processor->>API: Preview output
    API->>UI: Preview response
```

9) Sequence Diagram – Auto Redaction Flow
```mermaid
sequenceDiagram
    User->>API: POST /redact/auto
    API->>DetectionEngine: Detect sensitive data
    DetectionEngine->>RedactionEngine: Provide regions
    RedactionEngine->>API: Redacted file
    API->>User: Download response
```

10) Data Flow Diagram
```mermaid
flowchart LR
    U[User] -->|File| API
    API --> Detect[Detection Engine]
    Detect --> API
    API --> Redact[Redaction Engine]
    Redact --> API
    API -->|Redacted File| U
```

11) Conceptual Data Model (ER Diagram)
```mermaid
erDiagram
    FILE ||--o{ REGION : has
    FILE ||--o{ MATCH : detects

    FILE {
        string filename
        string type
        int size
    }

    REGION {
        float x
        float y
        float width
        float height
    }

    MATCH {
        string text
        string category
    }
```

12) Security & Privacy Considerations

No user authentication (MVP scope)

No file or text persistence

Files processed in-memory per request

No external data transmission by default

Debug logging disabled in production mode

13) Scalability & Future Enhancements

Permanent PDF redaction (apply_redactions)

Batch file uploads

Password-protected PDF support

Authentication & RBAC

Audit logs for compliance

Separate UI and API containers

Cloud deployment (AWS / Azure)

14) Summary

This architecture ensures modularity, privacy, and reliability, making the File Redaction Web Application suitable for secure document handling while remaining extensible for future enterprise features. (See <attachments> above for file contents. You may not need to search or read the file again.)
