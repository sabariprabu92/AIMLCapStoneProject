import os
from fastapi import UploadFile, HTTPException
from app.utils.file_utils import save_uploaded_file
from app.utils.text_cleaner import clean_text
from app.utils.document_reader import extract_text_from_file
from app.core.document_store import document_store
from app.core.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB
from app.core.logger import logger
from app.services.llamaindex_rag_service import build_llamaindex_from_text


async def process_uploaded_document(file: UploadFile):
    try:
        filename = file.filename

        if not filename:
            raise HTTPException(status_code=400, detail="No file uploaded")

        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension not in ALLOWED_EXTENSIONS:
            logger.warning(f"Unsupported file upload attempt: {file_extension}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_extension}. Allowed types: {ALLOWED_EXTENSIONS}"
            )

        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > MAX_FILE_SIZE_BYTES:
            logger.warning(f"File size exceeded: {filename}, size={file_size}")
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB} MB"
            )

        file_path = await save_uploaded_file(file)

        extracted_text = extract_text_from_file(file_path, file_extension)
        cleaned_text = clean_text(extracted_text)

        if not cleaned_text:
            logger.warning(f"No readable text found in file: {filename}")
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the uploaded document"
            )

        document_store["filename"] = filename
        document_store["file_type"] = file_extension
        document_store["content"] = cleaned_text
        document_store["character_count"] = len(cleaned_text)

        llamaindex_result = build_llamaindex_from_text(filename, cleaned_text)

        logger.info(f"Document processed successfully: {filename}")

        return {
            "status": "success",
            "message": "Document uploaded, processed, indexed successfully",
            "filename": filename,
            "file_type": file_extension,
            "file_size_bytes": file_size,
            "character_count": len(cleaned_text),
            "llamaindex_result": llamaindex_result,
            "preview": cleaned_text[:500]
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Unexpected error while processing document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing document"
        )