from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_document(pages):
    """
    Splits extracted PDF pages into smaller chunks while
    preserving page number metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = []

    for page in pages:
        page_number = page["page_number"]
        text = page["text"]

        split_texts = splitter.split_text(text)

        for i, chunk in enumerate(split_texts):
            chunks.append({
                "page_number": page_number,
                "chunk_id": i + 1,
                "text": chunk,
            })

    return chunks