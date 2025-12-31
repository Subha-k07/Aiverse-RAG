import streamlit as st
from rag.generator import generate_answer

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AiVerse – AI Investment Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# THEME + CSS (STABLE & MINIMAL)
# -------------------------------------------------
st.markdown("""
<style>

/* ----- GLOBAL ----- */
.stApp {
    background-color: #ffffff;
    color: #0f172a;
}

.main .block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ----- HERO ----- */
.hero {
    background: linear-gradient(180deg, #e0f2fe, #ffffff);
    border-radius: 22px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2.5rem;
}

.hero h1 {
    color: #1d4ed8;
    font-size: 2.4rem;
    font-weight: 700;
}

.hero p {
    color: #334155;
    font-size: 1.05rem;
}

/* ----- RADIO (FIXED) ----- */
[data-testid="stRadio"] label {
    opacity: 1 !important;
}

[data-testid="stRadio"] span {
    color: #1e3a8a !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}

[data-testid="stRadio"] input:checked + div span {
    color: #2563eb !important;
    font-weight: 700 !important;
}

/* ----- SUGGESTED BUTTONS ----- */
div.stButton > button {
    background-color: #f0f9ff !important;
    color: #1d4ed8 !important;
    border: 2px solid #3b82f6 !important;
    border-radius: 16px;
    height: 90px;
    width: 100%;
    font-size: 0.95rem;
    font-weight: 500;
    white-space: normal;
}

div.stButton > button:hover {
    background-color: #e0f2fe !important;
}

/* ----- INPUT ----- */
input {
    background-color: #ffffff !important;
    border: 2px solid #93c5fd !important;
    border-radius: 14px !important;
    color: #0f172a !important;
}

input:focus {
    border-color: #2563eb !important;
}

/* ----- ANSWER CARD ----- */
.answer-card {
    background-color: #f8fafc;
    color: #0f172a;
    border: 2px solid #60a5fa;
    border-radius: 18px;
    padding: 22px;
    margin-top: 1.8rem;
    font-size: 0.95rem;
    line-height: 1.65;
}

/* ----- DISCLAIMER ----- */
.disclaimer {
    margin-top: 16px;
    font-size: 0.8rem;
    color: #475569;
    border-left: 4px solid #3b82f6;
    padding-left: 12px;
}

/* ----- FOOTER ----- */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.8rem;
    margin-top: 3rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>AiVerse – AI Investment Intelligence Analyst</h1>
    <p>Source-grounded investment insights from fragmented startup & funding data</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LANGUAGE SETUP
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
    options=list(LANGUAGE_MAP.keys()),
    horizontal=True
)

lang_code = LANGUAGE_MAP[language]

# -------------------------------------------------
# SUGGESTED QUESTIONS (ALL LANGS — NO KEYERROR)
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
    "te": [
        "భారతదేశంలో ప్రారంభ దశ AI స్టార్టప్‌లలో ఎవరు పెట్టుబడి పెడుతున్నారు?",
        "భారతీయ ఫిన్‌టెక్ స్టార్టప్‌లలో ఏ పెట్టుబడి ధోరణులు కనిపిస్తున్నాయి?",
        "గత 2 సంవత్సరాల్లో సమాన స్టార్టప్‌లలో పెట్టుబడి పెట్టిన VCs ఎవరు?",
        "ఫండింగ్ పొందిన స్టార్టప్‌లకు బలమైన PMF సంకేతాలు ఏమిటి?",
    ],
    "ml": [
        "ഇന്ത്യയിലെ പ്രാരംഭ ഘട്ട AI സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിക്കുന്നവർ ആരെല്ലാം?",
        "ഇന്ത്യൻ ഫിൻടെക് സ്റ്റാർട്ടപ്പുകളിൽ ഉയർന്ന് വരുന്ന നിക്ഷേപ പ്രവണതകൾ എന്തെല്ലാം?",
        "കഴിഞ്ഞ 2 വർഷങ്ങളിൽ സമാന സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിച്ച VCs ആരെല്ലാം?",
        "ഫണ്ടിംഗ് ലഭിച്ച സ്റ്റാർട്ടപ്പുകൾക്ക് ശക്തമായ PMF സൂചനകൾ എന്തെല്ലാം?",
    ],
    "kn": [
        "ಭಾರತದ ಆರಂಭಿಕ ಹಂತದ AI ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಯಾರು ಹೂಡಿಕೆ ಮಾಡುತ್ತಿದ್ದಾರೆ?",
        "ಭಾರತೀಯ ಫಿನ್‌ಟೆಕ್ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಯಾವ ಹೂಡಿಕೆ ಪ್ರವೃತ್ತಿಗಳು ಕಾಣಿಸುತ್ತಿವೆ?",
        "ಕಳೆದ 2 ವರ್ಷಗಳಲ್ಲಿ ಸಮಾನ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಿದ VCs ಯಾರು?",
        "ಹೂಡಿಕೆ ಪಡೆದ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಿಗೆ ಬಲವಾದ PMF ಸೂಚನೆಗಳು ಯಾವುವು?",
    ],
}

# -------------------------------------------------
# SUGGESTED UI
# -------------------------------------------------
st.markdown("## Suggested intelligence queries")

cols = st.columns(2)
selected_question = None

questions = SUGGESTED_QUESTIONS.get(lang_code, SUGGESTED_QUESTIONS["en"])

for i, q in enumerate(questions):
    with cols[i % 2]:
        if st.button(q):
            selected_question = q

# -------------------------------------------------
# QUERY INPUT
# -------------------------------------------------
query = st.text_input(
    "Enter your question",
    value=selected_question or "",
    placeholder="Ask about investors, funding trends, or startup signals..."
)

# -------------------------------------------------
# ANSWER
# -------------------------------------------------
if st.button("Get Answer") and query:
    with st.spinner("Analyzing sources…"):
        answer = generate_answer(query, lang_code)

    st.markdown(
        f"<div class='answer-card'>{answer}</div>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="disclaimer">
        Generated using a Retrieval-Augmented Generation (RAG) system over public startup,
        funding, and policy documents. For research purposes only.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("How the RAG model works"):
        st.markdown("""
        • Retrieves relevant startup & funding documents  
        • Ranks content using semantic similarity  
        • Generates answers strictly from retrieved sources  
        • Ensures grounded, explainable insights
        """)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    "<div class='footer'>© 2025 AiVerse · Retrieval-Augmented Intelligence</div>",
    unsafe_allow_html=True
)
