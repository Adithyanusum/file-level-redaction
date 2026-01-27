from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import io, json
from . import redact

app = FastAPI(title="File Redaction Hackathon")
app.mount("/static", StaticFiles(directory="static"), name="static")

# allow requests from local dev servers (e.g. Live Server on :5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permissive for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    print("[app] startup complete")


@app.on_event("shutdown")
def on_shutdown():
    print("[app] shutdown")


@app.get('/health')
def health():
    return JSONResponse({'status': 'ok'})


@app.post("/redact/image")
async def redact_image(file: UploadFile = File(...), regions: str = Form(None), mode: str = Form("blackout")):
    data = await file.read()
    regions_list = json.loads(regions) if regions else []
    out_bytes = redact.redact_image_bytes(data, regions_list, mode)
    return StreamingResponse(io.BytesIO(out_bytes), media_type=file.content_type)


@app.post("/redact/pdf")
async def redact_pdf(file: UploadFile = File(...), regions: str = Form(None)):
    data = await file.read()
    regions_obj = json.loads(regions) if regions else []
    out_bytes = redact.redact_pdf_bytes(data, regions_obj)
    return StreamingResponse(io.BytesIO(out_bytes), media_type="application/pdf")


@app.post("/redact/docx")
async def redact_docx(file: UploadFile = File(...), phrases: str = Form(None)):
    data = await file.read()
    phrases_list = json.loads(phrases) if phrases else []
    out_bytes = redact.redact_docx_bytes(data, phrases_list)
    return StreamingResponse(io.BytesIO(out_bytes), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


@app.post("/redact/xlsx")
async def redact_xlsx(file: UploadFile = File(...), cells: str = Form(None), columns: str = Form(None)):
    data = await file.read()
    cells_list = json.loads(cells) if cells else []
    columns_list = json.loads(columns) if columns else []
    out_bytes = redact.redact_xlsx_bytes(data, cells_list, columns_list)
    return StreamingResponse(io.BytesIO(out_bytes), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get("/")
def home():
    return RedirectResponse(url='/static/indexx.html')


@app.post('/preview/pdf')
async def preview_pdf(file: UploadFile = File(...)):
    data = await file.read()
    try:
        out = redact.preview_pdf_first_page(data)
        return StreamingResponse(io.BytesIO(out), media_type='image/png')
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)


@app.post('/preview/docx')
async def preview_docx(file: UploadFile = File(...)):
    data = await file.read()
    try:
        out = redact.preview_docx_bytes(data)
        return StreamingResponse(io.BytesIO(out), media_type='image/png')
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)


@app.post('/preview/xlsx')
async def preview_xlsx(file: UploadFile = File(...)):
    data = await file.read()
    try:
        out = redact.preview_xlsx_bytes(data)
        return StreamingResponse(io.BytesIO(out), media_type='image/png')
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)


@app.post('/detect')
async def detect(file: UploadFile = File(...)):
    data = await file.read()
    name = file.filename.lower()
    if name.endswith('.pdf'):
        res = redact.detect_pdf_bytes(data)
        return JSONResponse(res)
    if name.endswith('.docx'):
        res = redact.detect_docx_bytes(data)
        return JSONResponse(res)
    if name.endswith('.xlsx'):
        res = redact.detect_xlsx_bytes(data)
        return JSONResponse(res)
    # image
    res = redact.detect_image_bytes(data)
    return JSONResponse({'matches': res})
