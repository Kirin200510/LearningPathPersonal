from functools import lru_cache

from langchain_openai import ChatOpenAI

from app.core.config import settings


@lru_cache(maxsize=1)
def get_llm() -> ChatOpenAI:
    if not settings.OPENCODE_API_KEY:
        raise ValueError("Không có API key của OpenCode.")

    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENCODE_API_KEY,
        base_url=settings.LLM_BASE_URL,
        temperature=0,
    )
