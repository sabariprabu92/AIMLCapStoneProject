from app.services.vector_store_service import search_similar_chunks


def retrieve_relevant_chunks(query: str, top_k: int = 3):
    results = search_similar_chunks(query, top_k)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    relevant_chunks = []

    for index, document in enumerate(documents):
        relevant_chunks.append({
            "rank": index + 1,
            "content": document,
            "metadata": metadatas[index],
            "distance": distances[index]
        })

    return {
        "query": query,
        "top_k": top_k,
        "retrieved_chunk_count": len(relevant_chunks),
        "relevant_chunks": relevant_chunks
    }