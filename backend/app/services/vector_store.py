
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from backend.app.services.embedding_service import (
    generate_embeddings
)


class LocalEmbeddingAdapter(Embeddings):

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return generate_embeddings(texts)

    def embed_query(self, text: str) -> list[float]:
        return generate_embeddings([text])[0]


def create_vector_store(chunks: list[dict]):

    if not chunks:
        raise ValueError("No text chunks provided")

    documents = []

    for chunk in chunks:
        document = Document(
            page_content=chunk["text"],
            metadata={
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"]
            }
        )

        documents.append(document)

    embedding_model = LocalEmbeddingAdapter()

    vector_store = FAISS.from_documents(
        documents,
        embedding_model
    )

    return vector_store


def save_vector_store(vector_store, document_id: str):

    index_path = Path("storage/indexes") / document_id
    index_path.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(index_path))

    return str(index_path)
