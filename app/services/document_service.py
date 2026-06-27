import os
from app.services.chunking_service import create_and_store_chunks
from fastapi import UploadFile, HTTPException
from app.utils.file_utils import save_uploaded_file
from app.utils.text_cleaner import clean_text
from app.utils.document_reader import extract_text_from_file
from app.core.document_store import document_store
from app.services.vector_store_service import store_chunks_in_vector_db

ALLOWED_EXTENSIONS = [".pdf", ".txt", ".csv", ".xlsx", ".xls", ".json", ".yaml", ".yml"]


async def process_uploaded_document(file: UploadFile):
    filename = file.filename

    if not filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_extension}"
        )

    file_path = await save_uploaded_file(file)

    extracted_text = extract_text_from_file(file_path, file_extension)

    cleaned_text = clean_text(extracted_text)

    if not cleaned_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the uploaded document"
        )

    document_store["filename"] = filename
    document_store["file_type"] = file_extension
    document_store["content"] = cleaned_text
    document_store["character_count"] = len(cleaned_text)
    chunks = create_and_store_chunks(filename, cleaned_text)
    vector_result = store_chunks_in_vector_db(filename, chunks)

    return {
    "status": "success",
    "message": "Document uploaded, processed, chunked, embedded, and stored successfully",
    "filename": filename,
    "file_type": file_extension,
    "character_count": len(cleaned_text),
    "chunk_count": len(chunks),
    "vector_store_status": vector_result,
    "preview": cleaned_text[:500]
}