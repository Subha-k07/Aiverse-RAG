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
        "இந்திய FinTech ஸ்டார்ட்அப்புகளில் புதிய முதலீட்டு போக்குகள் என்ன?",
        "கடந்த 2 ஆண்டுகளில் இதே மாதிரியான ஸ்டார்ட்அப்புகளில் முதலீடு செய்த VCs யார்?",
        "முதலீடு பெற்ற ஸ்டார்ட்அப்புகளில் தயாரிப்பு–மார்க்கெட் பொருத்தம் காட்டும் சிக்னல்கள் என்ன?"
    ],
    "hi": [
        "भारत में शुरुआती चरण के AI स्टार्टअप्स में निवेश करने वाले निवेशक कौन हैं?",
        "भारतीय FinTech स्टार्टअप्स में उभरते फंडिंग ट्रेंड्स क्या हैं?",
        "पिछले 2 वर्षों में समान स्टार्टअप्स में किन VCs ने निवेश किया है?",
        "फंड प्राप्त स्टार्टअप्स में मजबूत प्रोडक्ट–मार्केट फिट के संकेत क्या हैं?"
    ],
    "te": [
        "భారతదేశంలో ప్రారంభ దశ AI స్టార్టప్‌లలో పెట్టుబడి పెట్టే ఇన్వెస్టర్లు ఎవరు?",
        "భారతీయ FinTech స్టార్టప్‌లలో కొత్త పెట్టుబడి ధోరణులు ఏమిటి?",
        "గత 2 సంవత్సరాలలో సమానమైన స్టార్టప్‌లలో పెట్టుబడి పెట్టిన VCs ఎవరు?",
        "నిధులు పొందిన స్టార్టప్‌లలో బలమైన ప్రొడక్ట్–మార్కెట్ ఫిట్ సంకేతాలు ఏమిటి?"
    ],
    "ml": [
        "ഇന്ത്യയിലെ പ്രാരംഭ ഘട്ട AI സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിക്കുന്ന നിക്ഷേപകർ ആരെല്ലാം?",
        "ഇന്ത്യൻ FinTech സ്റ്റാർട്ടപ്പുകളിൽ പുതിയ ഫണ്ടിംഗ് ട്രെൻഡുകൾ എന്തൊക്കെയാണ്?",
        "കഴിഞ്ഞ 2 വർഷങ്ങളിൽ സമാന സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിച്ച VCs ആരെല്ലാം?",
        "ഫണ്ടിംഗ് ലഭിച്ച സ്റ്റാർട്ടപ്പുകളിൽ ശക്തമായ പ്രൊഡക്ട്–മാർക്കറ്റ് ഫിറ്റ് സൂചിപ്പിക്കുന്ന സിഗ്നലുകൾ എന്തൊക്കെയാണ്?"
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

    .answer-card {
        border: 1px solid #2563eb;
        background-color: #020617;
        border-radius: 10px;
        padding: 18px;
        margin-top: 1rem;
    }

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

    .skeleton {
        background: linear-gradient(90deg,#020617 25%,#0f172a 37%,#020617 63%);
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
    "<div class='subtitle'>Grounded investment insights from fragmented startup & funding data</div>",
    unsafe_allow_html=True
)

# -----------------------------
# Language Selector
# -----------------------------
language = st.radio(
    "Select language",
    list(LANGUAGE_MAP.keys()),
    horizontal=True
)

lang_code = LANGUAGE_MAP.get(language, "en")

# -----------------------------
# Suggested Queries
# -----------------------------
st.markdown("**Suggested intelligence queries**")

queries = SUGGESTED_QUERIES.get(lang_code, SUGGESTED_QUERIES["en"])
c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

for col, text in zip([c1, c2, c3, c4], queries):
    with col:
        if st.button(text):
            st.session_state.query = text

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
            <div class="confidence-badge">
                Grounded in retrieved sources • Generated in {latency}s
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
                It is intended for <em>research and analytical purposes only</em> and
                should not be treated as financial or investment advice.
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# How the RAG model works
# -----------------------------
with st.expander("How the RAG model works"):
    st.write(
        """
        1. The user query is converted into an embedding and matched against a FAISS
           vector index built from startup, funding, and policy documents.
        2. The retriever selects the most semantically relevant evidence chunks.
        3. The generator synthesizes an analyst-style insight strictly grounded in
           the retrieved sources.
        4. Source provenance is preserved to minimize hallucinations and improve trust.
        """
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "<div class='footer'>© 2025 AiVerse | Powered by Retrieval-Augmented Generation</div>",
    unsafe_allow_html=True
)
