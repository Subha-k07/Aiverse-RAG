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
# Session State
# -----------------------------
if "query" not in st.session_state:
    st.session_state.query = ""

# -----------------------------
# UI Styles
# -----------------------------
st.markdown(
    """
    <style>

    body {
        background-color: #000000;
        color: #e5e7eb;
    }

    /* Title */
    .title {
        font-size: 2rem;
        font-weight: 700;
        color: #2563eb;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 1.6rem;
    }

    /* Suggested questions container */
    .suggestions {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
        margin-bottom: 1.5rem;
    }

    /* Individual suggestion box */
    .suggestion-box {
        border: 1.5px solid #2563eb;
        background-color: #000000;
        color: #2563eb;
        padding: 16px;
        border-radius: 8px;
        font-size: 0.9rem;
        height: 90px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        cursor: pointer;
        transition: background 0.2s ease;
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
# Suggested Questions (HTML-based, FIXED)
# -----------------------------
st.markdown("**Suggested intelligence queries**")

suggested_questions = [
    "Which investors actively fund early-stage AI startups in India?",
    "What funding trends are emerging in Indian FinTech startups?",
    "Which VCs have invested in similar startups over the last 2 years?",
    "What signals indicate strong product–market fit for funded startups?"
]

html = "<div class='suggestions'>"
for q in suggested_questions:
    html += f"""
    <form method="post">
        <button name="suggested" value="{q}" class="suggestion-box">
            {q}
        </button>
    </form>
    """
html += "</div>"

st.markdown(html, unsafe_allow_html=True)

# Handle click
if "suggested" in st.query_params:
    st.session_state.query = st.query_params["suggested"]

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
# Submit
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
        AiVerse is a production-grade Retrieval-Augmented Generation (RAG) system.

        - Ingests startup, funding, and investor documents  
        - Converts unstructured data into embeddings  
        - Retrieves only the most relevant sources  
        - Generates grounded, context-aware insights  

        Designed to minimize hallucinations and support real investment decisions.
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
