import time
import streamlit as st
from rag.generator import generate_answer

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AiVerse – AI Investment Intelligence",
    page_icon="🌊",
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
# Suggested Questions (per language)
# -----------------------------
SUGGESTED_QUESTIONS = {
    "en": [
        "Which investors actively fund early-stage AI startups in India?",
        "What funding trends are emerging in Indian FinTech startups?",
        "Which VCs have invested in similar startups over the last 2 years?",
        "What signals indicate strong product–market fit for funded startups?"
    ],
    "hi": [
        "भारत में शुरुआती AI स्टार्टअप्स में सक्रिय निवेशक कौन हैं?",
        "भारतीय फिनटेक स्टार्टअप्स में उभरते निवेश रुझान क्या हैं?",
        "पिछले 2 वर्षों में समान स्टार्टअप्स में किन VCs ने निवेश किया है?",
        "फंड प्राप्त स्टार्टअप्स में मजबूत प्रोडक्ट–मार्केट फिट के संकेत क्या हैं?"
    ],
    "ta": [
        "இந்தியாவில் ஆரம்ப நிலை AI ஸ்டார்ட்அப்களில் முதலீடு செய்யும் முதலீட்டாளர்கள் யார்?",
        "இந்திய FinTech ஸ்டார்ட்அப்களில் உருவாகும் நிதி போக்குகள் என்ன?",
        "கடந்த 2 ஆண்டுகளில் இதே போன்ற ஸ்டார்ட்அப்களில் எந்த VCs முதலீடு செய்துள்ளனர்?",
        "நிதி பெற்ற ஸ்டார்ட்அப்களில் வலுவான தயாரிப்பு–சந்தை பொருத்தம் எவ்வாறு அறியலாம்?"
    ],
    "te": [
        "భారతదేశంలో ప్రారంభ దశ AI స్టార్టప్‌లకు పెట్టుబడి పెట్టే ఇన్వెస్టర్లు ఎవరు?",
        "భారతీయ ఫిన్‌టెక్ స్టార్టప్‌లలో కొత్త ఫండింగ్ ధోరణులు ఏమిటి?",
        "గత 2 సంవత్సరాల్లో సమాన స్టార్టప్‌లలో పెట్టుబడి పెట్టిన VCs ఎవరు?",
        "ఫండింగ్ పొందిన స్టార్టప్‌లలో బలమైన ప్రోడక్ట్–మార్కెట్ ఫిట్ సంకేతాలు ఏమిటి?"
    ],
    "ml": [
        "ഇന്ത്യയിലെ ആരംഭ ഘട്ട AI സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിക്കുന്നവർ ആരെല്ലാം?",
        "ഇന്ത്യൻ ഫിൻടെക് സ്റ്റാർട്ടപ്പുകളിലെ പുതിയ ഫണ്ടിംഗ് പ്രവണതകൾ എന്തൊക്കെയാണ്?",
        "കഴിഞ്ഞ 2 വർഷങ്ങളിൽ സമാന സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിച്ച VCs ആരെല്ലാം?",
        "ഫണ്ടിംഗ് നേടിയ സ്റ്റാർട്ടപ്പുകളിൽ ശക്തമായ പ്രോഡക്ട്–മാർക്കറ്റ് ഫിറ്റ് സൂചനകൾ എന്താണ്?"
    ],
    "kn": [
        "ಭಾರತದಲ್ಲಿ ಪ್ರಾರಂಭಿಕ ಹಂತದ AI ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಿಗೆ ಹೂಡಿಕೆ ಮಾಡುವ ಹೂಡಿಕೆದಾರರು ಯಾರು?",
        "ಭಾರತೀಯ ಫಿನ್‌ಟೆಕ್ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಉದಯಿಸುತ್ತಿರುವ ಹೂಡಿಕೆ ಪ್ರವೃತ್ತಿಗಳು ಯಾವುವು?",
        "ಕಳೆದ 2 ವರ್ಷಗಳಲ್ಲಿ ಸಮಾನ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಿದ VCs ಯಾರು?",
        "ಹೂಡಿಕೆ ಪಡೆದ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಬಲವಾದ ಉತ್ಪನ್ನ–ಮಾರುಕಟ್ಟೆ ಹೊಂದಾಣಿಕೆಯ ಸೂಚನೆಗಳು ಯಾವುವು?"
    ]
}

