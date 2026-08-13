from langchain_core.documents import Document

from app.rag.vector_store import get_vector_store


def retrieve_chunks(
    query: str,
    limit: int = 3,
) -> list[tuple[Document, float]]:
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    vector_store = get_vector_store()

    return vector_store.similarity_search_with_score(
        query=query,
        k=limit,
    )


def get_retriever(limit: int = 3):
    """Return a standard LangChain Retriever for later chains/agents."""

    return get_vector_store().as_retriever(
        search_type="similarity",
        search_kwargs={"k": limit},
    )
