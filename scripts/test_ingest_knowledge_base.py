from app.core.config import settings
from app.rag.knowledge_ingestor import (
    ingest_knowledge_base,
    load_all_documents,
)


def main() -> None:
    print("=== KIỂM TRA KNOWLEDGE BASE ===")

    documents = load_all_documents()

    print(
        f"Tổng số chunk tìm thấy: {len(documents)}"
    )

    if not documents:
        print("Không có chunk nào.")
        return

    metadata = documents[0].metadata

    print("\nChunk đầu tiên:")
    print("Document:", metadata.get("document_name"))
    print("Section:", metadata.get("section_title"))

    print("\n=== BẮT ĐẦU INGEST ===")
    print(
        "Collection:",
        settings.QDRANT_COLLECTION,
    )

    total_points = ingest_knowledge_base()

    print("\n=== HOÀN THÀNH ===")
    print(
        f"Đã lưu {total_points} documents vào Qdrant qua LangChain."
    )


if __name__ == "__main__":
    main()
