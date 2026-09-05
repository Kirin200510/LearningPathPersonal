from app.rag.intent_router import (
    classify_intent,
)



def main():

    questions = [
        "Tôi muốn trở thành Backend Developer thì nên học lộ trình nào?"
    ]

    for question in questions:

        intent = classify_intent(
            question
        )

        print(
            "QUESTION:",
            question
        )

        print(
            "INTENT:",
            intent
        )

        print(
            "=" * 70
        )


if __name__ == "__main__":
    main()