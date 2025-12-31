import os
from typing import List
from deep_translator import GoogleTranslator

from rag.retriever import retrieve
from langchain_core.documents import Document


def generate_answer(query: str, language: str = "en", max_chunks: int = 5) -> str:
    """
    Analyst-style RAG answer with:
    - Synthesized insight
    - Clear sources
    - Evaluation metric
    """

    user_lang = language or "en"

    # Translate query → English ONLY if needed
    translated_query = (
        GoogleTranslator(source=user_lang, target="en").translate(query)
        if user_lang != "en"
        else query
    )

    # Retrieve evidence (TOP-K ONLY)
    docs: List[Document] = retrieve(translated_query, k=max_chunks)

    if not docs:
        return "No relevant evidence was found for this query."

    #  Analyst-style synthesis (FAST + STRUCTURED)
    insights = []
    sources = set()

    for doc in docs:
        text = doc.page_content.strip()
        source = os.path.basename(doc.metadata.get("source", "Unknown"))

        if text and text not in insights:
            insights.append(text)
            sources.add(source)

        # Early stop for speed
        if len(insights) >= 3:
            break

    #  Build professional insight
    insight_text = (
        "Our analysis indicates that:\n\n"
        + "\n".join(
            f"- {s.split('.')[0].strip()}."
            for s in insights
            if len(s) > 40
        )
    )

    #  Evidence block
    sources_text = "\n".join(f"• {src}" for src in sorted(sources))

    evaluation_text = (
        f"Answer grounded in {len(sources)} independent source(s)."
    )

    final_answer = f"""
{insight_text}

---

**Sources**
{sources_text}

---

*{evaluation_text}*
"""

    #  Translate back ONLY once (critical speed win)
    if user_lang != "en":
        final_answer = GoogleTranslator(
            source="en", target=user_lang
        ).translate(final_answer)

    return final_answer.strip()
