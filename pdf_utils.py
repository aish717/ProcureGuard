from io import BytesIO
from pypdf import PdfReader

def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from a text-based PDF."""
    reader = PdfReader(BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages).strip()
