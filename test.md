Project Test Cases — Redaction Project

I used the TC-01..TC-29 matrix as my baseline and added redaction-specific tests below. I grouped tests into Positive, Negative and Edge cases and noted current status and next steps.

Positive tests (should pass)
- R-P1: Detect PAN / Tax IDs in text and redact (exact pattern). Test: submit a document containing a PAN and verify masked output. [tests/test_redact.py::test_detect_pan_and_redact] — Working
- R-P2: Detect Aadhaar with valid Verhoeff checksum and redact. Test: feed Aadhaar-like number with valid Verhoeff → redacted. [tests/test_redact.py::test_aadhaar_verhoeff] — Working
- R-P3: Detect credit card numbers that pass Luhn and redact (mask digits). Test: insert card numbers in text/image and verify masked output. [tests/test_redact.py::test_credit_card_luhn] — Working
- R-P4: Detect IBAN/IFSC/account numbers and redact when context matches bank patterns. [tests/test_redact.py::test_bank_details_detection] — Working
- R-P5: OCR images to find text-based sensitive data and map rectangles for preview. [tests/test_redact_image.py::test_ocr_image_mapping] — Working (clear images)
- R-P6: Detect API keys / JWT-like tokens and redact (pattern + heuristics). [tests/test_redact.py::test_api_key_jwt_detection] — Working
- R-P7: Phrase queueing: add selected phrase in the UI, re-run detection server-side, map rects and update preview immediately. [tests/test_ui.py::test_phrase_queueing_updates_preview] — Working
- R-P8: Office redaction: redact embedded images/media in DOCX/XLSX and mask text in HTML preview. [tests/test_office.py::test_docx_xlsx_media_redact] — Working
- R-P9: Same-tab download: clicking Redact downloads the redacted artifact in the same tab (or triggers download) and the artifact shows expected masking. [tests/test_export.py::test_same_tab_download_redacted] — Working

Negative tests (should not redact or should fail safely)
- R-N1: Do not redact numbers that fail checksums (Luhn/Verhoeff). [tests/test_redact.py::test_invalid_checksum_not_redacted] — Working
- R-N2: Unsupported file types return a clear 400 error. [tests/test_redact_api.py::test_unsupported_file_type_error] — Working
- R-N3: Adding empty or duplicate phrases is handled gracefully (no crash, dedupe applied). [tests/test_ui.py::test_phrase_add_invalid_or_duplicate] — Working
- R-N4: Extremely large uploads beyond configured limits return 413 or appropriate error. [tests/test_redact_api.py::test_large_file_rejected] — Needs CI test

Edge tests (boundary, concurrency, complex layout)
- R-E1: Multi-page PDF with repeated sensitive data on several pages — redaction applied on all pages with preserved page mapping. [tests/test_redact.py::test_multipage_pdf_redaction] — Needs tests
- R-E2: Overlapping/adjacent matches should merge into a single redaction region rather than draw duplicates. [tests/test_redact.py::test_overlapping_matches_merge] — Needs tests
- R-E3: Rotated or tiny-font text in PDFs/images — OCR or sliding-window word-box fallback maps correctly or gracefully degrades. [tests/test_redact_image.py::test_rotated_text_ocr] — Partially working, needs improvement
- R-E4: Phrase spans line-breaks or hyphenation — multi-word sliding-window matching maps the phrase. [tests/test_redact.py::test_phrase_spanning_line_breaks] — Edge / Needs tests
- R-E5: Concurrent redaction API requests (race conditions) — temp file isolation and no data corruption. [tests/test_concurrency.py::test_concurrent_redaction_requests] — Needs tests

What's working (redaction-specific)
- Checksum validators (Verhoeff for Aadhaar, Luhn for cards) are implemented and used to reduce false positives.
- Broad regex detectors (PAN, IBAN, IFSC, generic account) are in place.
- OCR mapping for clear images and embedded OOXML media blur/redaction are implemented.
- Phrase queueing and immediate preview updates in the UI are implemented.
- Same-tab download flow and office HTML masking exist.

What's not working / incomplete
- OCR on noisy, rotated, or very small text is flaky and needs better thresholds and tests.
- Phrase→rect mapping can fail on complex PDFs (heavy formatting, multiple columns); needs more tests and heuristics tuning.
- Automated tests for redaction are incomplete — multi-page, overlapping-match, concurrency and stress tests are missing.

Future work (priority)
1. Implement `tests/test_redact.py` covering R-P1..R-P4 and R-N1 using small synthetic fixtures with known values (positive and negative checksum cases).
2. Add `tests/test_redact_image.py` for OCR mapping scenarios (clear, rotated, noisy) and `tests/test_office.py` for DOCX/XLSX embedded media behavior.
3. Add end-to-end smoke tests: upload sample PDF/DOCX/XLSX/image, queue phrase, confirm preview mask, download redacted artifact and validate content.
4. Add concurrency tests and temp-dir isolation for CI to ensure parallel runs are safe.
5. Run CI (GitHub Actions) to run tests and block merges on failures.

How I classified tests
- Positive cases: detection and redaction behavior when input matches known patterns and checksums.
- Negative cases: inputs that are malformed, unsupported, or intentionally invalid to confirm no false redactions and correct error handling.
- Edge cases: multi-page, rotated/obfuscated inputs, concurrency and performance boundaries.

If you want I will scaffold `tests/test_redact.py` and `tests/test_redact_image.py` with placeholder fixtures and a small fixture generator under `tests/fixtures/`. Say “Scaffold tests” to proceed.
