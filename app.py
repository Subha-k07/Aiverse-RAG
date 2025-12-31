import time
import streamlit as st
from rag.generator import generate_answer

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="AiVerse – AI Investment Intelligence",
    page_icon="🌊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# Language Mapping
# -------------------------------------------------
LANGUAGE_MAP = {
    "English": "en",
    "தமிழ்": "ta",
    "हिन्दी": "hi",
    "తెలుగు": "te",
    "മലയാളം": "ml",
    "ಕನ್ನಡ": "kn"
}

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "query" not in st.session_state:
    st.session_state.query = ""

# -------------------------------------------------
# Global Styles – Ocean Theme
# -------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff;
        color: #0f172a;
    }

    /* ---------- Header ---------- */
    .title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0b5ed7;
        margin-bottom: 0.25rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 2rem;
    }

    /* ---------- Cards ---------- */
    .card {
        background: linear-gradient(180deg, #f8fbff, #eef6ff);
        border: 1.5px solid #cfe2ff;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    }

    /* ---------- Suggested Buttons ---------- */
    div.stButton > button {
        background: linear-gradient(180deg, #f8fbff, #eef6ff) !important;
        color: #0b5ed7 !important;
        border: 1.5px solid #0b5ed7 !important;
        border-radius: 12px;
        height: 90px;
        width: 100%;
        font-size: 0.95rem;
        font-weight: 600;
        white-space: normal;
        box-shadow: 0 6px 18px rgba(11, 94, 215, 0.15);
    }

    div.stButton > button:hover {
        background: #e7f1ff !important;
    }

    /* ---------- Input ---------- */
    input {
        border-radius: 10px !important;
        border: 1.5px solid #cfe2ff !important;
    }

    /* ---------- Answer Card ---------- */
    .answer-card {
        margin-top: 1rem;
        padding: 22px;
        border-radius: 16px;
        background: linear-gradient(180deg, #ffffff, #f4f9ff);
        border: 1.5px solid #0b5ed7;
        box-shadow: 0 14px 40px rgba(11, 94, 215, 0.18);
        color: #0f172a;
    }

    /* ---------- Confidence Badge ---------- */
    .confidence {
        display: inline-block;
        background-color: #e7f1ff;
        color: #0b5ed7;
        border: 1px solid #0b5ed7;
        padding: 5px 12px;
        font-size: 0.75rem;
        border-radius: 999px;
        margin-bottom: 10px;
        font-weight: 600;
    }

    /* ---------- Skeleton ---------- */
    .skeleton {
        height: 14px;
        border-radius: 6px;
        margin-bottom: 12px;
        background: linear-gradient(
            90deg,
            #e7f1ff 25%,
            #d0e3ff 37%,
            #e7f1ff 63%
        );
        background-size: 400% 100%;
        animation: shimmer 1.4s ease infinite;
    }

    @keyframes shimmer {
        0% { background-position: 100% 0; }
        100% { background-position: -100% 0; }
    }

    /* ---------- Disclaimer ---------- */
    .disclaimer {
        margin-top: 16px;
        font-size: 0.85rem;
        color: #475569;
        border-left: 4px solid #0b5ed7;
        padding-left: 12px;
    }

    /* ---------- Footer ---------- */
    .footer {
        text-align: center;
        margin-top: 3rem;
        font-size: 0.85rem;
        color: #0b5ed7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("<div class='title'>AiVerse – AI Investment Intelligence Analyst</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Source-grounded investment insights from fragmented startup and funding data</div>",
    unsafe_allow_html=True
)

# -------------------------------------------------
# Language Selector
# -------------------------------------------------
language = st.radio(
    "Select language",
    list(LANGUAGE_MAP.keys()),
    horizontal=True
)

# -------------------------------------------------
# Suggested Questions
# -------------------------------------------------
st.markdown("### Suggested intelligence queries")

q1, q2 = st.columns(2)
q3, q4 = st.columns(2)

with q1:
    if st.button("Which investors actively fund early-stage AI startups in India?"):
        st.session_state.query = "Which investors actively fund early-stage AI startups in India?"

with q2:
    if st.button("What funding trends are emerging in Indian FinTech startups?"):
        st.session_state.query = "What funding trends are emerging in Indian FinTech startups?"

with q3:
    if st.button("Which VCs have invested in similar startups over the last 2 years?"):
        st.session_state.query = "Which VCs have invested in similar startups over the last 2 years?"

with q4:
    if st.button("What signals indicate strong product–market fit for funded startups?"):
        st.session_state.query = "What signals indicate strong product–market fit for funded startups?"

# -------------------------------------------------
# Query Input
# -------------------------------------------------
query = st.text_input(
    "Enter your question",
    value=st.session_state.query,
    placeholder="Ask about investors, funding patterns, or startup intelligence..."
)

# -------------------------------------------------
# Submit
# -------------------------------------------------
if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        lang_code = LANGUAGE_MAP.get(language, "en")

        # Skeleton loader
        with st.container():
            st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)
            st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)
            st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)

        start = time.time()
        answer = generate_answer(query, language=lang_code)
        latency = round(time.time() - start, 2)

        st.markdown("### Generated Insight")

        st.markdown(
            f"""
            <div class="confidence">
                Answer grounded in multiple sources • Generated in {latency}s
            </div>
            <div class="answer-card">
                {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="disclaimer">
                <strong>Disclaimer</strong><br>
                This insight is generated using publicly available startup, policy,
                and funding data processed through a Retrieval-Augmented Generation (RAG) system.
                It is intended for <em>research and informational purposes only</em>
                and should not be treated as financial or investment advice.
            </div>
            """,
            unsafe_allow_html=True
        )

# -------------------------------------------------
# How the RAG Model Works
# -------------------------------------------------
with st.expander("How the RAG model works"):
    st.write(
        """
        1. **Query Understanding** – Your question is normalized and translated if required.  
        2. **Retrieval** – Relevant startup, investor, and policy documents are fetched using semantic search.  
        3. **Grounding** – Only retrieved evidence is used to prevent hallucinations.  
        4. **Synthesis** – An analyst-style insight is generated and backed by explicit sources.
        """
    )

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("<div class='footer'>© 2025 AiVerse | Built with RAG & Open-Source AI</div>", unsafe_allow_html=True)
