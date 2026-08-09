from app.core.config import settings
from app.rag.embedding import embed_texts
from app.rag.vector_store import get_qdrant_client

def retrieve_chunks(query: str, limit: int = 3):
    vectors = embed_texts(
        [query],
        batch_size=1,
    )
    query_vector=vectors[0]
    client = get_qdrant_client()

    try:
        result = client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            limit=limit,
            with_payload=True)
        return result.points
    finally:
        client.close()