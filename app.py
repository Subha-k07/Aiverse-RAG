import time
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
# Global Styles
# -----------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #e5e7eb;
    }

    .title {
        font-size: 2rem;
        font-weight: 700;
        color: #2563eb;
    }

    .subtitle {
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }

    /* Suggested question buttons */
    div.stButton > button {
        background-color: #000000 !important;
        color: #2563eb !important;
        border: 1.5px solid #2563eb !important;
        border-radius: 8px;
        height: 90px;
        width: 100%;
        font-size: 0.9rem;
        font-weight: 500;
        white-space: normal;
    }

    div.stButton > button:hover {
        background-color: #020617 !important;
    }

    /* Answer card */
    .answer-card {
        border: 1px solid #2563eb;
        background-color: #020617;
        border-radius: 10px;
        padding: 18px;
        margin-top: 1rem;
    }

    /* Confidence badge */
    .confidence-badge {
        display: inline-block;
        background-color: #020617;
        border: 1px solid #2563eb;
        color: #2563eb;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 999px;
        margin-bottom: 8px;
    }

    /* Loading skeleton */
    .skeleton {
        background: linear-gradient(
            90deg,
            #020617 25%,
            #0f172a 37%,
            #020617 63%
        );
        animation: shimmer 1.4s ease infinite;
        background-size: 400% 100%;
        height: 14px;
        border-radius: 4px;
        margin-bottom: 10px;
    }

    @keyframes shimmer {
        0% { background-position: 100% 0; }
        100% { background-position: -100% 0; }
    }

    /* Disclaimer */
    .disclaimer {
        margin-top: 14px;
        font-size: 0.8rem;
        color: #94a3b8;
        border-left: 3px solid #2563eb;
        padding-left: 10px;
    }

    .footer {
        text-align: center;
        color: #2563eb;
        font-size: 0.85rem;
        margin-top: 2rem;
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
        lang_code = LANGUAGE_MAP.get(language, "en")

        # ---- Loading skeleton (perceived speed boost)
        with st.container():
            st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)
            st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)
            st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)

        start = time.time()
        answer = generate_answer(query, language=lang_code)
        latency = round(time.time() - start, 2)

        # -----------------------------
        # Output
        # -----------------------------
        st.markdown("### Generated Insight")

        st.markdown(
            f"""
            <div class="confidence-badge">
                Answer grounded in multiple independent sources • Generated in {latency}s
            </div>
            <div class="answer-card">
                {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------
        # Disclaimer
        # -----------------------------
        st.markdown(
            """
            <div class="disclaimer">
                <strong>Disclaimer</strong><br>
                This insight is generated using publicly available startup, policy,
                and funding data processed via an AI-powered retrieval system.
                The information provided is for <em>research and informational purposes only</em>
                and should not be considered financial, legal, or investment advice.
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# How it works
# -----------------------------
with st.expander("How AiVerse works"):
    st.write(
        """
        AiVerse is a Retrieval-Augmented Generation (RAG) system that ingests
        startup, funding, and investor data, retrieves relevant evidence,
        and synthesizes analyst-style insights grounded in real sources.
        """
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "<div class='footer'>© 2025 AiVerse | Powered by RAG & Open-Source AI</div>",
    unsafe_allow_html=True
)
