from pathlib import Path

from langchain_community.vectorstores import FAISS

from backend.app.services.vector_store import LocalEmbeddingAdapter


def load_vector_store(document_id: str):

    index_path = Path("storage/indexes") / document_id

    if not index_path.exists():
        raise FileNotFoundError("Vector index not found")

    embedding_model = LocalEmbeddingAdapter()

    vector_store = FAISS.load_local(
        str(index_path),
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return vector_store


def search_documents(
    document_id: str,
    question: str,
    top_k: int = 3
):

    vector_store = load_vector_store(document_id)

    results = vector_store.similarity_search(
        question,
        k=top_k
    )

    return results