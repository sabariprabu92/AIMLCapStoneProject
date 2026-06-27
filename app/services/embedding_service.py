from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str):
    embedding = embedding_model.encode(text)
    return embedding.tolist()