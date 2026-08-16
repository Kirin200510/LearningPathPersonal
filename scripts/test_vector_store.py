from app.core.config import settings

from app.rag.vector_store import (
    get_qdrant_client,
    get_vector_store,
)


def main():

    client = get_qdrant_client()

    vector_store = get_vector_store()

    print(
        "Collection:",
        settings.QDRANT_COLLECTION,
    )

    print(
        "Collection exists:",
        client.collection_exists(
            settings.QDRANT_COLLECTION
        ),
    )

    print(
        "Vector store type:",
        type(vector_store),
    )


if __name__ == "__main__":
    main()