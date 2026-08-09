from qdrant_client.models import Distance, VectorParams

from app.rag.vector_store import get_qdrant_client


COLLECTION_NAME = "rag_test"


def main() -> None:
    client = get_qdrant_client()

    try:
        if not client.collection_exists(COLLECTION_NAME):
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=4,
                    distance=Distance.COSINE,
                ),
            )
            print(f"Đã tạo collection: {COLLECTION_NAME}")
        else:
            print(f"Collection đã tồn tại: {COLLECTION_NAME}")

        collections = client.get_collections()

        print("Danh sách collection:")

        for collection in collections.collections:
            print(f"- {collection.name}")

    finally:
        client.close()


if __name__ == "__main__":
    main()