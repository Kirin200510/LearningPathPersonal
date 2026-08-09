from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
class Settings(BaseSettings):
    DATABASE_URI: str

    OPENCODE_API_KEY: str | None = None
    LLM_MODEL: str = "deepseek-v4-flash"
    LLM_BASE_URL: str
    EMBEDDING_MODEL: str = "BAAI/bge-m3"
    QDRANT_PATH: str = "qdrant_storage"
    QDRANT_COLLECTION: str = "learning_knowledge"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
