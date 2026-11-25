
from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> list:
    """
    Extract text from a PDF and preserve page numbers.
    """

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError("PDF file not found")

    reader = PdfReader(str(pdf_path))

    if reader.is_encrypted:
        raise ValueError("Password-protected PDFs are not supported")

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        extracted_pages.append({
            "page_number": page_number,
            "text": text.strip()
        })

    if not any(page["text"] for page in extracted_pages):
        raise ValueError("No extractable text found in PDF")

    return extracted_pages
