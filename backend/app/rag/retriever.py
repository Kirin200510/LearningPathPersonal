from langchain_core.vectorstores import VectorStoreRetriever

from app.rag.catalog_parent import get_program_by_source_id
from app.rag.vector_store import get_vector_store
from qdrant_client import models

def get_document_type(intent:str) -> str:
    if intent == "CAREER":
        return "career_guidance"
    elif intent == "LEARNING":
        return "learning_program_chunk"

def get_retriever(intent:str,k: int = 3) -> VectorStoreRetriever:
    document_type = get_document_type(intent)
    filter_type=models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.document_type",
                match=models.MatchValue(value=document_type)
            )
    ])

    vector_store = get_vector_store()
    retriever=vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs={
            "k": k,
            "filter": filter_type,
        }
    )
    return retriever

def retrieve_catalog_programs(query: str,k: int = 5) -> list[dict]:
    query = query.strip()
    retriever = get_retriever(intent="LEARNING",k=k)
    child_chunks= retriever.invoke(query)

    programs=[]
    seen_programs=set()

    for chunk in child_chunks:
        source_id=chunk.metadata.get("source_id")
        if not source_id:
            continue
        if source_id in seen_programs:
            continue

        program=get_program_by_source_id(source_id)
        if program is None:
            continue
        programs.append(program)
        seen_programs.add(source_id)

    return programs