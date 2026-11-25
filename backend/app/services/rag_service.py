
from backend.app.services.retrieval_service import search_documents
from backend.app.services.llm_service import generate_answer


def ask_question(
    document_id: str,
    question: str,
    top_k: int = 10
) -> dict:
    """
    Retrieve relevant document chunks and generate an AI answer.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    # Step 1: Retrieve relevant chunks from FAISS
    retrieved_chunks = search_documents(
        document_id=document_id,
        question=question,
        top_k=top_k
    )

    if not retrieved_chunks:
        return {
            "question": question,
            "answer": "The answer is not available in the uploaded document.",
            "sources": []
        }

    # Step 2: Remove duplicate chunks
    unique_chunks = []
    seen_chunks = set()

    for chunk in retrieved_chunks:

        chunk_key = (
            chunk.metadata["page_number"],
            chunk.metadata["chunk_index"]
        )

        if chunk_key not in seen_chunks:
            seen_chunks.add(chunk_key)
            unique_chunks.append(chunk)

    # Step 3: Arrange chunks in original PDF order
    unique_chunks.sort(
        key=lambda chunk: (
            chunk.metadata["page_number"],
            chunk.metadata["chunk_index"]
        )
    )

    # Step 4: Prepare context for the LLM
    context_parts = []

    for chunk in unique_chunks:
        context_parts.append(
            f"[Page {chunk.metadata['page_number']}]\n"
            f"{chunk.page_content}"
        )

    context = "\n\n".join(context_parts)

    # Step 5: Generate answer using Ollama
    answer = generate_answer(
        question=question,
        context=context
    )

    # Step 6: Collect source references
    sources = [
        {
            "page_number": chunk.metadata["page_number"],
            "chunk_index": chunk.metadata["chunk_index"]
        }
        for chunk in unique_chunks
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }
