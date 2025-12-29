import os
import re
from tqdm import tqdm
from langdetect import detect

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


# -------------------------
# CONFIG
# -------------------------
DATA_DIR = "data/raw"
VECTORSTORE_DIR = "vectorstore/faiss_index"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
BATCH_SIZE = 64   # 🔥 critical

os.makedirs(VECTORSTORE_DIR, exist_ok=True)


# -------------------------
# Utils
# -------------------------
def clean_text(text: str) -> str:
    """Hard clean for PDF poison"""
    if not isinstance(text, str):
        return ""

    text = text.replace("\x00", "")           # remove null bytes
    text = re.sub(r"\s+", " ", text)           # normalize spaces
    text = text.strip()

    if len(text) < 20:
        return ""

    return text


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"


# -------------------------
# Load Documents
# -------------------------
def load_documents():
    documents = []

    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            path = os.path.join(root, file)

            try:
                if file.lower().endswith(".pdf"):
                    documents.extend(PyPDFLoader(path).load())
                elif file.lower().endswith(".txt"):
                    documents.extend(TextLoader(path, encoding="utf-8").load())
            except Exception as e:
                print(f"⚠️ Skipped {file}: {e}")

    return documents


# -------------------------
# Main
# -------------------------
def main():
    print("🔹 Loading documents...")
    docs = load_documents()
    print(f"📄 Loaded documents: {len(docs)}")

    print("🔹 Chunking...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    print(f"🧩 Raw chunks: {len(chunks)}")

    print("🔹 Cleaning & tagging...")
    texts, metadatas = [], []

    for chunk in tqdm(chunks):
        text = clean_text(chunk.page_content)
        if not text:
            continue

        texts.append(text)
        metadatas.append({
            "source": chunk.metadata.get("source", ""),
            "language": detect_language(text)
        })

    print(f"✅ Clean chunks ready: {len(texts)}")

    # -------------------------
    # Embedding (SAFE MODE)
    # -------------------------
    print("🔹 Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    vectorstore = None
    failed = 0

    print("🔹 Building FAISS index (batch-safe)...")

    for i in tqdm(range(0, len(texts), BATCH_SIZE)):
        batch_texts = texts[i:i + BATCH_SIZE]
        batch_meta = metadatas[i:i + BATCH_SIZE]

        try:
            if vectorstore is None:
                vectorstore = FAISS.from_texts(
                    batch_texts,
                    embeddings,
                    metadatas=batch_meta
                )
            else:
                vectorstore.add_texts(batch_texts, metadatas=batch_meta)

        except Exception as e:
            failed += len(batch_texts)
            print(f"⚠️ Skipped batch {i}-{i+BATCH_SIZE}: {e}")

    vectorstore.save_local(VECTORSTORE_DIR)

    print("🎉 FAISS index built successfully!")
    print(f"📁 Stored at: {VECTORSTORE_DIR}")
    print(f"❌ Failed chunks skipped: {failed}")


if __name__ == "__main__":
    main()
