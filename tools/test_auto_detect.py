import fitz
import io
import httpx

# create a simple PDF with sensitive text
doc = fitz.open()
page = doc.new_page()
text = "Contact: alice@example.com  Phone: +1 555-123-4567\nAccount: 123456789012"
page.insert_text(fitz.Point(72, 72), text, fontsize=12)
buf = io.BytesIO()
doc.save(buf)
doc.close()
buf.seek(0)

with open('test_doc.pdf','wb') as f:
    f.write(buf.getvalue())

print('Saved test_doc.pdf')

# POST to /detect
files = {'file': ('test_doc.pdf', open('test_doc.pdf','rb'), 'application/pdf')}
try:
    r = httpx.post('http://127.0.0.1:8000/detect', files=files, timeout=10.0)
    print('detect status:', r.status_code)
    print('detect json:', r.text)
except Exception as e:
    print('detect error', e)

# POST to /preview/pdf
try:
    r2 = httpx.post('http://127.0.0.1:8000/preview/pdf', files=files, timeout=10.0)
    print('preview status:', r2.status_code)
    if r2.status_code==200:
        with open('preview_output.png','wb') as f:
            f.write(r2.content)
        print('Wrote preview_output.png')
    else:
        print('preview failed', r2.text)
except Exception as e:
    print('preview error', e)
