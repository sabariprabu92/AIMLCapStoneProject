from app.services.llamaindex_rag_service import retrieve_source_chunks


def retrieve_information(question: str):
    chunks = retrieve_source_chunks(question)

    return {
        "agent": "retriever",
        "task": "Retrieve relevant document chunks",
        "retrieved_chunks": chunks
    }