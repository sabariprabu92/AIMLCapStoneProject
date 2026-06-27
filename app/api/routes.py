from fastapi import APIRouter, UploadFile, File
from app.services.document_service import process_uploaded_document
from app.services.question_service import process_question
from app.schemas.question_schema import QuestionRequest
from app.core.chunk_store import chunk_store

router = APIRouter()


@router.get("/health-check")
def health_check():
    return {
        "status": "success",
        "message": "API is running successfully"
    }


@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    result = await process_uploaded_document(file)
    return result


@router.post("/ask-questions")
def ask_questions(request: QuestionRequest):
    result = process_question(request.question)
    return result

@router.get("/chunks")
def get_chunks():
    return {
        "status": "success",
        "filename": chunk_store["filename"],
        "chunk_count": len(chunk_store["chunks"]),
        "chunks": chunk_store["chunks"]
    }