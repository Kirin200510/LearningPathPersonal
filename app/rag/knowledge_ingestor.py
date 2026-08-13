import uuid

from langchain_core.documents import Document

from app.core.config import BASE_DIR
from app.rag.document_loader import load_document_chunks
from app.rag.vector_store import get_vector_store


KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"


def load_all_documents() -> list[Document]:
    all_documents: list[Document] = []

    markdown_files = sorted(
        KNOWLEDGE_BASE_DIR.glob("*.md")
    )

    for file_path in markdown_files:
        documents = load_document_chunks(file_path)
        all_documents.extend(documents)

    return all_documents


# Alias để các script cũ chưa cần đổi tên ngay.
def load_all_chunks() -> list[Document]:
    return load_all_documents()


def create_document_ids(
    documents: list[Document],
) -> list[str]:
    ids: list[str] = []

    for document in documents:
        document_id = document.metadata["document_id"]
        chunk_index = document.metadata["chunk_index"]

        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{document_id}:{chunk_index}",
            )
        )

        ids.append(point_id)

    return ids


def ingest_knowledge_base() -> int:
    documents = load_all_documents()

    if not documents:
        raise ValueError("Knowledge base does not have documents.")

    ids = create_document_ids(documents)
    vector_store = get_vector_store()

    vector_store.add_documents(
        documents=documents,
        ids=ids,
    )

    return len(documents)
