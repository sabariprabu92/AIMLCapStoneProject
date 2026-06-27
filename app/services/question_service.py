from fastapi import HTTPException
from app.core.document_store import document_store
from app.agents.agent_orchestrator import run_agentic_workflow
from app.core.logger import logger


def process_question(question: str):
    try:
        if not question or not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        if len(question) > 1000:
            raise HTTPException(status_code=400, detail="Question is too long")

        if not document_store["content"]:
            raise HTTPException(
                status_code=400,
                detail="No document uploaded yet. Please upload a document first."
            )

        logger.info(f"Question received: {question}")

        agent_result = run_agentic_workflow(question)

        logger.info("Question processed successfully")

        return {
            "status": "success",
            "question": question,
            "document_used": document_store["filename"],
            "agentic_workflow": agent_result,
            "answer": agent_result["final_answer"]
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Unexpected error while processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing question"
        )