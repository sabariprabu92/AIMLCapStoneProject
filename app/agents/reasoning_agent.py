def reason_over_chunks(question: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return {
            "agent": "reasoning",
            "reasoning_summary": "No relevant chunks were found.",
            "can_answer": False,
            "grounded_context": ""
        }

    grounded_context = ""

    for index, chunk in enumerate(retrieved_chunks, start=1):
        grounded_context += f"\nChunk {index}:\n{chunk['text']}\n"

    return {
        "agent": "reasoning",
        "reasoning_summary": "Relevant chunks were found and prepared as grounded context.",
        "can_answer": True,
        "grounded_context": grounded_context
    }