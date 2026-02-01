import requests
import os

def test_image_redaction(base_url):
    file_path = "test_data/sample_sensitive.png"
    assert os.path.exists(file_path)

    with open(file_path, "rb") as f:
        response = requests.post(
            f"{base_url}/redact/image",
            files={"file": f},
            data={"mode": "blackout"}
        )

    assert response.status_code == 200
    print("Image redaction test PASSED")
