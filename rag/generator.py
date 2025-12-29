import os
from typing import List
from googletrans import Translator  # for Indic language query handling

from retriever import retrieve, Document

# -----------------------------
# Translator Setup (Optional)
# -----------------------------
translator = Translator()

# -----------------------------
# Answer Generator
# -----------------------------
def generate_answer(query: str, language: str = None, max_chunks: int = 5) -> str:
    """
    Generates a clean, concise answer from retrieved chunks with citations.
    
    Args:
        query (str): User query
        language (str): Optional, user language code (e.g., 'hi' for Hindi)
        max_chunks (int): Number of chunks to retrieve
    
    Returns:
        str: Synthesized answer with citations
    """

    # Step 1: Translate query to English if needed
    user_lang = language
    if language and language != "en":
        translated_query = translator.translate(query, src=language, dest="en").text
    else:
        translated_query = query

    # Step 2: Retrieve top chunks from FAISS
    docs: List[Document] = retrieve(translated_query, language=None, k=max_chunks)

    if not docs:
        return "⚠️ No relevant documents found for your query."

    # Step 3: Synthesize answer
    answer_lines = []
    seen_texts = set()  # to avoid duplicates

    for i, doc in enumerate(docs, 1):
        text = doc.page_content.strip()
        # Simple deduplication
        if text in seen_texts:
            continue
        seen_texts.add(text)

        # Split into sentences for inline citation
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]
        for s in sentences:
            answer_lines.append(f"{s.strip()}. (Source: {os.path.basename(doc.metadata.get('source',''))})")

    # Step 4: Join top N sentences (limit length)
    MAX_SENTENCES = 6
    answer = "\n".join(answer_lines[:MAX_SENTENCES])

    # Step 5: Translate answer back to user language if needed
    if user_lang and user_lang != "en":
        answer = translator.translate(answer, src="en", dest=user_lang).text

    return answer

# -----------------------------
# Interactive CLI
# -----------------------------
def main():
    print("🟢 RAG Generator - Level 5")
    print("Type 'exit' to quit.\n")

    user_lang = input("Enter your language code (en for English, hi for Hindi, etc.): ").strip().lower()
    if user_lang == "":
        user_lang = "en"

    while True:
        query = input("\n🧠 Enter your query: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        print("\n📌 Generating answer...\n")
        answer = generate_answer(query, language=user_lang)
        print(answer)
        print("\n" + "-"*80)

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
