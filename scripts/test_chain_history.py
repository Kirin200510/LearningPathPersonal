from app.rag.chain import get_rag_chain


def main():
    chain = get_rag_chain()

    session_id = "test-001"

    # Lượt chat 1
    answer1 = chain.invoke(
        {
            "question": "Tôi muốn học một lộ trình"
        },
        config={
            "configurable": {
                "session_id": session_id
            }
        },
    )

    print("USER:")
    print("Tôi muốn học một lộ trình")

    print("\nAI:")
    print(answer1)

    print("\n" + "=" * 70)

    # Lượt chat 2
    answer2 = chain.invoke(
        {
            "question": "Data Scientist"
        },
        config={
            "configurable": {
                "session_id": session_id
            }
        },
    )

    print("USER:")
    print("Data Scientist")

    print("\nAI:")
    print(answer2)


if __name__ == "__main__":
    main()