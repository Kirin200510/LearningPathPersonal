from app.rag.llm import get_llm


def main():

    llm = get_llm()

    response = llm.invoke(
        "Backend Developer là gì? "
        "Trả lời trong 2 câu."
    )

    print("TYPE:")
    print(type(response))

    print("\nCONTENT:")
    print(response.content)


if __name__ == "__main__":
    main()