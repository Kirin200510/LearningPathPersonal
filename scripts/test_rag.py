from app.rag.rag_service import answer_question


def main() -> None:
    query = "Tôi thích phân tích dữ liệu và tạo báo cáo, nghề nào phù hợp?"

    result = answer_question(
        query=query,
        limit=3,
    )

    print("QUESTION:")
    print(query)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(source)


if __name__ == "__main__":
    main()
