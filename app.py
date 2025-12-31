import time
import streamlit as st
from rag.generator import generate_answer

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AIVerse – AI Investment Intelligence",
    page_icon="📊",
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
# Suggested Queries (Multilingual)
# -----------------------------
SUGGESTED_QUERIES = {
    "en": [
        "Which investors actively fund early-stage AI startups in India?",
        "What funding trends are emerging in Indian FinTech startups?",
        "Which VCs have invested in similar startups over the last 2 years?",
        "What signals indicate strong product–market fit for funded startups?"
    ],
    "ta": [
        "இந்தியாவில் ஆரம்ப நிலை AI ஸ்டார்ட்அப்புகளில் முதலீடு செய்பவர்கள் யார்?",
        "இந்திய FinTech ஸ்டார்ட்அப்புகளில் உருவாகும் முதலீட்டு போக்குகள் என்ன?",
        "கடந்த 2 ஆண்டுகளில் இதே மாதிரியான ஸ்டார்ட்அப்புகளில் முதலீடு செய்த VCs யார்?",
        "முதலீடு பெற்ற ஸ்டார்ட்அப்புகளில் வலுவான தயாரிப்பு–மார்க்கெட் பொருத்தம் சிக்னல்கள் என்ன?"
    ],
    "te": [
        "భారతదేశంలో ప్రారంభ దశ AI స్టార్టప్‌లలో పెట్టుబడి పెట్టే ఇన్వెస్టర్లు ఎవరు?",
        "భారతీయ FinTech స్టార్టప్‌లలో కొత్త ఫండింగ్ ధోరణులు ఏమిటి?",
        "గత 2 సంవత్సరాలలో సమానమైన స్టార్టప్‌లలో పెట్టుబడి పెట్టిన VCs ఎవరు?",
        "ఫండింగ్ పొందిన స్టార్టప్‌లలో బలమైన ప్రొడక్ట్–మార్కెట్ ఫిట్ సంకేతాలు ఏమిటి?"
    ],
    "ml": [
        "ഇന്ത്യയിലെ പ്രാരംഭ ഘട്ട AI സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിക്കുന്ന നിക്ഷേപകർ ആരെല്ലാം?",
        "ഇന്ത്യൻ FinTech സ്റ്റാർട്ടപ്പുകളിൽ ഉയർന്നുവരുന്ന ഫണ്ടിംഗ് ട്രെൻഡുകൾ എന്തൊക്കെയാണ്?",
        "കഴിഞ്ഞ 2 വർഷങ്ങളിൽ സമാന സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിച്ച VCs ആരെല്ലാം?",
        "ഫണ്ടിംഗ് ലഭിച്ച സ്റ്റാർട്ടപ്പുകളിൽ ശക്തമായ പ്രൊഡക്ട്–മാർക്കറ്റ് ഫിറ്റ് സൂചകങ്ങൾ എന്തൊക്കെയാണ്?"
    ],
    "kn": [
        "ಭಾರತದಲ್ಲಿ ಪ್ರಾರಂಭಿಕ ಹಂತದ AI ಸ್ಟಾರ್ಟಪ್‌ಗಳಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡುವ ಹೂಡಿಕೆದಾರರು ಯಾರು?",
        "ಭಾರತೀಯ FinTech ಸ್ಟಾರ್ಟಪ್‌ಗಳಲ್ಲಿ ಹೊಸ ಹೂಡಿಕೆ ಪ್ರವೃತ್ತಿಗಳು ಯಾವುವು?",
        "ಕಳೆದ 2 ವರ್ಷಗಳಲ್ಲಿ ಸಮಾನ ಸ್ಟಾರ್ಟಪ್‌ಗಳಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಿದ VCs ಯಾರು?",
        "ಹೂಡಿಕೆ ಪಡೆದ ಸ್ಟಾರ್ಟಪ್‌ಗಳಲ್ಲಿ ಬಲವಾದ ಪ್ರೊಡಕ್ಟ್–ಮಾರ್ಕೆಟ್ ಫಿಟ್ ಸೂಚನೆಗಳು ಯಾವುವು?"
    ]
}

# -----------------------------
# Session State
# -----------------------------
if "query" not in st.session_state:
    st.session_state.query = ""

# -----------------------------
# Global Styles (WHITE + BLUE)
# -----------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #f8fafc;
        color: #0f172a;
    }

    .title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1d4ed8;
    }

    .subtitle {
        color: #475569;
        margin-bottom: 1.5rem;
    }

    div.stButton > button {
        background-color: #ffffff !important;
        color: #1d4ed8 !important;
        border: 1.5px solid #1d4ed8 !important;
        border-radius: 10px;
        height: 90px;
        width: 100%;
        font-size: 0.9rem;
        font-weight: 500;
        white-space: normal;
    }

    div.stButton > button:hover {
        background-color: #eff6ff !important;
    }

    .answer-card {
        border: 1px solid #c7d2fe;
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        margin-top: 1rem;
        color: #0f172a;
    }

    .confidence-badge {
        display: inline-block;
        background-color: #eff6ff;
        border: 1px solid #93c5fd;
        color: #1d4ed8;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 999px;
        margin-bottom: 8px;
    }

    .skeleton {
        background: linear-gradient(
            90deg,
            #e5e7eb 25%,
            #f1f5f9 37%,
            #e5e7eb 63%
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

    .disclaimer {
        margin-top: 16px;
        font-size: 0.8rem;
        color: #475569;
        border-left: 3px solid #1d4ed8;
        padding-left: 10px;
        background-color: #f8fafc;
    }

    .footer {
        text-align: center;
        color: #64748b;
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
    "<div class='subtitle'>Reliable, source-grounded insights from fragmented startup & funding data</div>",
    unsafe_allow_html=True
)

# -----------------------------
# Language Selector
# -----------------------------
language = st.radio("Select language", list(LANGUAGE_MAP.keys()), horizontal=True)
lang_code = LANGUAGE_MAP.get(language, "en")

# -----------------------------
# Suggested Queries
# -----------------------------
st.markdown("**Suggested intelligence queries**")
queries = SUGGESTED_QUERIES.get(lang_code, SUGGESTED_QUERIES["en"])

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

for col, q in zip([c1, c2, c3, c4], queries):
    with col:
        if st.button(q):
            st.session_state.query = q

# -----------------------------
# Query Input
# -----------------------------
query = st.text_input(
    "Enter your question",
    value=st.session_state.query,
    placeholder="Ask about investors, funding patterns, or startup intelligence..."
)

# -----------------------------
# Submit
# -----------------------------
if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        for _ in range(3):
            st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)

        start = time.time()
        answer = generate_answer(query, language=lang_code)
        latency = round(time.time() - start, 2)

        st.markdown("### Generated Insight")
        st.markdown(
            f"""
            <div class="confidence-badge">
                Evidence-grounded RAG output • Generated in {latency}s
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
                This output is generated using a Retrieval-Augmented Generation (RAG)
                system over publicly available startup, funding, and policy documents.
                It is intended strictly for research and analytical purposes.
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# How RAG Works
# -----------------------------
with st.expander("How the RAG model works"):
    st.write(
        """
        • User queries are embedded and matched against a vector index of startup,
          investor, funding, and policy documents.  
        • The retriever selects the most relevant evidence chunks.  
        • The generator synthesizes analyst-style insights strictly grounded in those sources.  
        • Source provenance is preserved to reduce hallucinations and improve trust.
        """
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("<div class='footer'>© 2025 AiVerse | AI Investment Intelligence via RAG</div>", unsafe_allow_html=True)
