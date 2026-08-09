from functools import lru_cache

import torch
from FlagEmbedding import BGEM3FlagModel

from app.core.config import settings

#lưu model cũ vào cache để dùng lại
@lru_cache(maxsize=1)
#lấy model để embedding
def get_embedding_model() -> BGEM3FlagModel:
    use_fp16 = torch.cuda.is_available()

    return BGEM3FlagModel(settings.EMBEDDING_MODEL, use_fp16=use_fp16)

def embed_texts(texts: list[str], batch_size: int = 4) -> list[list[float]]:

    cleaned_texts=  [" ".join(text.split())for text in texts]
    if not cleaned_texts: raise ValueError("No text to embedded.")
    if any(not text for text in cleaned_texts):
        raise ValueError("Text list contains empty text.")

    model = get_embedding_model()
    output = model.encode(
        cleaned_texts,
        batch_size=batch_size,
        max_length=1024,
        return_dense=True,
        return_sparse=False,
        return_colbert_vecs=False,
    )
    return output["dense_vecs"].tolist()

