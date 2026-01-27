import io
import json
import fitz
import cv2
import numpy as np
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pdf_redact():
    # create PDF with sensitive text
    doc = fitz.open()
    page = doc.new_page()
    text = "Contact: alice@example.com  Phone: +1 555-123-4567\nAccount: 123456789012"
    page.insert_text(fitz.Point(72, 72), text, fontsize=12)
    buf = io.BytesIO()
    doc.save(buf)
    doc.close()
    buf.seek(0)

    files = {'file': ('test_doc.pdf', buf.getvalue(), 'application/pdf')}
    # detect
    r = client.post('/detect', files=files)
    print('detect status', r.status_code)
    det = r.json()
    print('detect json', det)

    # convert detections to regions for redact (page rects expected)
    regions = []
    if isinstance(det, list) and det:
        for m in det[0]['matches']:
            x0,y0,x1,y1 = m['rect']
            regions.append({'page': 0, 'rect': [x0,y0,x1,y1]})

    fd = {'file': ('test_doc.pdf', buf.getvalue(), 'application/pdf')}
    data = {'regions': io.StringIO(str(regions))}
    # TestClient doesn't support both files+form in same call easily; post as multipart manually
    multipart = {}
    multipart.update(files)
    multipart['regions'] = (None, json.dumps(regions))
    res = client.post('/redact/pdf', files=multipart)
    print('redact status', res.status_code)
    if res.status_code==200:
        with open('redacted_test_doc.pdf','wb') as f:
            f.write(res.content)
        print('Wrote redacted_test_doc.pdf')

def test_image_redact():
    # create sample image with text
    img = np.full((200,400,3), 255, dtype=np.uint8)
    cv2.putText(img, 'Phone: +1 555-123-4567', (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
    success, out = cv2.imencode('.png', img)
    data = out.tobytes()
    files = {'file': ('test_img.png', data, 'image/png')}
    # choose region around text
    regions = [[10,30,300,30]]
    multipart = {}
    multipart.update(files)
    multipart['mode'] = (None, 'blur')
    multipart['regions'] = (None, json.dumps(regions))
    res = client.post('/redact/image', files=multipart)
    print('image redact status', res.status_code)
    if res.status_code==200:
        with open('redacted_test_img.png','wb') as f:
            f.write(res.content)
        print('Wrote redacted_test_img.png')

if __name__ == '__main__':
    test_pdf_redact()
    test_image_redact()
