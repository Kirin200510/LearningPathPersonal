from app.rag.intent_router import classify_intent
from app.rag.retriever import get_retriever


def test_question(question: str):
    print("\n" + "=" * 70)

    print("QUESTION:")
    print(question)

    # 1. Phân loại câu hỏi
    intent = classify_intent(
        question
    )

    print(
        "INTENT:",
        intent
    )

    # 2. Lấy retriever theo intent
    retriever = get_retriever(
        intent=intent,
        k=3,
    )

    # 3. Search Qdrant
    documents = retriever.invoke(
        question
    )

    # 4. In kết quả
    for index, document in enumerate(
        documents,
        start=1,
    ):
        print(
            f"\nRESULT {index}"
        )

        print(
            "DOCUMENT TYPE:",
            document.metadata.get(
                "document_type"
            )
        )

        print(
            "TITLE:",
            document.metadata.get(
                "title"
            )
        )

        print(
            "SOURCE ID:",
            document.metadata.get(
                "source_id"
            )
        )


def main():

    test_question(
        "Có khóa học nào về Power Pages không?"
    )


if __name__ == "__main__":
    main()