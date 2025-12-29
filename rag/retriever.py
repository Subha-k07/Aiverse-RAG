import os
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore", "faiss_index")

# -----------------------------
# Embeddings
# -----------------------------
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# -----------------------------
# Load FAISS
# -----------------------------
def load_vectorstore():
    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore

# -----------------------------
# Retrieve
# -----------------------------
def retrieve(query: str, language: str = "en", k: int = 5) -> List[Document]:
    vectorstore = load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    docs = retriever.invoke(query)

    if language:
        docs = [
            doc for doc in docs
            if doc.metadata.get("language", "en") == language
        ]

    return docs
