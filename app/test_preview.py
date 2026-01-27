from fastapi.testclient import TestClient
from app.main import app
import fitz
import io

# create simple PDF in-memory
doc = fitz.open()
doc.new_page()
doc[0].insert_text((72,72), "Hello Preview PDF", fontsize=20)
buf = io.BytesIO()
doc.save(buf)
doc.close()
buf.seek(0)

client = TestClient(app)
files = {'file': ('sample.pdf', buf.getvalue(), 'application/pdf')}
resp = client.post('/preview/pdf', files=files)
print('status', resp.status_code)
print('content-type', resp.headers.get('content-type'))
open('preview_test.png','wb').write(resp.content)
print('Wrote preview_test.png')
