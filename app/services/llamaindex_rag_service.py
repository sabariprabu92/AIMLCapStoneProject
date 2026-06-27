import chromadb

from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

CHROMA_DB_PATH = "vector_db"
COLLECTION_NAME = "enterprise_documents_llamaindex"

Settings.llm = Ollama(
    model="llama3.2:3b",
    request_timeout=180
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


def build_llamaindex_from_text(filename: str, text: str):
    splitter = SentenceSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    document = Document(
        text=text,
        metadata={"filename": filename}
    )

    nodes = splitter.get_nodes_from_documents([document])

    VectorStoreIndex(
        nodes,
        storage_context=storage_context
    )

    return {
        "status": "success",
        "message": "LlamaIndex index created using free local embeddings and ChromaDB",
        "filename": filename,
        "chunk_count": len(nodes)
    }


def ask_llamaindex_question(question: str):
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store
    )

    query_engine = index.as_query_engine(
        similarity_top_k=3,
        response_mode="compact"
    )

    prompt = f"""
Answer the question using only the uploaded document context.

If the answer is not available in the uploaded document context, say:
"I could not find this information in the uploaded document."

Do not use outside knowledge.

Question:
{question}
"""

    response = query_engine.query(prompt)

    source_chunks = []

    for source_node in response.source_nodes:
        source_chunks.append({
            "text": source_node.node.get_content(),
            "score": source_node.score,
            "metadata": source_node.node.metadata
        })

    return {
        "answer": str(response),
        "source_chunks": source_chunks
    }

def retrieve_source_chunks(question: str):
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store
    )

    retriever = index.as_retriever(
        similarity_top_k=3
    )

    nodes = retriever.retrieve(question)

    source_chunks = []

    for node in nodes:
        source_chunks.append({
            "text": node.node.get_content(),
            "score": node.score,
            "metadata": node.node.metadata
        })

    return source_chunks

def generate_answer_from_context(question: str, grounded_context: str):
    prompt = f"""
You are an enterprise document question-answering assistant.

Answer the question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. If the answer is not present in the context, say:
   "I could not find this information in the uploaded document."
3. Keep the response clear and professional.
4. Group the answer logically if needed.

Context:
{grounded_context}

Question:
{question}

Answer:
"""

    response = Settings.llm.complete(prompt)

    return str(response)