# -----------------------------
# Session State
# -----------------------------
if "query" not in st.session_state:
    st.session_state.query = ""

# -----------------------------
# OCEAN THEME CSS (FINAL)
# -----------------------------
st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background: #ffffff;
    color: #0f172a;
    font-family: "Inter", sans-serif;
}

/* Animated wave header */
.wave-header {
    background: linear-gradient(180deg, #e0f2fe, #ffffff);
    border-radius: 18px;
    padding: 40px 30px;
    text-align: center;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.wave-header::after {
    content: "";
    position: absolute;
    width: 200%;
    height: 120px;
    left: -50%;
    bottom: -60px;
    background: radial-gradient(circle at 50% 50%, #38bdf8 0%, transparent 70%);
    animation: wave 8s linear infinite;
    opacity: 0.25;
}

@keyframes wave {
    from { transform: translateX(0); }
    to { transform: translateX(50%); }
}

/* Titles */
.title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #2563eb;
}

.subtitle {
    color: #334155;
    font-size: 0.95rem;
    margin-top: 6px;
}

/* Radio */
label {
    color: #0f172a !important;
}

/* Suggested buttons */
div.stButton > button {
    background: #f0f9ff !important;
    color: #2563eb !important;
    border: 1.5px solid #2563eb !important;
    border-radius: 14px;
    height: 92px;
    font-weight: 500;
    white-space: normal;
}

div.stButton > button:hover {
    background: #e0f2fe !important;
}

/* Input */
input {
    background: #f8fafc !important;
    color: #0f172a !important;
    border: 1px solid #2563eb !important;
    border-radius: 10px !important;
}

/* Answer card */
.answer-card {
    background: #f0f9ff;
    border: 1px solid #2563eb;
    border-radius: 14px;
    padding: 20px;
    margin-top: 14px;
    color: #0f172a;
}

/* Badge */
.confidence-badge {
    display: inline-block;
    color: #2563eb;
    font-size: 0.75rem;
    border: 1px solid #2563eb;
    padding: 4px 10px;
    border-radius: 999px;
    margin-bottom: 10px;
}

/* Disclaimer */
.disclaimer {
    font-size: 0.8rem;
    color: #334155;
    border-left: 4px solid #38bdf8;
    padding-left: 12px;
    margin-top: 18px;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.8rem;
    margin-top: 32px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="wave-header">
    <div class="title">AiVerse – AI Investment Intelligence Analyst</div>
    <div class="subtitle">
        Source-grounded investment insights from fragmented startup & funding data
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Language Selector
# -----------------------------
language = st.radio(
    "Select language",
    list(LANGUAGE_MAP.keys()),
    horizontal=True
)

lang_code = LANGUAGE_MAP[language]
questions = SUGGESTED_QUESTIONS[lang_code]

# -----------------------------
# Suggested Queries
# -----------------------------
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

# -----------------------------
# Query Input
# -----------------------------
query = st.text_input(
    "Enter your question",
    value=st.session_state.query,
    placeholder="Ask about investors, funding trends, or startup signals…"
)

# -----------------------------
# Submit
# -----------------------------
if st.button("Get Answer"):
    if query.strip():
        start = time.time()
        answer = generate_answer(query, language=lang_code)
        latency = round(time.time() - start, 2)

        st.markdown("### Generated Insight")

        st.markdown(f"""
            <div class="confidence-badge">
                Grounded in multiple sources · {latency}s
            </div>
            <div class="answer-card">
                {answer}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="disclaimer">
                <strong>Disclaimer</strong><br>
                Generated using a Retrieval-Augmented Generation (RAG) system over
                public startup, funding, and policy documents.
                For research and informational purposes only.
            </div>
        """, unsafe_allow_html=True)

# -----------------------------
# How RAG Works
# -----------------------------
with st.expander("How the RAG model works"):
    st.write("""
    • Your query is translated (if needed) into English  
    • Relevant documents are retrieved using semantic search  
    • Evidence is synthesized into an analyst-style insight  
    • Citations are preserved to ensure traceability
    """)

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    "<div class='footer'>© 2025 AiVerse · Retrieval-Augmented Intelligence</div>",
    unsafe_allow_html=True
)
