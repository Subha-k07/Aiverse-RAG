import os
from typing import List
from deep_translator import GoogleTranslator

from rag.retriever import retrieve, Document


def generate_answer(query: str, language: str = "en", max_chunks: int = 5) -> str:
    """
    Generates a clean, concise answer from retrieved chunks with citations.
    """

    user_lang = language

    # 1️⃣ Translate query → English if needed
    if user_lang and user_lang != "en":
        translated_query = GoogleTranslator(
            source=user_lang, target="en"
        ).translate(query)
    else:
        translated_query = query

    # 2️⃣ Retrieve documents
    docs: List[Document] = retrieve(translated_query, k=max_chunks)

    if not docs:
        return "⚠️ No relevant documents found for your query."

    # 3️⃣ Build answer
    answer_lines = []
    seen = set()

    for doc in docs:
        text = doc.page_content.strip()
        if text in seen:
            continue
        seen.add(text)

        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 10]
        for s in sentences:
            answer_lines.append(
                f"{s}. (Source: {os.path.basename(doc.metadata.get('source',''))})"
            )

    answer = "\n".join(answer_lines[:6])

    # 4️⃣ Translate answer back to user language
    if user_lang and user_lang != "en":
        answer = GoogleTranslator(
            source="en", target=user_lang
        ).translate(answer)

    return answer
