from app.rag.retriever import retrieve_chunks


def main() -> None:
    query = "Tôi cần học gì để trở thành Backend Developer?"

    results = retrieve_chunks(
        query=query,
        limit=5,
    )

    print("QUERY:")
    print(query)

    for index, (document, score) in enumerate(results, start=1):
        print("\n" + "=" * 70)
        print(f"Kết quả #{index}")
        print(f"Score: {score}")

        metadata = document.metadata

        print("Document:", metadata.get("document_name"))
        print("Title:", metadata.get("title"))
        print("Section:", metadata.get("section_title"))

        print("\nText:")
        print(document.page_content)


if __name__ == "__main__":
    main()
