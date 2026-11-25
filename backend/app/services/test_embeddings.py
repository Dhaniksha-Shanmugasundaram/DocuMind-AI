
from backend.app.services.embedding_service import generate_embeddings


def test_generate_embeddings():

    sample_texts = [
        "Python is a programming language.",
        "FastAPI is used to build backend APIs."
    ]

    embeddings = generate_embeddings(sample_texts)

    # Check that embeddings are generated
    assert len(embeddings) == 2

    # Check that embeddings have valid dimensions
    assert len(embeddings[0]) == 384

    # Check that each embedding is a valid vector
    for embedding in embeddings:
        assert len(embedding) == 384

    print("Number of embeddings:", len(embeddings))
    print("Vector dimensions:", len(embeddings[0]))
    print("Embedding test passed!")
