from pathlib import Path
from functools import lru_cache
from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from app.core.config import BASE_DIR,settings
from app.rag.embeddings import get_embeddings

@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    storage_path=Path(settings.QDRANT_PATH)
    if not storage_path.is_absolute():
        storage_path = (BASE_DIR/ storage_path)

    storage_path.mkdir(parents=True,exist_ok=True)
    return QdrantClient(path=str(storage_path))

def create_collection(client: QdrantClient) -> None:
    collection_name=settings.QDRANT_COLLECTION
    if client.collection_exists(collection_name):
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1024,distance=Distance.COSINE))

@lru_cache(maxsize=1)
def get_vector_store() -> QdrantVectorStore:
    client = get_qdrant_client()
    create_collection(client)

    return QdrantVectorStore(
        client=client,
        collection_name=settings.QDRANT_COLLECTION,
        embedding=get_embeddings(),
        retrieval_mode=RetrievalMode.DENSE
    )


