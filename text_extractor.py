# text_extractor.py
from typing import Tuple
from io import BytesIO

from fastapi import UploadFile
from pypdf import PdfReader


async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Read an uploaded PDF (UploadFile) and return plain text.
    """
    pdf_bytes = await file.read()
    pdf_stream = BytesIO(pdf_bytes)

    reader = PdfReader(pdf_stream)
    text_chunks = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_chunks.append(page_text)

    full_text = "\n".join(text_chunks).strip()
    return full_text


async def parse_resume(resume_file: UploadFile) -> Tuple[str, int, str]:
    """
    High-level helper:
    - Extract text.
    - Return full text, its length, and a preview.
    """
    full_text = await extract_text_from_pdf(resume_file)
    text_length = len(full_text)
    preview = full_text[:]

    return full_text, text_length, preview