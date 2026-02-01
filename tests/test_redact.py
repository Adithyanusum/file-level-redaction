import requests
import os

def test_pdf_redaction(base_url):
    file_path = "test_data/sample_sensitive.pdf"
    assert os.path.exists(file_path)

    with open(file_path, "rb") as f:
        response = requests.post(
            f"{base_url}/redact/pdf",
            files={"file": f},
            data={"phrases": '["ravi.kumar92@example.com"]'}
        )

    assert response.status_code == 200
    assert response.headers.get("X-Redacted") == "true"
    print("PDF redaction test PASSED")


def test_docx_redaction(base_url):
    file_path = "test_data/sample_sensitive.docx"
    assert os.path.exists(file_path)

    with open(file_path, "rb") as f:
        response = requests.post(
            f"{base_url}/redact/docx",
            files={"file": f},
            data={"phrases": '["+91 9876543210"]'}
        )

    assert response.status_code == 200
    print("DOCX redaction test PASSED")
