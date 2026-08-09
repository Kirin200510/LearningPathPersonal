from app.rag.context_builder import build_context
from app.rag.llm import generate_answer
from app.rag.prompt_builder import build_prompt
from app.rag.retriever import retrieve_chunks


def main() -> None:
    query = "Tôi thích phân tích dữ liệu và tạo báo cáo, nghề nào phù hợp?"

    points = retrieve_chunks(
        query=query,
        limit=3,
    )

    context = build_context(points)

    prompt = build_prompt(
        query=query,
        context=context,
    )

    answer = generate_answer(prompt)

    print("QUESTION:")
    print(query)

    print("\nCONTEXT:")
    print(context)

    print("\nANSWER:")
    print(answer)


if __name__ == "__main__":
    main()