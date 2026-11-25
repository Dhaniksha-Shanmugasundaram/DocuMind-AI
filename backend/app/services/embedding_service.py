from sentence_transformers import SentenceTransformer


# Load the local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convert text into numerical embeddings.
    """

    if not texts:
        return []

    embeddings = model.encode(texts)

    return embeddings.tolist()