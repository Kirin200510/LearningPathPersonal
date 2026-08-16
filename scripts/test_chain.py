from app.rag.chain import get_rag_chain


def test_question(
    question: str,
):
    print(
        "\n" + "=" * 70
    )

    print("QUESTION:")
    print(question)

    rag_chain = get_rag_chain()

    answer = rag_chain.invoke(
        question
    )

    print("\nANSWER:")
    print(answer)


def main():

    test_question(
        (
            "Tôi muốn học lộ trình dành cho Data Scientist"
        )
    )


if __name__ == "__main__":
    main()