import uuid

from qdrant_client.models import PointStruct
from app.core.config import BASE_DIR, settings
from app.rag.document_loader import DocumentChunk,load_document_chunks
from app.rag.embedding import embed_texts
from app.rag.vector_store import create_collection,get_qdrant_client

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

def load_all_chunks() -> list[DocumentChunk]:
    all_chunks: list[DocumentChunk] = []

    markdown_files = sorted(KNOWLEDGE_BASE_DIR.glob("*.md"))
    for file_path in markdown_files:
        chunks = load_document_chunks(file_path)
        #extend tránh lồng list
        all_chunks.extend(chunks)

    return all_chunks

def create_points(chunks: list[DocumentChunk],vectors: list[list[float]]) -> list[PointStruct]:
    if len(chunks) != len(vectors):
        raise ValueError("No equal length of vectors and chunks")

    points: list[PointStruct] = []
    for chunk,vector in zip(chunks,vectors):
        point_id = str(uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"{chunk.document_id}:{chunk.chunk_index}"))

        point = PointStruct(id=point_id,
                            vector=vector,
                            payload={
                                "document_id": chunk.document_id,
                                "document_name": chunk.document_name,
                                "title": chunk.title,
                                "role_group": chunk.role_group,
                                "section_title": chunk.section_title,
                                "chunk_index": chunk.chunk_index,
                                "language": chunk.language,
                                "text": chunk.text,
                                "source_urls": chunk.source_urls,
                            })
        points.append(point)
    return points

def ingest_knowledge_base(batch_size: int=4)-> int:
    chunks = load_all_chunks()
    if not chunks:
        raise ValueError("Knowledge base do not have chunks.")
    #Lấy texts của all chunks
    texts=[chunk.text for chunk in chunks]
    vectors = embed_texts(texts,batch_size=batch_size)
    points = create_points(chunks,vectors)
    #Connect Qdrant Client
    client = get_qdrant_client()

    try:
        create_collection(client)
        client.upsert(collection_name=settings.QDRANT_COLLECTION,
                      points=points,
                      wait=True)
    finally:
        client.close()

    return len(points)










