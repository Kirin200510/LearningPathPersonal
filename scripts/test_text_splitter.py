from app.core.config import BASE_DIR

from app.rag.document_loader import (
    read_markdown_file,
)

from app.rag.text_splitter import (
    split_document,
)


DOCUMENT_PATH = (
    BASE_DIR
    / "knowledge_base"
    / "backend_developer.md"
)


def main():

    document = read_markdown_file(
        DOCUMENT_PATH
    )

    chunks = split_document(
        document
    )

    print(
        "Tổng chunks:",
        len(chunks),
    )

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):
        print(
            "\n" + "=" * 70
        )

        print(
            f"CHUNK {index}"
        )

        print(
            "\nMETADATA:"
        )

        print(
            chunk.metadata
        )

        print(
            "\nCONTENT:"
        )

        print(
            chunk.page_content[:500]
        )


if __name__ == "__main__":
    main()