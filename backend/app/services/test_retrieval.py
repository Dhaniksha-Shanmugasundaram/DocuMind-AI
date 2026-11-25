
from backend.app.services.text_splitter import split_text_into_chunks
from backend.app.services.vector_store import (
    create_vector_store,
    save_vector_store
)
from backend.app.services.retrieval_service import search_documents


def test_document_retrieval(tmp_path):

    # Create sample document content
    sample_pages = [
        {
            "page_number": 1,
            "text": (
                "Python is a programming language. "
                "It is used for AI and Machine Learning. "
            ) * 20
        },
        {
            "page_number": 2,
            "text": (
                "FastAPI helps developers build backend APIs. "
                "It is a Python web framework. "
            ) * 20
        }
    ]

    # Split document into chunks
    chunks = split_text_into_chunks(sample_pages)

    assert len(chunks) > 0

    # Create FAISS vector store
    vector_store = create_vector_store(chunks)

    # Save index in temporary storage
    document_id = "test-retrieval"
    index_path = tmp_path / "indexes" / document_id
    index_path.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(index_path))

    # Temporarily use the test index location
    import backend.app.services.retrieval_service as retrieval

    original_load = retrieval.load_vector_store

    def load_test_index(doc_id):
        from langchain_community.vectorstores import FAISS
        from backend.app.services.vector_store import LocalEmbeddingAdapter

        return FAISS.load_local(
            str(index_path),
            LocalEmbeddingAdapter(),
            allow_dangerous_deserialization=True
        )

    retrieval.load_vector_store = load_test_index

    try:
        results = search_documents(
            document_id=document_id,
            question="What is Python used for?",
            top_k=3
        )

        assert len(results) > 0
        assert all(result.page_content.strip() for result in results)

        print("Retrieved results:", len(results))
        print("Document retrieval test passed!")

    finally:
        retrieval.load_vector_store = original_load
