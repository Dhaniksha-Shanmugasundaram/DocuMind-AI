
from backend.app.services.text_splitter import split_text_into_chunks
from backend.app.services.vector_store import (
    create_vector_store,
    save_vector_store
)


def test_create_and_save_vector_store(tmp_path):

    # Sample document content
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

    assert vector_store is not None

    # Save the index in a temporary test directory
    save_path = tmp_path / "test-document"
    vector_store.save_local(str(save_path))

    assert save_path.exists()
    assert (save_path / "index.faiss").exists()

    print("Total chunks:", len(chunks))
    print("FAISS index created successfully!")
    print("FAISS index saved successfully!")
