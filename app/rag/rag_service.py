from app.rag.context_builder import build_context
from app.rag.llm import generate_answer
from app.rag.prompt_builder import build_prompt
from app.rag.retriever import retrieve_chunks


def answer_question(query: str,limit: int = 3) -> dict:
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    points = retrieve_chunks(
        query=query,
        limit=limit,
    )

    context = build_context(points)

    prompt = build_prompt(
        query=query,
        context=context,
    )

    answer = generate_answer(prompt)
    sources=[]
    for point in points:
        payload = point.payload or {}
        sources.append({
            "document_name": payload.get("document_name"),
            "title": payload.get("title"),
            "section_title": payload.get("section_title"),
            "score": point.score,
            "source_urls": payload.get("source_urls", [])
        })


    return dict(answer=answer, sources=sources)