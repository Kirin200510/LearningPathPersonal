from pathlib import Path
import re

import yaml
from langchain_core.documents import Document

def read_markdown_file(file_path:Path)->Document:
    content=file_path.read_text(encoding='utf-8')

    pattern=re.compile(
        r"^---\s*\n(.*?)\n---\s*\n(.*)$",
        re.DOTALL,
    )
    match=pattern.match(content)
    if match is None:
        metadata={}
        markdown_body=content.strip()

    else:
        metadata_text=match.group(1)
        markdown_body=match.group(2).strip()

        metadata = yaml.safe_load(metadata_text)or {}
    metadata['document_name']=file_path.name
    metadata['source_path']=str(file_path)

    document = Document(
        page_content=markdown_body,
        metadata=metadata,
    )

    return document


