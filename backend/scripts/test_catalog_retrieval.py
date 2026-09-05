from app.rag.retriever import (
    retrieve_catalog_programs,
)


def main():
    query = "Tôi muốn học một lộ trình về Backend"

    programs = retrieve_catalog_programs(
        query=query,
        k=5,
    )

    print(
        "TOTAL PROGRAMS:",
        len(programs)
    )

    for index, program in enumerate(
        programs,
        start=1,
    ):
        print(
            "\n" + "=" * 70
        )

        print(
            f"PROGRAM {index}"
        )

        print(
            "TITLE:",
            program.get("title")
        )

        print(
            "SOURCE ID:",
            program.get("source_id")
        )

        learning_items = program.get(
            "learning_items",
            []
        )

        print(
            "TOTAL LEARNING ITEMS:",
            len(learning_items)
        )

        for item in learning_items:
            print(
                item.get("order"),
                "-",
                item.get("title"),
            )


if __name__ == "__main__":
    main()