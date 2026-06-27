from app.core.chunk_store import chunk_store


def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 100):
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end]

        last_period = chunk.rfind(".")
        last_newline = chunk.rfind("\n")

        split_point = max(last_period, last_newline)

        if split_point > 100:
            end = start + split_point + 1
            chunk = text[start:end]

        cleaned_chunk = chunk.strip()

        if cleaned_chunk:
            chunks.append({
                "chunk_id": len(chunks) + 1,
                "text": cleaned_chunk,
                "character_count": len(cleaned_chunk)
            })

        start = end - overlap

        if start < 0:
            start = 0

        if start >= text_length:
            break

    return chunks


def create_and_store_chunks(filename: str, text: str):
    chunks = split_text_into_chunks(text)

    chunk_store["filename"] = filename
    chunk_store["chunks"] = chunks

    return chunks