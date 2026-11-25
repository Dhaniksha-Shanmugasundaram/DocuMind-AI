
from backend.app.services.text_splitter import split_text_into_chunks


def test_text_splitting():

    sample_pages = [
        {
            "page_number": 1,
            "text": "Python is a programming language. It is used for AI and Machine Learning. " * 100
        },
        {
            "page_number": 2,
            "text": "FastAPI is used to build APIs. It helps developers create backend applications. " * 100
        }
    ]

    chunks = split_text_into_chunks(sample_pages)

    # Check that chunks were generated
    assert len(chunks) > 0

    # Check that both pages are represented
    page_numbers = {chunk["page_number"] for chunk in chunks}
    assert page_numbers == {1, 2}

    # Check that every chunk contains text
    for chunk in chunks:
        assert chunk["text"].strip() != ""

    print("Total chunks generated:", len(chunks))
    print("Text splitting test passed!")
