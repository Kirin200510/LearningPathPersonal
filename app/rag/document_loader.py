from dataclasses import dataclass
from pathlib import Path
import re

import yaml

@dataclass
class DocumentChunk:
    document_id: str
    document_name: str
    title: str
    role_group: str
    section_title: str
    chunk_index: int
    language: str
    text: str
    source_urls: list[str]

def read_markdown_document(file_path: Path,) -> tuple[dict, str]:
    content=file_path.read_text(encoding='utf-8')

    front_matter_pattern = re.compile(
        r"^---\s*\n(.*?)\n---\s*\n(.*)$",
        re.DOTALL,
    )

    match = front_matter_pattern.match(content)

    if match is None:
        return {}, content.strip()

    metadata_text = match.group(1)
    markdown_body = match.group(2).strip()
    #Chuển thành kiểu dl python(dict)
    metadata = yaml.safe_load(metadata_text) or {}

    return metadata, markdown_body

def split_by_h2(markdown_body: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []

    current_title = "Giới thiệu"
    current_lines: list[str] = []

    for raw_line in markdown_body.splitlines():
        line = raw_line.strip()

        if line.startswith("## "):
            current_text = "\n".join(current_lines).strip()

            if current_text:
                sections.append((current_title, current_text))

            current_title = line.removeprefix("## ").strip()
            current_lines = []
            continue

        if line.startswith("# "):
            continue

        current_lines.append(raw_line)

    final_text = "\n".join(current_lines).strip()

    if final_text:
        sections.append((current_title, final_text))

    return sections

def load_document_chunks( file_path: Path) -> list[DocumentChunk]:
    metadata, markdown_body = read_markdown_document(file_path)
    sections = split_by_h2(markdown_body)
    document_id = metadata.get("id",file_path.stem)
    title = metadata.get("title",file_path.stem)
    role_group = metadata.get("role_group","unknown")
    language = metadata.get("language","vi")
    source_urls = metadata.get("source_urls", [], )
    chunks: list[DocumentChunk] = []
    for index, (section_title, section_text) in enumerate(sections):
        chunk_text = (f"Nghề nghiệp: {title}\n" 
                      f"Chủ đề: {section_title}\n\n" 
                      f"{section_text}")
        chunk = DocumentChunk(document_id=document_id,
                              document_name=file_path.name,
                              title=title,
                              role_group=role_group,
                              section_title=section_title,
                              chunk_index=index,
                              language=language,
                              text=chunk_text,
                              source_urls=source_urls)
        chunks.append(chunk)

    return chunks



