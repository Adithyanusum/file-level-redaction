import pytest


def test_detect_pan_and_redact(fixtures_dir, tmp_path):
    pytest.skip("skeleton: implement detection+redaction assertion using fixtures")


def test_aadhaar_verhoeff(fixtures_dir):
    pytest.skip("skeleton: implement Aadhaar Verhoeff positive/negative cases")


def test_credit_card_luhn(fixtures_dir):
    pytest.skip("skeleton: implement Luhn card detection + redaction test")


def test_bank_details_detection(fixtures_dir):
    pytest.skip("skeleton: implement IBAN/IFSC/account detection test")


def test_invalid_checksum_not_redacted(fixtures_dir):
    pytest.skip("skeleton: ensure invalid checksums are not redacted")


def test_multipage_pdf_redaction(fixtures_dir):
    pytest.skip("skeleton: multi-page PDF redaction test")
