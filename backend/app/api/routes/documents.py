
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.app.services.pdf_processor import extract_text_from_pdf
from backend.app.services.text_splitter import split_text_into_chunks
from backend.app.services.vector_store import (
    create_vector_store,
    save_vector_store
)

router = APIRouter(prefix="/api/documents", tags=["Documents"])

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty"
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds 10 MB limit"
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    document_id = str(uuid4())
    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    try:
        # Step 1: Save uploaded PDF
        file_path.write_bytes(content)

        # Step 2: Extract PDF text
        pages = extract_text_from_pdf(str(file_path))

        # Step 3: Split text into chunks
        chunks = split_text_into_chunks(pages)

        if not chunks:
            raise ValueError("No text chunks generated from PDF")

        # Step 4: Generate embeddings and create FAISS index
        vector_store = create_vector_store(chunks)

        # Step 5: Save FAISS index
        save_vector_store(vector_store, document_id)

        return {
            "document_id": document_id,
            "filename": file.filename,
            "total_pages": len(pages),
            "total_chunks": len(chunks),
            "status": "processed",
            "message": "PDF uploaded and indexed successfully"
        }

    except Exception as error:
        file_path.unlink(missing_ok=True)

        if isinstance(error, ValueError):
            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

        raise HTTPException(
            status_code=422,
            detail="Unable to process and index PDF"
        ) from error

    finally:
        await file.close()
