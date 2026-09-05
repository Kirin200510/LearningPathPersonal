from app.rag.chain import get_rag_chain


def main():
    chain = get_rag_chain()

    result = chain.invoke(
        {
            "question": (
                "Tôi muốn học lộ trình "
                "để trở thành Backend Developer"
            )
        },
        config={
            "configurable": {
                "session_id": "test-program-001"
            }
        },
    )

    print("RESULT:")
    print(result)

    print("\nANSWER:")
    print(result["answer"])

    print("\nPROGRAM ID:")
    print(result["selected_program_id"])


if __name__ == "__main__":
    main()