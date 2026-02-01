🛡️ SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
FILE-LEVEL REDACTION WEB APPLICATION

================================================================================

📌 Document Control

Project Title: File-Level Redaction Web Application

Document Type: Software Requirements Specification (SRS)

Version: 1.0

Prepared By: Your Name

Technology Stack: FastAPI, OCR, PDF/Image Processing

Intended Audience: Developers, Evaluators, Instructors

================================================================================

🔷 1️⃣ INTRODUCTION
1.1 Purpose

This document specifies the functional and non-functional requirements for the File-Level Redaction Web Application.
The system enables users to detect, preview, and redact sensitive information from uploaded documents in a secure and reliable manner.

1.2 Scope

The application supports:

Uploading documents (PDF, Images, DOCX, XLSX)

Detecting sensitive information (PII)

Manual, phrase-based, and automatic redaction

Previewing documents before redaction

Downloading sanitized output files

The system is designed for privacy-focused document handling without persistent storage.

1.3 Definitions, Acronyms, and Abbreviations
Term	Description
PII	Personally Identifiable Information
OCR	Optical Character Recognition
API	Application Programming Interface
SRS	Software Requirements Specification
MVP	Minimum Viable Product

================================================================================

🔷 2️⃣ OVERALL DESCRIPTION
2.1 Product Perspective

The application is a web-based document redaction system built using a client–server architecture.
The frontend interacts with a FastAPI backend which handles document processing, detection, and redaction.

2.2 Product Functions

Upload documents securely

Extract text from files

Detect sensitive information

Allow manual selection for redaction

Apply redaction (blur/blackout)

Generate previews

Provide downloadable redacted files

2.3 User Characteristics

Basic computer and browser knowledge

No technical expertise required

No authentication required (MVP)

2.4 Operating Environment

Web browser (Chrome, Firefox, Edge)

Backend server running FastAPI

OCR engine installed on server

Supported OS: Windows / Linux

2.5 Design Constraints

OCR accuracy depends on input quality

Free-tier hosting performance limits

Visual redaction only for PDFs (text layer may persist)

================================================================================

🔷 3️⃣ SYSTEM REQUIREMENTS
3.1 Functional Requirements
FR-1: File Upload

The system shall allow users to upload PDF, image, DOCX, and XLSX files.

The system shall reject unsupported file formats.

FR-2: Text Extraction

The system shall extract text from PDFs and Office documents.

The system shall use OCR for image-based files.

FR-3: Sensitive Data Detection

The system shall detect common PII (emails, phone numbers, IDs).

The system shall support phrase-based detection.

FR-4: Redaction

The system shall support manual region-based redaction.

The system shall support automatic redaction.

The system shall apply blur or blackout redaction styles.

FR-5: Preview

The system shall generate document previews before redaction.

The system shall allow user confirmation before final output.

FR-6: Download

The system shall allow users to download the redacted file.

3.2 Non-Functional Requirements
NFR-1: Performance

The system shall process documents within acceptable time limits.

Large files may take longer to process.

NFR-2: Security

Files shall be processed in memory.

No files shall be stored permanently by default.

NFR-3: Usability

The user interface shall be simple and intuitive.

Minimal user interaction required.

NFR-4: Reliability

The system shall handle invalid or corrupted files gracefully.

NFR-5: Scalability

The architecture shall support future enhancements such as batch uploads.

================================================================================

🔷 4️⃣ EXTERNAL INTERFACE REQUIREMENTS
4.1 User Interface

Web-based UI using HTML, CSS, and JavaScript

Upload, preview, redaction selection, and download screens

4.2 Software Interfaces

OCR Engine (Tesseract)

PDF processing libraries

Image processing libraries

4.3 Communication Interfaces

HTTP/HTTPS REST APIs

JSON request and response format

================================================================================

🔷 5️⃣ SYSTEM ARCHITECTURE OVERVIEW

Presentation Layer: Web UI

Application Layer: FastAPI backend

Processing Layer: OCR, document parsing, redaction engine

Deployment Layer: Uvicorn server hosted on cloud platform

================================================================================

🔷 6️⃣ ASSUMPTIONS AND DEPENDENCIES

OCR engine must be installed on the server

User provides readable and valid documents

Internet connection required for web access

================================================================================

🔷 7️⃣ FUTURE ENHANCEMENTS

Permanent PDF redaction

Multilingual OCR support

Authentication and access control

Audit logging

Cloud storage integration

================================================================================

🔷 8️⃣ APPENDIX

This SRS document serves as the baseline specification for the File-Level Redaction Web Application and may be updated as the system evolves.

================================================================================
