from functools import lru_cache

import torch
from FlagEmbedding import BGEM3FlagModel

from langchain_core.embeddings import Embeddings

from app.core.config import settings

@lru_cache(maxsize=1)
def get_bge_model() -> BGEM3FlagModel:
    use_fp16 = torch.cuda.is_available()

    model = BGEM3FlagModel(
        settings.EMBEDDING_MODEL,
        use_fp16=use_fp16,
    )

    return model

class BGEM3Embeddings(Embeddings):
    def embed_documents(self, texts: list[str],) -> list[list[float]]:
        model = get_bge_model()
        result = model.encode(
            texts,
            batch_size=4,
            max_length=1024,
            return_dense=True,
            return_sparse=False,
            return_colbert_vecs=False,
        )
        return result["dense_vecs"].tolist()

    def embed_query(self,text: str,) -> list[float]:
        model = get_bge_model()

        result = model.encode(
            [text],
            batch_size=1,
            max_length=1024,
            return_dense=True,
            return_sparse=False,
            return_colbert_vecs=False,
        )

        return result["dense_vecs"][0].tolist()

@lru_cache(maxsize=1)
def get_embeddings() -> BGEM3Embeddings:
    return BGEM3Embeddings()

