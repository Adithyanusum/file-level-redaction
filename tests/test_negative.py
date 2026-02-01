import requests
import os

def test_pdf_negative_no_redaction(base_url):
    path = "test_data/sample_clean.pdf"
    assert os.path.exists(path)

    with open(path, "rb") as f:
        r = requests.post(
            f"{base_url}/redact/pdf",
            files={"file": f}
        )

    assert r.status_code == 200

    # No sensitive data → should not redact
    assert r.headers.get("X-Redacted") == "false"
    print("NEGATIVE TEST: Clean PDF not redacted")
