import streamlit as st
from rag.generator import generate_answer

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="AiVerse – AI Investment Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# FORCE OVERRIDE STREAMLIT STYLES
# -------------------------------------------------
st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */
    .stApp {
        background-color: #ffffff;
        color: #0f172a;
    }

    .main .block-container {
        max-width: 1100px;
        padding: 2rem;
    }

    /* ---------- HERO ---------- */
    .hero {
        background: linear-gradient(135deg, #e0f2fe, #f8fafc);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        margin-bottom: 2.5rem;
    }

    .hero h1 {
        color: #1d4ed8;
        font-size: 2.3rem;
        font-weight: 700;
    }

    .hero p {
        color: #334155;
        font-size: 1rem;
    }

    /* ---------- RADIO (CRITICAL FIX) ---------- */
    div[role="radiogroup"] label {
        opacity: 1 !important;
    }

    div[role="radiogroup"] label span {
        color: #0f172a !important;   /* DARK TEXT */
        font-size: 1rem !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    div[role="radiogroup"] input:checked + div span {
        color: #1d4ed8 !important;   /* BLUE WHEN SELECTED */
        font-weight: 700 !important;
    }

    /* ---------- BUTTONS ---------- */
    div.stButton > button {
        background-color: #f8fafc !important;
        color: #1d4ed8 !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 14px;
        height: 90px;
        width: 100%;
        font-size: 0.95rem;
        font-weight: 500;
        white-space: normal;
    }

    div.stButton > button:hover {
        background-color: #e0f2fe !important;
    }

    /* ---------- ANSWER CARD ---------- */
    .answer-card {
        background-color: #f8fafc;
        color: #0f172a;
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 20px;
        margin-top: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ---------- DISCLAIMER ---------- */
    .disclaimer {
        margin-top: 16px;
        font-size: 0.8rem;
        color: #334155;
        border-left: 4px solid #3b82f6;
        padding-left: 12px;
    }

    /* ---------- FOOTER ---------- */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 3rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>AiVerse – AI Investment Intelligence Analyst</h1>
        <p>Source-grounded investment insights from fragmented startup & funding data</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# LANGUAGE
# -------------------------------------------------
LANGUAGE_MAP = {
    "English": "en",
    "தமிழ்": "ta",
    "हिन्दी": "hi",
    "తెలుగు": "te",
    "മലയാളം": "ml",
    "ಕನ್ನಡ": "kn",
}

language = st.radio(
    "Select language",
    list(LANGUAGE_MAP.keys()),
    horizontal=True
)

# -------------------------------------------------
# SUGGESTED QUESTIONS
# -------------------------------------------------
SUGGESTED_QUESTIONS = {
    "en": [
        "Which investors actively fund early-stage AI startups in India?",
        "What funding trends are emerging in Indian FinTech startups?",
        "Which VCs have invested in similar startups over the last 2 years?",
        "What signals indicate strong product–market fit for funded startups?",
    ],
    "ta": [
        "இந்தியாவில் ஆரம்ப கட்ட AI ஸ்டார்ட்அப்களில் முதலீடு செய்பவர்கள் யார்?",
        "இந்திய FinTech ஸ்டார்ட்அப்களில் உருவாகும் முதலீட்டு போக்குகள் என்ன?",
        "கடந்த 2 ஆண்டுகளில் ஒத்த ஸ்டார்ட்அப்களில் முதலீடு செய்த VCs யார்?",
        "நிதி பெற்ற ஸ்டார்ட்அப்களுக்கு வலுவான PMF அறிகுறிகள் என்ன?",
    ],
    "hi": [
        "भारत में शुरुआती AI स्टार्टअप्स में निवेश करने वाले कौन हैं?",
        "भारतीय FinTech स्टार्टअप्स में उभरते निवेश रुझान क्या हैं?",
        "पिछले 2 वर्षों में समान स्टार्टअप्स में किन VCs ने निवेश किया?",
        "फंडेड स्टार्टअप्स में मजबूत PMF के संकेत क्या हैं?",
    ],
}

lang_code = LANGUAGE_MAP[language]

st.markdown("## Suggested intelligence queries")

cols = st.columns(2)
selected = None
for i, q in enumerate(SUGGESTED_QUESTIONS[lang_code]):
    with cols[i % 2]:
        if st.button(q):
            selected = q

# -------------------------------------------------
# QUESTION INPUT
# -------------------------------------------------
question = st.text_input(
    "Enter your question",
    value=selected if selected else ""
)

# -------------------------------------------------
# ANSWER
# -------------------------------------------------
if st.button("Get Answer") and question:
    with st.spinner("Analyzing sources…"):
        answer = generate_answer(question, lang_code)

    st.markdown(
        f"<div class='answer-card'>{answer}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="disclaimer">
        Generated using a Retrieval-Augmented Generation (RAG) system over public
        startup, funding, and policy documents.
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("How the RAG model works"):
        st.markdown(
            """
            • Retrieves relevant startup & funding documents  
            • Ranks context using semantic similarity  
            • Generates answers strictly from retrieved sources  
            • Preserves grounding & citations
            """
        )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    "<div class='footer'>© 2025 AiVerse · Retrieval-Augmented Intelligence</div>",
    unsafe_allow_html=True
)
