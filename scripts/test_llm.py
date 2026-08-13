from app.rag.llm import get_llm


def main() -> None:
    response = get_llm().invoke(
        "Backend Developer là gì? Trả lời ngắn gọn."
    )

    print("ANSWER:")
    print(response.content)


if __name__ == "__main__":
    main()
