
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_into_chunks(
    pages: list,
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> list:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for index, chunk in enumerate(page_chunks):
            chunks.append({
                "page_number": page["page_number"],
                "chunk_index": index,
                "text": chunk
            })

    return chunks
