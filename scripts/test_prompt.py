from app.rag.context_builder import build_context
from app.rag.prompt_builder import get_rag_prompt
from app.rag.retriever import retrieve_chunks


def main() -> None:
    query = "Tôi cần học gì để trở thành Backend Developer?"

    results = retrieve_chunks(
        query=query,
        limit=3,
    )

    documents = [
        document
        for document, _score in results
    ]

    context = build_context(documents)

    prompt_value = get_rag_prompt().invoke(
        {
            "context": context,
            "question": query,
        }
    )

    print(prompt_value.to_string())


if __name__ == "__main__":
    main()
