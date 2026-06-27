from app.services.llamaindex_rag_service import generate_answer_from_context


def generate_final_response(question: str, grounded_context: str):
    if not grounded_context:
        return {
            "agent": "response",
            "answer": "I could not find this information in the uploaded document."
        }

    answer = generate_answer_from_context(question, grounded_context)

    return {
        "agent": "response",
        "answer": answer
    }