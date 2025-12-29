import streamlit as st
from rag.generator import generate_answer

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AiVerse – AI Investment Intelligence",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
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
# UI Styles
# -----------------------------
st.markdown(
    """
    <style>

    body {
        background-color: #000000;
        color: #000000;
    }

    /* Header */
    .title {
        font-size: 2rem;
        font-weight: 700;
        color: #2563eb;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }

    /* Suggested question boxes */
    .suggestion-box {
        border: 1.5px solid #2563eb;
        background-color: #000000;
        color: #2563eb;
        padding: 14px;
        border-radius: 8px;
        font-size: 0.9rem;
        height: 90px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        cursor: pointer;
    }

    .suggestion-box:hover {
        background-color: #020617;
    }

    /* Buttons */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 8px 22px;
    }

    /* Radio buttons */
    .stRadio label {
        color: #000000 !important;
        font-weight: 600;
    }

    /* Answer card */
    .answer-card {
        border: 1px solid #2563eb;
        border-radius: 10px;
        padding: 18px;
        background-color: #020617;
        color: #e5e7eb;
        margin-top: 1rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #2563eb;
        font-size: 0.85rem;
        margin-top: 2rem;
    }

    .disclaimer {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.markdown("<div class='title'>AiVerse – AI Investment Intelligence Analyst</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Turn fragmented startup and funding data into actionable intelligence for founders and VCs</div>",
    unsafe_allow_html=True
)

# -----------------------------
# Suggested Questions
# -----------------------------
st.markdown("**Suggested intelligence queries**")

if "query" not in st.session_state:
    st.session_state.query = ""

suggested_questions = [
    "Which investors actively fund early-stage AI startups in India?",
    "What funding trends are emerging in Indian FinTech startups?",
    "Which VCs have invested in similar startups over the last 2 years?",
    "What signals indicate strong product–market fit for funded startups?"
]

cols = st.columns(2)
for idx, question in enumerate(suggested_questions):
    with cols[idx % 2]:
        if st.button(question, key=f"suggest_{idx}"):
            st.session_state.query = question

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
    placeholder="Ask about investors, funding trends, or startup intelligence..."
)

# -----------------------------
# Submit Button
# -----------------------------
if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing data and retrieving insights..."):
            lang_code = LANGUAGE_MAP.get(language, "en")
            answer = generate_answer(query, language=lang_code)

        st.markdown("### Generated Insight")
        st.markdown(
            f"<div class='answer-card'>{answer}</div>",
            unsafe_allow_html=True
        )

# -----------------------------
# How it works
# -----------------------------
with st.expander("How AiVerse works"):
    st.markdown(
        """
        **AiVerse is a production-grade Retrieval-Augmented Generation (RAG) system.**

        - Ingests startup, funding, and policy-related documents  
        - Converts unstructured data into vector embeddings  
        - Retrieves only the most relevant sources using semantic search  
        - Generates grounded answers using an LLM with retrieved context  

        This architecture minimizes hallucinations and ensures context-aware,
        verifiable insights for investment decision-making.
        """
    )

# -----------------------------
# Disclaimer
# -----------------------------
st.markdown(
    "<div class='disclaimer'>"
    "Disclaimer: AiVerse provides AI-generated insights based on available data. "
    "It does not constitute financial or investment advice."
    "</div>",
    unsafe_allow_html=True
)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "<div class='footer'>© 2025 AiVerse | Powered by LangChain & Open-Source AI Models</div>",
    unsafe_allow_html=True
)
