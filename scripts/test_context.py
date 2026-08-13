from app.rag.context_builder import build_context
from app.rag.retriever import retrieve_chunks


def main() -> None:
    query = (
        "Tôi cần học gì để trở thành "
        "Backend Developer?"
    )

    results = retrieve_chunks(
        query=query,
        limit=3,
    )

    documents = [
        document
        for document, _score in results
    ]

    context = build_context(documents)

    print("QUERY:")
    print(query)

    print("\n" + "=" * 70)
    print("CONTEXT:")
    print("=" * 70)
    print(context)


if __name__ == "__main__":
    main()
