from app.rag.context_builder import build_context
from app.rag.prompt_builder import build_prompt
from app.rag.retriever import retrieve_chunks


def main():
    query = "Tôi cần học gì để trở thành Backend Developer?"

    points = retrieve_chunks(
        query=query,
        limit=3,
    )

    context = build_context(points)

    prompt = build_prompt(
        query=query,
        context=context,
    )

    print(prompt)


if __name__ == "__main__":
    main()