from fastapi import HTTPException
from app.core.document_store import document_store
from app.services.retrieval_service import retrieve_relevant_chunks


def process_question(question: str):
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if not document_store["content"]:
        raise HTTPException(
            status_code=400,
            detail="No document uploaded yet. Please upload a document first."
        )

    retrieval_result = retrieve_relevant_chunks(question, top_k=3)

    return {
        "status": "success",
        "question": question,
        "document_used": document_store["filename"],
        "message": "Relevant document chunks retrieved successfully using similarity search.",
        "retrieval_result": retrieval_result
    }