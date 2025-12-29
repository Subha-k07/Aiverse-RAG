import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def build_faiss_index(chunks):
    model = SentenceTransformer(MODEL_NAME)

    texts = [c["text"] for c in chunks]
    metadata = [c["metadata"] for c in chunks]

    embeddings = model.encode(texts, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs("vectorstore/faiss_index", exist_ok=True)

    faiss.write_index(index, "vectorstore/faiss_index/index.faiss")

    with open("vectorstore/faiss_index/metadata.pkl", "wb") as f:
        pickle.dump({"texts": texts, "metadata": metadata}, f)

    print(f"FAISS index built with {len(texts)} chunks")
