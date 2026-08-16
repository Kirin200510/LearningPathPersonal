from app.rag.catalog_loader import (
    load_catalog_documents,
)


def main():

    documents = (
        load_catalog_documents()
    )

    print(
        "Total documents:",
        len(documents)
    )

    print(
        "\n" + "=" * 70
    )

    print(
        documents[0].page_content
    )

    print(
        "\n" + "=" * 70
    )

    print(
        documents[0].metadata
    )


if __name__ == "__main__":
    main()