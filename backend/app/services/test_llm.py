
from backend.app.services.llm_service import generate_answer


def test_llm_answer_generation():

    question = "What is Python?"

    context = (
        "Python is a programming language "
        "used for AI and Machine Learning."
    )

    answer = generate_answer(question, context)

    # Check that the LLM returns a non-empty answer
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0

    print("\nQuestion:", question)
    print("\nAI Answer:", answer)
    print("\nLLM test passed!")
