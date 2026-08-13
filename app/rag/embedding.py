from functools import lru_cache

from FlagEmbedding import BGEM3FlagModel
from langchain_core.embeddings import Embeddings
import torch

from app.core.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> BGEM3FlagModel:
    use_fp16 = torch.cuda.is_available()

    return BGEM3FlagModel(
        settings.EMBEDDING_MODEL,
        use_fp16=use_fp16,
    )


class BGEM3Embeddings(Embeddings):
    """LangChain Embeddings adapter for the existing BGE-M3 model."""

    def __init__(self, batch_size: int = 4):
        self.batch_size = batch_size

    @staticmethod
    def _clean_texts(texts: list[str]) -> list[str]:
        cleaned_texts = [" ".join(text.split()) for text in texts]

        if not cleaned_texts:
            raise ValueError("No text to embed.")

        if any(not text for text in cleaned_texts):
            raise ValueError("Text list contains empty text.")

        return cleaned_texts

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        cleaned_texts = self._clean_texts(texts)
        model = get_embedding_model()

        output = model.encode(
            cleaned_texts,
            batch_size=self.batch_size,
            max_length=1024,
            return_dense=True,
            return_sparse=False,
            return_colbert_vecs=False,
        )

        return output["dense_vecs"].tolist()

    def embed_query(self, text: str) -> list[float]:
        cleaned_text = self._clean_texts([text])[0]
        model = get_embedding_model()

        output = model.encode(
            [cleaned_text],
            batch_size=1,
            max_length=1024,
            return_dense=True,
            return_sparse=False,
            return_colbert_vecs=False,
        )

        return output["dense_vecs"][0].tolist()


@lru_cache(maxsize=1)
def get_embeddings() -> BGEM3Embeddings:
    return BGEM3Embeddings()


# Giữ hàm này để các script cũ vẫn có thể test embedding trực tiếp.
def embed_texts(
    texts: list[str],
    batch_size: int = 4,
) -> list[list[float]]:
    return BGEM3Embeddings(batch_size=batch_size).embed_documents(texts)
