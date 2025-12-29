import streamlit as st
from rag.generator import generate_answer

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AiVerse – Intelligent Policy Assistant",
    page_icon="🧠",
    layout="centered"
)

# -----------------------------
# Language Mapping
# -----------------------------
LANGUAGE_MAP = {
    "English": "en",
    "தமிழ்": "ta",
    "हिन्दी": "hi",
    "తెలుగు": "te",
    "മലയാളം": "ml",
    "ಕನ್ನಡ": "kn"
}

# -----------------------------
# UI Styles (Black + Blue only)
# -----------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff;
        color: #000000;
    }

    .title {
        color: #2563eb;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        color: #1e3a8a;
        font-size: 1rem;
        margin-bottom: 1.8rem;
    }

    .chip {
        display: inline-block;
        padding: 6px 14px;
        margin: 6px 6px 0 0;
        border: 1px solid #2563eb;
        border-radius: 20px;
        color: #2563eb;
        font-size: 0.85rem;
        cursor: pointer;
    }

    .chip:hover {
        background-color: #2563eb;
        color: #ffffff;
    }

    .answer-card {
        border: 1px solid #2563eb;
        border-radius: 8px;
        padding: 16px;
        background-color: #f9fbff;
        margin-top: 12px;
    }

    .answer-title {
        color: #2563eb;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .disclaimer {
        font-size: 0.8rem;
        color: #1e3a8a;
        margin-top: 10px;
    }

    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 8px 22px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.markdown("<div class='title'>AiVerse – Intelligent Policy Assistant</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Ask questions from policy documents using AI-powered retrieval</div>",
    unsafe_allow_html=True
)

# -----------------------------
# Suggested Question Chips
# -----------------------------
st.markdown("**Suggested questions**")

suggested_questions = [
    "What are the biggest risks for startups in India?",
    "What policies support MSMEs in India?",
    "What are the major challenges in Indian FinTech?",
    "How does the government support early-stage startups?"
]

if "query" not in st.session_state:
    st.session_state.query = ""

cols = st.columns(len(suggested_questions))
for i, q in enumerate(suggested_questions):
    if cols[i].button(q):
        st.session_state.query = q

# -----------------------------
# Language Selector
# -----------------------------
language = st.radio(
    "Select language",
    list(LANGUAGE_MAP.keys()),
    horizontal=True
)

# -----------------------------
# Query Input
# -----------------------------
query = st.text_input(
    "Enter your question",
    value=st.session_state.query,
    placeholder="Type your question here..."
)

# -----------------------------
# Submit Button
# -----------------------------
if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Processing your query..."):
            lang_code = LANGUAGE_MAP.get(language, "en")
            answer = generate_answer(query, language=lang_code)

        st.markdown(
            f"""
            <div class="answer-card">
                <div class="answer-title">AI-Generated Answer</div>
                <div>{answer}</div>
                <div class="disclaimer">
                    This response is generated from retrieved policy documents and may not replace official or legal guidance.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# How It Works (Expandable)
# -----------------------------
with st.expander("How AiVerse works"):
    st.markdown(
        """
        **AiVerse** uses a Retrieval-Augmented Generation (RAG) pipeline:

        • Policy documents are ingested and cleaned  
        • Text is embedded using open-source language models  
        • FAISS vector search retrieves relevant content  
        • Answers are synthesized and translated if needed  

        This ensures responses are **grounded in real documents**, not hallucinated.
        """
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#2563eb; font-size:0.85rem;'>"
    "© 2025 AiVerse | Powered by LangChain & Open-Source AI Models"
    "</div>",
    unsafe_allow_html=True
)
