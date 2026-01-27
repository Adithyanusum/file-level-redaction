import io, time, os
import json
import fitz
import psutil
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# create multi-page PDF (6 pages)
PAGE_COUNT = 6
buf = io.BytesIO()
doc = fitz.open()
for i in range(PAGE_COUNT):
    page = doc.new_page()
    text = f"Page {i+1}\nContact: user{i}@example.com\nPhone: +1 555-12{i:02d}-000{i}"
    page.insert_text(fitz.Point(72, 72), text, fontsize=12)
buf = io.BytesIO()
doc.save(buf)
doc.close()
buf.seek(0)

files = {'file': ('multipage.pdf', buf.getvalue(), 'application/pdf')}

proc = psutil.Process()
start_mem = proc.memory_info().rss
start_time = time.time()
res = client.post('/preview/pdf', files=files)
render_time = time.time() - start_time
end_mem = proc.memory_info().rss

print('preview status', res.status_code)
if res.status_code == 200:
    out_path = 'preview_multipage.png'
    with open(out_path, 'wb') as f:
        f.write(res.content)
    print('Wrote', out_path)
else:
    print('preview error', res.text)

# parse preview image size to estimate pages (we rendered pages stacked vertically)
from PIL import Image
im = Image.open('preview_multipage.png')
print('preview image size:', im.size)
# If page heights are equal, pages = total_height / single_page_height
# Render one page to get page height
# Render individually for comparison
single_pages = []
for p in range(PAGE_COUNT):
    doc = fitz.open(stream=buf.getvalue(), filetype='pdf')
    page = doc.load_page(p)
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0,2.0))
    single_pages.append(Image.open(io.BytesIO(pix.tobytes('png'))))
    doc.close()

page_heights = [p.height for p in single_pages]
page_widths = [p.width for p in single_pages]
print('single page sizes (w,h):', list(zip(page_widths, page_heights)))

estimated_pages = im.height // page_heights[0] if page_heights[0]>0 else 'unknown'
print('Estimated pages in preview image:', estimated_pages)
print('Total pages expected:', PAGE_COUNT)
print('Render time (s):', render_time)
print('Memory start (MB):', round(start_mem/1024/1024,2), 'end (MB):', round(end_mem/1024/1024,2))

# now test redact across pages: redact region from page 3 (index 2)
# detect first
buf_seek = io.BytesIO(buf.getvalue())
resd = client.post('/detect', files=files)
print('detect status', resd.status_code)
det = resd.json()
print('detect result sample:', det[2] if len(det)>2 else det)
# prepare regions for page 3
regions = []
if isinstance(det, list) and len(det)>2:
    for m in det[2]['matches']:
        regions.append({'page': 2, 'rect': m['rect']})

multipart = {}
multipart.update(files)
multipart['regions'] = (None, json.dumps(regions))
resr = client.post('/redact/pdf', files=multipart)
print('redact status', resr.status_code)
if resr.status_code==200:
    with open('redacted_multipage.pdf','wb') as f:
        f.write(resr.content)
    print('Wrote redacted_multipage.pdf')
else:
    print('redact error', resr.text)
