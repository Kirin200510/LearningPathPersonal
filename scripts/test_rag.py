from app.rag.chain import get_rag_chain


def main():
    rag_chain = get_rag_chain()

    question = (
        "Tôi cần học gì để "
        "trở thành Backend Developer?"
    )

    answer = rag_chain.invoke(
        question
    )

    print("QUESTION:")
    print(question)

    print(
        "\n" + "=" * 70
    )

    print("ANSWER:")
    print(answer)


if __name__ == "__main__":
    main()