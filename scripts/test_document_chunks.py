from app.core.config import BASE_DIR
from app.rag.document_loader import load_document_chunks


DOCUMENT_PATH = (
    BASE_DIR
    / "knowledge_base"
    / "backend_developer.md"
)


def main() -> None:
    if not DOCUMENT_PATH.exists():
        print(
            f"Không tìm thấy document tại:\n"
            f"{DOCUMENT_PATH}"
        )
        return

    documents = load_document_chunks(DOCUMENT_PATH)

    print(f"Document: {DOCUMENT_PATH.name}")
    print(f"Tổng số chunk: {len(documents)}")

    for document in documents:
        metadata = document.metadata

        print("\n" + "=" * 70)
        print(f"Chunk index: {metadata.get('chunk_index')}")
        print(f"Document ID: {metadata.get('document_id')}")
        print(f"Tiêu đề nghề: {metadata.get('title')}")
        print(f"Section: {metadata.get('section_title')}")
        print(f"Số ký tự: {len(document.page_content)}")

        print("\nNội dung:")
        print(document.page_content[:500])

        if len(document.page_content) > 500:
            print("...")


if __name__ == "__main__":
    main()
