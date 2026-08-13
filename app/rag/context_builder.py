from langchain_core.documents import Document


def build_context(documents: list[Document]) -> str:
    context_parts: list[str] = []

    for index, document in enumerate(documents, start=1):
        text = document.page_content.strip()

        if not text:
            continue

        context_parts.append(
            f"[Context {index}]\n{text}"
        )

    return "\n\n".join(context_parts)
