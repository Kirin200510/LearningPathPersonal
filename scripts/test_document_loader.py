from app.core.config import BASE_DIR
from app.rag.document_loader import (
    read_markdown_file
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

    print("TYPE:")
    print(type(document))

    print("\nMETADATA:")
    print(document.metadata)

    print("\nCONTENT:")
    print(
        document.page_content[:500]
    )


if __name__ == "__main__":
    main()