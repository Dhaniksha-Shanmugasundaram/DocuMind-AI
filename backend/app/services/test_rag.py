
from backend.app.services.rag_service import ask_question


def test_complete_rag_pipeline():

    result = ask_question(
        document_id="test-document",
        question="What is Python used for?"
    )

    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # Check that the question is returned
    assert result["question"] == "What is Python used for?"

    # Check that the AI generates an answer
    assert isinstance(result["answer"], str)
    assert len(result["answer"].strip()) > 0

    # Check that source references are returned
    assert isinstance(result["sources"], list)
    assert len(result["sources"]) > 0

    print("\nQuestion:", result["question"])
    print("\nAI Answer:", result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(
            "Page:", source["page_number"],
            "| Chunk:", source["chunk_index"]
        )

    print("\nComplete RAG pipeline test passed!")
