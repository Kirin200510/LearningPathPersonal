from app.rag.retriever import retrieve_chunks


def main():
    query = "Tôi cần học gì để trở thành Backend Developer?"

    results = retrieve_chunks(
        query=query,
        limit=5,
    )

    print("QUERY:")
    print(query)

    for index, point in enumerate(results, start=1):
        print("\n" + "=" * 70)

        print(f"Kết quả #{index}")
        print(f"Score: {point.score}")

        payload = point.payload or {}

        print(
            "Document:",
            payload.get("document_name"),
        )

        print(
            "Title:",
            payload.get("title"),
        )

        print(
            "Section:",
            payload.get("section_title"),
        )

        print("\nText:")
        print(payload.get("text"))


if __name__ == "__main__":
    main()