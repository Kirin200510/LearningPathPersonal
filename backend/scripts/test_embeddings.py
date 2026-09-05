from app.rag.embeddings import (
    get_embeddings,
)


def main():
    embeddings = get_embeddings()

    text = (
        "Backend Developer cần học "
        "Python, HTTP và Database."
    )

    vector = embeddings.embed_query(
        text
    )

    print(
        "Vector type:",
        type(vector),
    )

    print(
        "Vector dimension:",
        len(vector),
    )

    print(
        "5 giá trị đầu:",
        vector[:5],
    )


if __name__ == "__main__":
    main()