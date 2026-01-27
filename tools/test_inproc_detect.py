import fitz
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

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

r = client.post('/detect', files=files)
print('detect status', r.status_code)
print('detect json', r.json())

# preview
buf.seek(0)
r2 = client.post('/preview/pdf', files=files)
print('preview status', r2.status_code)
if r2.status_code==200:
    with open('preview_output.png','wb') as f:
        f.write(r2.content)
    print('Wrote preview_output.png')
else:
    print('preview failed', r2.text)
