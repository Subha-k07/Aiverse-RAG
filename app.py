import time
import streamlit as st
from rag.generator import generate_answer

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AiVerse – AI Investment Intelligence",
    page_icon="🌊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Language Mapping
# --------------------------------------------------
LANGUAGE_MAP = {
    "English": "en",
    "தமிழ்": "ta",
    "हिन्दी": "hi",
    "తెలుగు": "te",
    "മലയാളം": "ml",
    "ಕನ್ನಡ": "kn"
}

# --------------------------------------------------
# Suggested Questions (ALL languages fixed)
# --------------------------------------------------
SUGGESTED_QUESTIONS = {
    "en": [
        "Which investors actively fund early-stage AI startups in India?",
        "What funding trends are emerging in Indian FinTech startups?",
        "Which VCs have invested in similar startups over the last 2 years?",
        "What signals indicate strong product–market fit for funded startups?"
    ],
    "ta": [
        "இந்தியாவில் ஆரம்ப நிலை AI ஸ்டார்ட்அப்களில் முதலீடு செய்யும் முதலீட்டாளர்கள் யார்?",
        "இந்திய FinTech ஸ்டார்ட்அப்களில் உருவாகும் முதலீட்டு போக்குகள் என்ன?",
        "கடந்த 2 ஆண்டுகளில் ஒத்த ஸ்டார்ட்அப்களில் முதலீடு செய்த VCs யார்?",
        "நிதியுதவி பெற்ற ஸ்டார்ட்அப்களில் தயாரிப்பு–சந்தை பொருத்தத்தை காட்டும் அறிகுறிகள் என்ன?"
    ],
    "hi": [
        "भारत में शुरुआती AI स्टार्टअप्स में सक्रिय निवेशक कौन हैं?",
        "भारतीय फिनटेक स्टार्टअप्स में उभरते निवेश रुझान क्या हैं?",
        "पिछले 2 वर्षों में समान स्टार्टअप्स में किन VCs ने निवेश किया है?",
        "फंड प्राप्त स्टार्टअप्स में मजबूत प्रोडक्ट–मार्केट फिट के संकेत क्या हैं?"
    ],
    "te": [
        "భారతదేశంలో ప్రారంభ దశ AI స్టార్టప్‌లలో పెట్టుబడి పెట్టే పెట్టుబడిదారులు ఎవరు?",
        "భారతీయ ఫిన్‌టెక్ స్టార్టప్‌లలో ఉద్భవిస్తున్న పెట్టుబడి ధోరణులు ఏమిటి?",
        "గత 2 సంవత్సరాల్లో సమానమైన స్టార్టప్‌లలో పెట్టుబడి పెట్టిన VCs ఎవరు?",
        "నిధులు పొందిన స్టార్టప్‌లలో బలమైన ప్రోడక్ట్–మార్కెట్ ఫిట్‌ను సూచించే సంకేతాలు ఏమిటి?"
    ],
    "ml": [
        "ഇന്ത്യയിലെ തുടക്കഘട്ട AI സ്റ്റാർട്ടപ്പുകളിൽ സജീവമായി നിക്ഷേപിക്കുന്നവർ ആര്?",
        "ഇന്ത്യൻ ഫിൻടെക് സ്റ്റാർട്ടപ്പുകളിൽ ഉയർന്നുവരുന്ന നിക്ഷേപ പ്രവണതകൾ എന്തൊക്കെയാണ്?",
        "കഴിഞ്ഞ 2 വർഷങ്ങളിൽ സമാന സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിച്ച VCs ആരൊക്കെയാണ്?",
        "ഫണ്ടിംഗ് ലഭിച്ച സ്റ്റാർട്ടപ്പുകളിൽ ശക്തമായ പ്രോഡക്റ്റ്–മാർക്കറ്റ് ഫിറ്റ് സൂചിപ്പിക്കുന്ന ലക്ഷണങ്ങൾ എന്തൊക്കെയാണ്?"
    ],
    "kn": [
        "ಭಾರತದಲ್ಲಿ ಆರಂಭಿಕ ಹಂತದ AI ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಿಗೆ ಸಕ್ರಿಯವಾಗಿ ಹೂಡಿಕೆ ಮಾಡುವವರು ಯಾರು?",
        "ಭಾರತೀಯ ಫಿನ್‌ಟೆಕ್ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಉದಯಿಸುತ್ತಿರುವ ಹೂಡಿಕೆ ಪ್ರವೃತ್ತಿಗಳು ಯಾವುವು?",
        "ಕಳೆದ 2 ವರ್ಷಗಳಲ್ಲಿ ಸಮಾನ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಿದ VCs ಯಾರು?",
        "ಹೂಡಿಕೆ ಪಡೆದ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಬಲವಾದ ಉತ್ಪನ್ನ–ಮಾರುಕಟ್ಟೆ ಹೊಂದಾಣಿಕೆಯನ್ನು ಸೂಚಿಸುವ ಸಂಕೇತಗಳು ಯಾವುವು?"
    ]
}

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "query" not in st.session_state:
    st.session_state.query = ""

