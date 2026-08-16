from app.rag.catalog_loader import (
    load_catalog_programs,
)
from app.rag.catalog_splitter import (
    load_catalog_chunks,
    split_program,
)


def main():
    # Test toàn bộ catalog
    all_chunks = load_catalog_chunks(
        item_per_chunk=3
    )

    print(
        "TOTAL CHUNKS:",
        len(all_chunks)
    )

    print(
        "\n" + "=" * 70
    )

    # Tìm một program có nhiều hơn 3 learning items
    programs = load_catalog_programs()

    target_program = None

    for program in programs:
        learning_items = program.get(
            "learning_items",
            []
        )

        if len(learning_items) > 3:
            target_program = program
            break

    if target_program is None:
        print(
            "Không tìm thấy program "
            "có nhiều hơn 3 learning items."
        )
        return

    print("PROGRAM:")
    print(
        target_program.get("title")
    )

    print(
        "TOTAL LEARNING ITEMS:",
        len(
            target_program.get(
                "learning_items",
                []
            )
        )
    )

    # Split riêng program này
    program_chunks = split_program(
        program=target_program,
        item_per_chunk=3,
    )

    print(
        "TOTAL PROGRAM CHUNKS:",
        len(program_chunks)
    )

    # In từng chunk
    for chunk in program_chunks:
        print(
            "\n" + "=" * 70
        )

        print(
            "CHUNK INDEX:",
            chunk.metadata.get(
                "chunk_index"
            )
        )

        print(
            "SOURCE ID:",
            chunk.metadata.get(
                "source_id"
            )
        )

        print(
            "ITEM RANGE:",
            chunk.metadata.get(
                "item_start"
            ),
            "→",
            chunk.metadata.get(
                "item_end"
            ),
        )

        print("\nCONTENT:")
        print(
            chunk.page_content
        )


if __name__ == "__main__":
    main()