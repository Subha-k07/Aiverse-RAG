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
# Suggested Questions (Per Language)
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
        "கடந்த 2 ஆண்டுகளில் ஒத்த ஸ்டார்ட்அப்களில் முதலீடு செய்த VC-க்கள் யார்?",
        "முதலீடு பெற்ற ஸ்டார்ட்அப்களுக்கு தயாரிப்பு-மார்க்கெட் பொருத்தத்தை குறிக்கும் அறிகுறிகள் என்ன?"
    ],
    "te": [
        "భారతదేశంలో ప్రారంభ దశ AI స్టార్టప్‌లలో పెట్టుబడి పెట్టే ఇన్వెస్టర్లు ఎవరు?",
        "భారతీయ FinTech స్టార్టప్‌లలో కొత్త ఫండింగ్ ధోరణులు ఏమిటి?",
        "గత 2 సంవత్సరాలలో సమానమైన స్టార్టప్‌లలో పెట్టుబడి పెట్టిన VCలు ఎవరు?",
        "ఫండింగ్ పొందిన స్టార్టప్‌లకు ఉత్పత్తి-మార్కెట్ ఫిట్‌ను సూచించే సంకేతాలు ఏమిటి?"
    ],
    "ml": [
        "ഇന്ത്യയിലെ പ്രാരംഭ ഘട്ട AI സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിക്കുന്നവർ ആരെല്ലാം?",
        "ഇന്ത്യൻ FinTech സ്റ്റാർട്ടപ്പുകളിൽ പുതിയ ഫണ്ടിംഗ് പ്രവണതകൾ എന്തെല്ലാം?",
        "കഴിഞ്ഞ 2 വർഷങ്ങളിൽ സമാന സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിച്ച VCകൾ ആരെല്ലാം?",
        "ഫണ്ടിംഗ് ലഭിച്ച സ്റ്റാർട്ടപ്പുകളിൽ ഉൽപ്പന്ന-മാർക്കറ്റ് ഫിറ്റ് സൂചിപ്പിക്കുന്ന ലക്ഷണങ്ങൾ എന്തെല്ലാം?"
    ],
    "kn": [
        "ಭಾರತದಲ್ಲಿ ಆರಂಭಿಕ ಹಂತದ AI ಸ್ಟಾರ್ಟಪ್‌ಗಳಿಗೆ ಹೂಡಿಕೆ ಮಾಡುವ ಹೂಡಿಕೆದಾರರು ಯಾರು?",
        "ಭಾರತೀಯ FinTech ಸ್ಟಾರ್ಟಪ್‌ಗಳಲ್ಲಿ ಹೊಸ ಹೂಡಿಕೆ ಪ್ರವೃತ್ತಿಗಳು ಯಾವುವು?",
        "ಕಳೆದ 2 ವರ್ಷಗಳಲ್ಲಿ ಸಮಾನ ಸ್ಟಾರ್ಟಪ್‌ಗಳಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಿದ VC ಗಳು ಯಾರು?",
        "ಹೂಡಿಕೆ ಪಡೆದ ಸ್ಟಾರ್ಟಪ್‌ಗಳಲ್ಲಿ ಉತ್ಪನ್ನ-ಮಾರುಕಟ್ಟೆ ಹೊಂದಾಣಿಕೆಯನ್ನು ಸೂಚಿಸುವ ಸಂಕೇತಗಳು ಯಾವುವು?"
    ]
}

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "query" not in st.session_state:
    st.session_state.query = ""

# --------------------------------------------------
# Ocean Theme CSS (STREAMLIT-SAFE)
# --------------------------------------------------
st.markdown("""
<style>

/* Force white page */
.stApp {
    background-color: #ffffff;
}

/* Hide Streamlit chrome */
header, footer { visibility: hidden; }

/* Master container */
.ocean-shell {
    background: linear-gradient(180deg, #e6f3ff, #ffffff);
    border-radius: 18px;
    padding: 32px;
    margin-top: 20px;
}

/* Title */
.ocean-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #0b5ed7;
}

/* Subtitle */
.ocean-subtitle {
    color: #1e40af;
    margin-bottom: 28px;
}

/* Cards */
.ocean-card {
    background-color: #f0f8ff;
    border: 1px solid #0b5ed7;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}

/* Suggested buttons */
div[data-testid="stButton"] > button {
    background-color: #f0f8ff;
    color: #0b5ed7;
    border: 1.5px solid #0b5ed7;
    border-radius: 10px;
    padding: 14px;
    height: auto;
    font-weight: 500;
}

div[data-testid="stButton"] > button:hover {
    background-color: #e0f0ff;
}

/* Confidence badge */
.confidence {
    display: inline-block;
    border: 1px solid #0b5ed7;
    color: #0b5ed7;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.75rem;
    margin-bottom: 8px;
}

/* Skeleton loader */
.skeleton {
    height: 14px;
    background: linear-gradient(90deg, #e0f0ff 25%, #cce6ff 37%, #e0f0ff 63%);
    background-size: 400% 100%;
    animation: shimmer 1.4s ease infinite;
    border-radius: 6px;
    margin-bottom: 8px;
}

@keyframes shimmer {
    0% { background-position: 100% 0; }
    100% { background-position: -100% 0; }
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# UI START
# --------------------------------------------------
st.markdown("<div class='ocean-shell'>", unsafe_allow_html=True)

st.markdown("<div class='ocean-title'>AiVerse – AI Investment Intelligence Analyst</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='ocean-subtitle'>Source-grounded investment insights from fragmented startup & funding data</div>",
    unsafe_allow_html=True
)

# Language selector
language = st.radio(
    "Select language",
    list(LANGUAGE_MAP.keys()),
    horizontal=True
)
lang_code = LANGUAGE_MAP[language]

# Suggested Questions
st.markdown("### Suggested intelligence queries")
qs = SUGGESTED_QUESTIONS[lang_code]

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

with c1:
    if st.button(qs[0]): st.session_state.query = qs[0]
with c2:
    if st.button(qs[1]): st.session_state.query = qs[1]
with c3:
    if st.button(qs[2]): st.session_state.query = qs[2]
with c4:
    if st.button(qs[3]): st.session_state.query = qs[3]

# Query input
query = st.text_input(
    "Enter your question",
    value=st.session_state.query,
    placeholder="Ask about investors, funding trends, or startup signals..."
)

# Submit
if st.button("Get Answer"):
    if query.strip():
        st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)
        st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)

        start = time.time()
        answer = generate_answer(query, language=lang_code)
        latency = round(time.time() - start, 2)

        st.markdown(
            f"""
            <div class="ocean-card">
                <div class="confidence">Grounded in multiple sources • {latency}s</div>
                {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

# How RAG works
with st.expander("How the RAG model works"):
    st.write(
        """
        The system retrieves relevant startup, funding, and policy documents
        using semantic search. These sources are ranked, filtered, and passed
        into a language model which generates answers strictly grounded in
        retrieved evidence—reducing hallucinations and improving factual reliability.
        """
    )

st.markdown("</div>", unsafe_allow_html=True)
