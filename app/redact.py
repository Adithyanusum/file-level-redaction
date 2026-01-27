import io
import cv2
import numpy as np
import fitz
from docx import Document
from openpyxl import load_workbook
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import re
try:
    import pytesseract
except Exception:
    pytesseract = None


def redact_image_bytes(data: bytes, regions: list, mode: str = "blackout") -> bytes:
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError("Unable to decode image")
    for r in regions:
        # r expected [x, y, w, h]
        x, y, w, h = r
        x, y, w, h = int(x), int(y), int(w), int(h)
        if mode == "blur":
            roi = img[y:y+h, x:x+w]
            k = max(3, (w//7)|1)
            roi = cv2.GaussianBlur(roi, (k, k), 0)
            img[y:y+h, x:x+w] = roi
        else:
            if img.ndim == 3:
                img[y:y+h, x:x+w] = (0, 0, 0)
            else:
                img[y:y+h, x:x+w] = 0
    ext = ".png"
    success, out = cv2.imencode(ext, img)
    if not success:
        raise ValueError("Failed to encode image")
    return out.tobytes()


def redact_pdf_bytes(data: bytes, regions: list) -> bytes:
    # regions: list of {"page": int, "rect": [x0,y0,x1,y1]}
    doc = fitz.open(stream=data, filetype="pdf")
    for item in regions:
        page_no = int(item.get("page", 0))
        rect = item.get("rect")
        if rect is None:
            continue
        x0, y0, x1, y1 = map(float, rect)
        page = doc.load_page(page_no)
        shape = page.new_shape()
        shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
        shape.finish(fill=(0, 0, 0))
        shape.commit()
    buf = io.BytesIO()
    doc.save(buf)
    doc.close()
    return buf.getvalue()


def redact_docx_bytes(data: bytes, phrases: list) -> bytes:
    buf = io.BytesIO(data)
    doc = Document(buf)
    def mask_text(s):
        return "█" * len(s)
    for p in doc.paragraphs:
        text = p.text
        for ph in phrases:
            if ph in text:
                new = text.replace(ph, mask_text(ph))
                # crude replacement: clear runs then set single run
                for r in list(p.runs):
                    r.text = ""
                p.add_run(new)
                break
    # also redact inside tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text = cell.text
                for ph in phrases:
                    if ph in text:
                        new = text.replace(ph, mask_text(ph))
                        # clear paragraphs in cell and insert new text
                        for cp in list(cell.paragraphs):
                            for r in list(cp.runs):
                                r.text = ""
                        # put new text into first paragraph
                        if cell.paragraphs:
                            cell.paragraphs[0].add_run(new)
                        break
    out = io.BytesIO()
    doc.save(out)
    out_bytes = out.getvalue()
    # blur embedded images in the docx package (word/media)
    try:
        out_bytes = blur_media_in_ooxml(out_bytes, prefixes=('word/media/',))
    except Exception:
        pass
    return out_bytes


def redact_xlsx_bytes(data: bytes, cells: list, columns: list) -> bytes:
    buf = io.BytesIO(data)
    wb = load_workbook(filename=buf)
    for ws in wb.worksheets:
        # mask specific cells like "A1", "B2"
        for c in cells:
            try:
                cell = ws[c]
                cell.value = "REDACTED"
            except Exception:
                continue
        # mask entire columns like "C" or index
        for col in columns:
            for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
                try:
                    if isinstance(col, int):
                        row[col-1].value = "REDACTED"
                    else:
                        # assume column letter
                        cell = ws[f"{col}{row[0].row}"]
                        cell.value = "REDACTED"
                except Exception:
                    continue
    out = io.BytesIO()
    wb.save(out)
    out_bytes = out.getvalue()
    # blur embedded images in the xlsx package (xl/media)
    try:
        out_bytes = blur_media_in_ooxml(out_bytes, prefixes=('xl/media/',))
    except Exception:
        pass
    return out_bytes


EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"\+?\d[\d\s\-\(\)]{6,}\d")
ACC_RE = re.compile(r"\b\d{8,16}\b")


def preview_pdf_first_page(data: bytes, zoom: float = 2.0) -> bytes:
    # Render all pages and concatenate vertically into one PNG
    doc = fitz.open(stream=data, filetype="pdf")
    images = []
    try:
        for pno in range(len(doc)):
            page = doc.load_page(pno)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            images.append(img)
        if not images:
            return b""
        # concatenate vertically
        widths = [im.width for im in images]
        heights = [im.height for im in images]
        maxw = max(widths)
        totalh = sum(heights)
        out_img = Image.new('RGB', (maxw, totalh), color='white')
        y = 0
        for im in images:
            out_img.paste(im, (0, y))
            y += im.height
        out = io.BytesIO()
        out_img.save(out, format='PNG')
        return out.getvalue()
    finally:
        doc.close()


def detect_pdf_bytes(data: bytes):
    doc = fitz.open(stream=data, filetype="pdf")
    results = []
    for pno in range(len(doc)):
        page = doc.load_page(pno)
        text = page.get_text()
        matches = []
        for pattern in (EMAIL_RE, PHONE_RE, ACC_RE):
            for m in pattern.findall(text):
                # search on page for the exact text
                try:
                    areas = page.search_for(m)
                    for r in areas:
                        matches.append({"text": m, "rect": [r.x0, r.y0, r.x1, r.y1]})
                except Exception:
                    continue
        if matches:
            results.append({"page": pno, "matches": matches})
    doc.close()
    return results


def detect_docx_bytes(data: bytes):
    buf = io.BytesIO(data)
    doc = Document(buf)
    found = []
    # check paragraphs
    for p in doc.paragraphs:
        t = p.text
        for pattern in (EMAIL_RE, PHONE_RE, ACC_RE):
            for m in pattern.findall(t):
                found.append(m)
    # check tables (cells)
    try:
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    t = cell.text
                    for pattern in (EMAIL_RE, PHONE_RE, ACC_RE):
                        for m in pattern.findall(t):
                            found.append(m)
    except Exception:
        pass
    # also report embedded images (filenames) if present
    imgs = []
    try:
        # inspect package for word/media
        import zipfile
        z = zipfile.ZipFile(io.BytesIO(data))
        for name in z.namelist():
            if name.startswith('word/media/'):
                imgs.append(name.split('/')[-1])
        z.close()
    except Exception:
        pass
    res = list(set(found))
    return {'text_matches': res, 'images': imgs}


def detect_xlsx_bytes(data: bytes):
    buf = io.BytesIO(data)
    wb = load_workbook(filename=buf)
    found = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=False):
            for cell in row:
                val = cell.value
                if not isinstance(val, str):
                    continue
                for pattern in (EMAIL_RE, PHONE_RE, ACC_RE):
                    for m in pattern.findall(val):
                        found.append({"sheet": ws.title, "cell": cell.coordinate, "match": m})
    # also list images in xl/media
    imgs = []
    try:
        import zipfile
        z = zipfile.ZipFile(io.BytesIO(data))
        for name in z.namelist():
            if name.startswith('xl/media/'):
                imgs.append(name.split('/')[-1])
        z.close()
    except Exception:
        pass
    return {'text_matches': found, 'images': imgs}


