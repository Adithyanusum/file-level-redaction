import requests
import os

def test_pdf_edge_empty_file(base_url):
    path = "test_data/sample_empty.pdf"
    assert os.path.exists(path)

    with open(path, "rb") as f:
        r = requests.post(
            f"{base_url}/redact/pdf",
            files={"file": f}
        )

    # App should NOT crash
    assert r.status_code == 200
    print("EDGE TEST: Empty PDF handled safely")
