import os
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document   # ✅ FIXED IMPORT

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
    print("📁 Loading FAISS from:", VECTORSTORE_DIR)
    print("📄 Files:", os.listdir(VECTORSTORE_DIR))

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

    # ✅ New LangChain API
    docs = retriever.invoke(query)

    # Optional language filtering
    if language:
        docs = [
            doc for doc in docs
            if doc.metadata.get("language", "en") == language
        ]

    return docs

# -----------------------------
# Test
# -----------------------------
if __name__ == "__main__":
    query = "What is artificial intelligence?"

    results = retrieve(query)

    print(f"\n🔍 Retrieved {len(results)} documents\n")

    for i, doc in enumerate(results, 1):
        print(f"--- Chunk {i} ---")
        print(doc.page_content[:300])
        print("Metadata:", doc.metadata)
        print()
