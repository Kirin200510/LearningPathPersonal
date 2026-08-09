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

    chunks = load_document_chunks(DOCUMENT_PATH)

    print(f"Document: {DOCUMENT_PATH.name}")
    print(f"Tổng số chunk: {len(chunks)}")

    for chunk in chunks:
        print("\n" + "=" * 70)
        print(f"Chunk index: {chunk.chunk_index}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Tiêu đề nghề: {chunk.title}")
        print(f"Section: {chunk.section_title}")
        print(f"Số ký tự: {len(chunk.text)}")

        print("\nNội dung:")
        print(chunk.text[:500])

        if len(chunk.text) > 500:
            print("...")


if __name__ == "__main__":
    main()