from app.rag.catalog_loader import load_catalog_programs


def main():
    programs = load_catalog_programs()

    print(
        "Total programs:",
        len(programs),
    )

    if not programs:
        print("Catalog is empty.")
        return

    first_program = programs[0]

    print(
        "\n" + "=" * 70
    )

    print(
        "Source ID:",
        first_program.get("source_id"),
    )
    print(
        "Title:",
        first_program.get("title"),
    )
    print(
        "Description:",
        first_program.get("description"),
    )
    print(
        "Levels:",
        first_program.get("levels"),
    )
    print(
        "Roles:",
        first_program.get("roles"),
    )
    print(
        "Topics:",
        first_program.get("topics"),
    )
    print(
        "Technologies:",
        first_program.get("technologies"),
    )
    print(
        "Learning items:",
        len(first_program.get("learning_items", [])),
    )


if __name__ == "__main__":
    main()
