from pathlib import Path
import re

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
import yaml


def read_markdown_document(file_path: Path) -> tuple[dict, str]:
    content = file_path.read_text(encoding="utf-8")

    front_matter_pattern = re.compile(
        r"^---\s*\n(.*?)\n---\s*\n(.*)$",
        re.DOTALL,
    )

    match = front_matter_pattern.match(content)

    if match is None:
        return {}, content.strip()

    metadata_text = match.group(1)
    markdown_body = match.group(2).strip()
    metadata = yaml.safe_load(metadata_text) or {}

    return metadata, markdown_body


def load_document_chunks(file_path: Path) -> list[Document]:
    """Load one Markdown knowledge document as LangChain Documents.

    Each H2 section becomes one retrievable Document while front-matter
    information is preserved in Document.metadata.
    """

    metadata, markdown_body = read_markdown_document(file_path)

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("##", "section_title")],
        strip_headers=True,
    )

    section_documents = splitter.split_text(markdown_body)

    document_id = metadata.get("id", file_path.stem)
    title = metadata.get("title", file_path.stem)
    role_group = metadata.get("role_group", "unknown")
    language = metadata.get("language", "vi")
    source_urls = metadata.get("source_urls", [])

    documents: list[Document] = []

    for index, section_document in enumerate(section_documents):
        section_title = section_document.metadata.get(
            "section_title",
            "Giới thiệu",
        )

        section_text = section_document.page_content.strip()

        page_content = (
            f"Nghề nghiệp: {title}\n"
            f"Chủ đề: {section_title}\n\n"
            f"{section_text}"
        )

        document = Document(
            id=f"{document_id}:{index}",
            page_content=page_content,
            metadata={
                "document_id": document_id,
                "document_name": file_path.name,
                "title": title,
                "role_group": role_group,
                "section_title": section_title,
                "chunk_index": index,
                "language": language,
                "source_urls": source_urls,
            },
        )

        documents.append(document)

    return documents
