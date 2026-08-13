from langchain_core.output_parsers import StrOutputParser

from app.rag.context_builder import build_context
from app.rag.llm import get_llm
from app.rag.prompt_builder import get_rag_prompt
from app.rag.retriever import retrieve_chunks


def answer_question(
    query: str,
    limit: int = 3,
) -> dict:
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    results = retrieve_chunks(
        query=query,
        limit=limit,
    )

    documents = [
        document
        for document, _score in results
    ]

    context = build_context(documents)

    chain = (
        get_rag_prompt()
        | get_llm()
        | StrOutputParser()
    )

    answer = chain.invoke(
        {
            "context": context,
            "question": query,
        }
    )

    sources = []

    for document, score in results:
        metadata = document.metadata

        sources.append(
            {
                "document_name": metadata.get("document_name"),
                "title": metadata.get("title"),
                "section_title": metadata.get("section_title"),
                "score": score,
                "source_urls": metadata.get("source_urls", []),
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }
