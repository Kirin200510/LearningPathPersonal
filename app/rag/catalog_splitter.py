from langchain_core.documents import Document
from sqlalchemy.testing.suite.test_reflection import metadata

from app.rag.catalog_loader import load_catalog_programs

ITEMS_PER_CHUNK = 3

def build_learning_items_content(learning_items: list[dict]) -> str:
    item_blocks = []
    for item in learning_items:
        order = item.get("order")
        title = item.get("title")
        description = item.get("description")
        duration = item.get("duration")
        block = f"""
{order}. {title}

Description:
{description}
""".strip()
        if duration:
            block += (f"\n Duration: "
                      f"{duration} minutes")
        item_blocks.append(block)

    return "\n\n".join(item_blocks)


def split_program(program:dict,item_per_chunk:int=ITEMS_PER_CHUNK) -> list[Document]:
    learning_items = program.get("learning_items")
    chunks = []
    for start in range(0, len(learning_items), item_per_chunk):
        chunk_items = learning_items[start:start + item_per_chunk]
        chunk_index=start//item_per_chunk
        learning_content=build_learning_items_content(chunk_items)
        content=f"""
Program:
{program.get("title", "")}

Description:
{program.get("description", "")}

Levels:
{program.get("levels")}

Target roles:
{program.get("roles")}

Topics:
{program.get("topics")}

Technologies:
{program.get("technologies")}

Learning items:
{learning_content}
""".strip()
        metadata={
            "document_type":"learning_program_chunk",
            "source": program.get("source"),
            "source_id": program.get("source_id"),
            "title": program.get("title"),
            "url": program.get("url"),
            "levels": program.get("levels"),
            "roles": program.get("roles"),
            "topics": program.get("topics"),
            "technologies": program.get("technologies"),
            "chunk_index": chunk_index,
            "item_start": chunk_items[0].get("order")
            ,
            "item_end":chunk_items[-1].get("order")
        }
        document=Document(page_content=content,metadata=metadata)
        chunks.append(document)
    return chunks

def load_catalog_chunks(item_per_chunk: int = ITEMS_PER_CHUNK) -> list[Document]:
    programs = load_catalog_programs()

    all_chunks = []
    for program in programs:
        program_chunks = split_program(program=program, item_per_chunk=item_per_chunk)
        all_chunks.extend(program_chunks)

    return all_chunks

