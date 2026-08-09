from app.core.config import BASE_DIR
from app.rag.document_loader import load_document_chunks
from app.rag.embedding import embed_text


DOCUMENT_PATH = (
    BASE_DIR
    / "knowledge_base"
    / "backend_developer.md"
)


def main():
    chunks = load_document_chunks(DOCUMENT_PATH)

    first_chunk = chunks[0]

    print("Section:", first_chunk.section_title)

    result = embed_text(first_chunk.text)

    dense = result["dense"]

    print("Embedding thành công.")
    print("Kích thước vector:", len(dense))
    print("5 số đầu:", dense[:5])


if __name__ == "__main__":
    main()