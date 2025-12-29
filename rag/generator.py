import os
from typing import List

from deep_translator import GoogleTranslator
from retriever import retrieve, Document

# -----------------------------
# Answer Generator
# -----------------------------
def generate_answer(query: str, language: str = "en", max_chunks: int = 5) -> str:
    """
    Generates a clean, concise answer from retrieved chunks with citations.

    Args:
        query (str): User query
        language (str): User language code (e.g., 'hi', 'ta', 'en')
        max_chunks (int): Number of chunks to retrieve

    Returns:
        str: Synthesized answer with citations
    """

    user_lang = language or "en"

    # Step 1: Translate query to English if needed
    if user_lang != "en":
        translated_query = GoogleTranslator(
            source=user_lang, target="en"
        ).translate(query)
    else:
        translated_query = query

    # Step 2: Retrieve top chunks from FAISS
    docs: List[Document] = retrieve(translated_query, language=None, k=max_chunks)

    if not docs:
        return "⚠️ No relevant documents found for your query."

    # Step 3: Synthesize answer
    answer_lines = []
    seen_texts = set()

    for doc in docs:
        text = doc.page_content.strip()

        if text in seen_texts:
            continue
        seen_texts.add(text)

        source = os.path.basename(doc.metadata.get("source", "unknown"))

        sentences = [
            s.strip() for s in text.split(".")
            if len(s.strip()) > 10
        ]

        for sentence in sentences:
            answer_lines.append(
                f"{sentence}. (Source: {source})"
            )

    # Step 4: Limit output size
    MAX_SENTENCES = 6
    answer = "\n".join(answer_lines[:MAX_SENTENCES])

    # Step 5: Translate answer back to user language if needed
    if user_lang != "en":
        answer = GoogleTranslator(
            source="en", target=user_lang
        ).translate(answer)

    return answer


# -----------------------------
# Interactive CLI
# -----------------------------
def main():
    print("🟢 RAG Generator - Level 5")
    print("Type 'exit' to quit.\n")

    user_lang = input(
        "Enter your language code (en for English, hi for Hindi, etc.): "
    ).strip().lower() or "en"

    while True:
        query = input("\n🧠 Enter your query: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("Exiting...")
            break

        print("\n📌 Generating answer...\n")
        answer = generate_answer(query, language=user_lang)
        print(answer)
        print("\n" + "-" * 80)


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
