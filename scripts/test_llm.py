from app.rag.llm import generate_answer


def main() -> None:
    prompt = """
Bạn là trợ lý học tập.

Hãy trả lời ngắn gọn:
Backend Developer là gì?
""".strip()

    answer = generate_answer(prompt)

    print("ANSWER:")
    print(answer)


if __name__ == "__main__":
    main()