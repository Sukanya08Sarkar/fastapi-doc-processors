from fastapi import FastAPI, UploadFile, File
from typing import List
import fitz  # PyMuPDF

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is up!"}

@app.post("/process/")
async def process(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        text = extract_pdf_text(content) if file.filename.endswith('.pdf') else "Unsupported file type"
        results.append({"file_name": file.filename, "extracted_text": text})
    return {"attachments": results}

def extract_pdf_text(content: bytes):
    with fitz.open(stream=content, filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])