def blur_media_in_ooxml(data: bytes, prefixes=('word/media/', 'xl/media/')) -> bytes:
    """Open OOXML package bytes, blur images under given prefixes, and return new package bytes."""
    import zipfile
    inbuf = io.BytesIO(data)
    outbuf = io.BytesIO()
    with zipfile.ZipFile(inbuf, 'r') as zin:
        with zipfile.ZipFile(outbuf, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                name = item.filename
                raw = zin.read(name)
                # blur if path matches prefixes and file looks like an image
                if any(name.startswith(p) for p in prefixes):
                    try:
                        im = Image.open(io.BytesIO(raw)).convert('RGBA')
                        im = im.filter(ImageFilter.GaussianBlur(radius=8))
                        wb = io.BytesIO()
                        # preserve original format
                        fmt = im.format or ('PNG' if name.lower().endswith('.png') else 'JPEG')
                        im.save(wb, format=fmt)
                        raw = wb.getvalue()
                    except Exception:
                        pass
                zout.writestr(name, raw)
    return outbuf.getvalue()


def detect_image_bytes(data: bytes):
    if pytesseract is None:
        return {"error": "pytesseract not installed"}
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return {"error": "cannot decode image"}
    # use pytesseract to get word boxes
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    matches = []
    n = len(d['text'])
    for i in range(n):
        txt = d['text'][i]
        if not txt or txt.strip()=='' :
            continue
        for pattern in (EMAIL_RE, PHONE_RE, ACC_RE):
            if pattern.search(txt):
                x = int(d['left'][i]); y = int(d['top'][i]); w = int(d['width'][i]); h = int(d['height'][i])
                matches.append({"text": txt, "rect": [x, y, w, h]})
                break
    return matches


def preview_docx_bytes(data: bytes, width: int = 800, line_height: int = 18) -> bytes:
    buf = io.BytesIO(data)
    doc = Document(buf)
    lines = []
    for p in doc.paragraphs:
        text = p.text.strip()
        if text:
            lines.append(text)
    # include table cell contents for preview
    try:
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text.strip()
                    if text:
                        lines.append(text)
    except Exception:
        pass
    # create image and draw text
    font = None
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    img_h = max(200, line_height * (len(lines) + 2))
    out_img = Image.new('RGB', (width, img_h), color='white')
    draw = ImageDraw.Draw(out_img)
    y = 10
    for l in lines:
        draw.text((10, y), l, fill='black', font=font)
        y += line_height
    out = io.BytesIO()
    out_img.save(out, format='PNG')
    return out.getvalue()


def preview_xlsx_bytes(data: bytes, width: int = 800, row_h: int = 24) -> bytes:
    buf = io.BytesIO(data)
    wb = load_workbook(filename=buf, data_only=True)
    ws = wb.active
    # collect cell values for first 10 rows/10 cols
    max_rows = min(20, ws.max_row)
    max_cols = min(10, ws.max_column)
    cell_texts = []
    col_width = max(60, width // max_cols)
    img_h = max(200, row_h * (max_rows + 1))
    out_img = Image.new('RGB', (col_width * max_cols, img_h), color='white')
    draw = ImageDraw.Draw(out_img)
    font = None
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    # header
    y = 0
    for r in range(1, max_rows + 1):
        x = 0
        for c in range(1, max_cols + 1):
            val = ws.cell(row=r, column=c).value
            s = '' if val is None else str(val)
            draw.rectangle([x, y, x + col_width - 1, y + row_h - 1], outline='gray')
            draw.text((x + 4, y + 4), s, fill='black', font=font)
            x += col_width
        y += row_h
    out = io.BytesIO()
    out_img.save(out, format='PNG')
    return out.getvalue()
