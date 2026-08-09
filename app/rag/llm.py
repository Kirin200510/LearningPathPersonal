from functools import lru_cache
from openai import OpenAI
from app.core.config import settings

@lru_cache(maxsize=1)
def get_llm_client() -> OpenAI:
    if not settings.OPENCODE_API_KEY:
        raise ValueError("không có API key của Opencode" )

    return OpenAI(
        api_key=settings.OPENCODE_API_KEY,
        base_url=settings.LLM_BASE_URL)

def generate_answer(prompt: str) -> str:
    if not prompt.strip():
        return ValueError("Prompt empty")

    client = get_llm_client()
    response=client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    answer = response.choices[0].message.content
    return answer
