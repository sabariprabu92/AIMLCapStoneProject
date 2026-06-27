import chromadb
from app.services.embedding_service import generate_embedding

CHROMA_DB_PATH = "vector_db"
COLLECTION_NAME = "enterprise_documents"

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)


def store_chunks_in_vector_db(filename: str, chunks: list):
    if not chunks:
        return {
            "status": "failed",
            "message": "No chunks available to store"
        }

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        chunk_id = f"{filename}_chunk_{chunk['chunk_id']}"

        ids.append(chunk_id)
        documents.append(chunk["text"])
        embeddings.append(generate_embedding(chunk["text"]))
        metadatas.append({
            "filename": filename,
            "chunk_id": chunk["chunk_id"],
            "character_count": chunk["character_count"]
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return {
        "status": "success",
        "message": "Chunks embedded and stored in ChromaDB successfully",
        "stored_chunk_count": len(chunks)
    }


def search_similar_chunks(query: str, top_k: int = 3):
    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results