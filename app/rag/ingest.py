import uuid
from langchain_core.documents import Document
from sqlalchemy.testing.suite.test_reflection import metadata
from torch._dynamo.polyfills import os

from app.core.config import BASE_DIR,settings
from app.rag.document_loader import read_markdown_file
from app.rag.text_splitter import split_document
from app.rag.catalog_splitter import load_catalog_chunks
from app.rag.vector_store import create_collection,get_qdrant_client, get_vector_store

KNOWLEDGE_BASE_DIR = (
    BASE_DIR/ "data" / "knowledge_base"
)

def load_career_chunks()->list[Document]:
    all_chunks = []
    markdown_files=sorted(KNOWLEDGE_BASE_DIR.glob("*.md"))

    for markdown_file in markdown_files:
        document = read_markdown_file(markdown_file)
        chunks=split_document(document)
        all_chunks.extend(chunks)

    return all_chunks

def load_all_rag_chunks()->list[Document]:
    career_chunks = load_career_chunks()
    catalog_chunks = load_catalog_chunks(item_per_chunk=3)
    all_chunks = career_chunks + catalog_chunks
    return all_chunks

def create_chunk_ids(chunks: list[Document]) -> list[str]:
    ids: list[str] = []
    for chunk in chunks:
        metadata=chunk.metadata
        document_type = metadata.get("document_type","unknown")
        document_id = metadata.get("source_id") or metadata.get('id') or metadata.get('document_name')
        chunk_index=metadata.get('chunk_index')
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                (
                    f"{document_type}"
                    f"{document_id}:"
                    f"{chunk_index}"
                )
            )
        )
        ids.append(point_id)
    return ids

def ingest_all_rag_data()->int:
    chunks = load_all_rag_chunks()
    ids = create_chunk_ids(chunks)

    client = get_qdrant_client()

    if client.collection_exists(settings.QDRANT_COLLECTION):
        client.delete_collection(settings.QDRANT_COLLECTION)

    create_collection(client)

    vector_store = get_vector_store()
    vector_store.add_documents(documents=chunks, ids=ids)

    return len(chunks)




