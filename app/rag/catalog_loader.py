import json
from pathlib import Path

from langchain_core.documents import Document
from sqlalchemy.testing.suite.test_reflection import metadata

from app.core.config import BASE_DIR

CATALOG_PATH = BASE_DIR / "data" / "learning_catalog.json"


def read_catalog() -> dict:
    content = CATALOG_PATH.read_text(encoding="utf-8")

    data = json.loads(content)
    return data


def format_list(values: list[str]) -> str:
    if not values:
        return "Không có thông tin"

    return ", ".join(values)


def build_program_content(program: dict) -> str:
    title = program.get("title")
    description = program.get("description")
    levels = program.get("levels")
    roles = program.get("roles")
    topics = program.get("topics")
    technologies = program.get("technologies")
    learning_items = program.get("learning_items")
    items = []

    for item in learning_items:
        order = item.get("order")
        item_title = item.get("title")
        items.append(f"{order}. {item_title}")
    curriculum = "\n".join(items)
    content = f"""
    Program: {title}

    Description:
    {description}

    Levels:
    {levels}

    Target roles:
    {roles}

    Topics:
    {topics}

    Technologies:
    {technologies}

    Learning items:
    {curriculum}
    """.strip()

    return content

def create_program_document(program: dict) -> Document:
    content = build_program_content(program)
    metadata= {
        "document_type": "learning_program",
        "source":program.get("source"),
        "source_id":program.get("source_id"),
        "title":program.get("title"),
        "description":program.get("description"),
        "url":program.get("url"),
        "levels":program.get("levels"),
        "roles":program.get("roles"),
        "topics":program.get("topics"),
        "technologies":program.get("technologies"),
    }
    document = Document(page_content=content, metadata=metadata)
    return document

def load_catalog_documents()->list[Document]:
    programs=load_catalog_programs()
    documents = []
    for program in programs:
        document=create_program_document(program)
        documents.append(document)

    return documents

def load_catalog_programs()->dict:
    data = read_catalog()
    programs = data.get("programs")
    return programs
