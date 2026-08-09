from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.core.config import BASE_DIR, settings

def get_qdrant_client() -> QdrantClient:
    storage_path = Path(settings.QDRANT_PATH)

    if not storage_path.is_absolute():
        storage_path = BASE_DIR / storage_path

    storage_path.mkdir(parents=True, exist_ok=True)
    #gắn đối tượng kết nối có đường dẫn lưu trữ của qdrant storage(vector db)
    return QdrantClient(path=str(storage_path))

def create_collection(client: QdrantClient):
    collection_name = settings.QDRANT_COLLECTION
    if client.collection_exists(collection_name):
        return

    client.create_collection(
        collection_name=collection_name,
        # 1024 dimension(1024 tọa độ)
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE,
        ),
    )