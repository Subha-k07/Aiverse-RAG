from langchain.text_splitter import RecursiveCharacterTextSplitter
from langdetect import detect


def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", ".", " "]
    )

    chunked_docs = []

    for doc in documents:
        chunks = splitter.split_text(doc["text"])

        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                "text": chunk,
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": i,
                    "language": detect_language(chunk)
                }
            })

    return chunked_docs
