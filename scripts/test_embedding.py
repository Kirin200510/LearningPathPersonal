from app.rag.embedding import get_embeddings


def main() -> None:
    embeddings = get_embeddings()

    vector = embeddings.embed_query(
        "Tôi muốn trở thành Backend Developer."
    )

    print("Embedding thành công.")
    print("Kích thước vector:", len(vector))
    print("5 số đầu:", vector[:5])


if __name__ == "__main__":
    main()
