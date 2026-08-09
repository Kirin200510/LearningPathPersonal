from app.core.config import settings
from app.rag.knowledge_ingestor import (
    ingest_knowledge_base,
    load_all_chunks,
)


def main() -> None:
    print("=== KIỂM TRA KNOWLEDGE BASE ===")

    chunks = load_all_chunks()

    print(
        f"Tổng số chunk tìm thấy: {len(chunks)}"
    )

    if not chunks:
        print("Không có chunk nào.")
        return

    print("\nChunk đầu tiên:")
    print("Document:", chunks[0].document_name)
    print("Section:", chunks[0].section_title)

    print("\n=== BẮT ĐẦU INGEST ===")
    print(
        "Collection:",
        settings.QDRANT_COLLECTION,
    )

    total_points = ingest_knowledge_base(
        batch_size=4,
    )

    print("\n=== HOÀN THÀNH ===")
    print(
        f"Đã lưu {total_points} points vào Qdrant."
    )


if __name__ == "__main__":
    main()