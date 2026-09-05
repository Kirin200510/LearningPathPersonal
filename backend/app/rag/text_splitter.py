from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
)
HEADERS_TO_SPLIT_ON = [
    ("#", "h1"),
    ("##", "h2")
]

def split_document(document: Document) -> List[Document]:
    #Constructor
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON,strip_headers=False)

    chunks=markdown_splitter.split_text(document.page_content)
    for index, chunk in enumerate(chunks):
        chunk.metadata={
            **document.metadata,
            **chunk.metadata,
            'chunk_index':index
        }
    return chunks