# --------------------------------------------------
# Global Ocean Theme Styles (VISIBLE EVERYTHING)
# --------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff;
        color: #0f172a;
    }

    .hero {
        background: linear-gradient(180deg, #e0f2fe 0%, #ffffff 70%);
        padding: 3rem 2rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        text-align: center;
    }

    .title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1d4ed8;
    }

    .subtitle {
        color: #334155;
        margin-top: 0.6rem;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #eff6ff !important;
        color: #1d4ed8 !important;
        border: 1.5px solid #1d4ed8 !important;
        border-radius: 10px;
        height: 88px;
        width: 100%;
        font-size: 0.9rem;
        white-space: normal;
    }

    div.stButton > button:hover {
        background-color: #dbeafe !important;
    }

    /* Inputs */
    input {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        border: 1px solid #1d4ed8 !important;
        border-radius: 8px;
    }

    /* Answer card */
    .answer-card {
        background-color: #eff6ff;
        border-left: 4px solid #1d4ed8;
        border-radius: 10px;
        padding: 18px;
        color: #0f172a;
    }

    .confidence {
        font-size: 0.75rem;
        color: #1d4ed8;
        margin-bottom: 6px;
    }

    .disclaimer {
        margin-top: 16px;
        font-size: 0.8rem;
        color: #475569;
        border-left: 3px solid #1d4ed8;
        padding-left: 10px;
    }

    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.85rem;
        margin-top: 2.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Hero
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="title">AiVerse – AI Investment Intelligence Analyst</div>
        <div class="subtitle">
            Source-grounded investment insights from fragmented startup & funding data
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Language Selector
# --------------------------------------------------
language = st.radio(
    "Select language",
    list(LANGUAGE_MAP.keys()),
    horizontal=True
)

lang_code = LANGUAGE_MAP[language]
questions = SUGGESTED_QUESTIONS.get(lang_code, SUGGESTED_QUESTIONS["en"])

# --------------------------------------------------
# Suggested Questions
# --------------------------------------------------
st.markdown("### Suggested intelligence queries")

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

with c1:
    if st.button(questions[0]):
        st.session_state.query = questions[0]
with c2:
    if st.button(questions[1]):
        st.session_state.query = questions[1]
with c3:
    if st.button(questions[2]):
        st.session_state.query = questions[2]
with c4:
    if st.button(questions[3]):
        st.session_state.query = questions[3]

# --------------------------------------------------
# Query Input
# --------------------------------------------------
query = st.text_input(
    "Enter your question",
    value=st.session_state.query,
    placeholder="Ask about investors, funding trends, or startup signals..."
)

# --------------------------------------------------
# Submit
# --------------------------------------------------
if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        start = time.time()
        answer = generate_answer(query, language=lang_code)
        latency = round(time.time() - start, 2)

        st.markdown(
            f"""
            <div class="confidence">
                Answer grounded in multiple sources • Generated in {latency}s
            </div>
            <div class="answer-card">{answer}</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="disclaimer">
                <strong>Disclaimer</strong><br>
                Generated using a Retrieval-Augmented Generation (RAG) system over
                public startup, funding, and policy documents. For research purposes only.
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# RAG Explanation (CRISP)
# --------------------------------------------------
with st.expander("How the RAG model works"):
    st.write(
        """
        • Your query is matched against a vector database of startup & funding documents  
        • Relevant sources are retrieved using semantic similarity  
        • An analyst-style answer is synthesized **only from retrieved evidence**  
        • Citations ensure traceability and reduce hallucinations
        """
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    "<div class='footer'>© 2025 AiVerse • Retrieval-Augmented Intelligence</div>",
    unsafe_allow_html=True
)
