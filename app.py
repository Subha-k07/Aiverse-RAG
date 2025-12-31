import streamlit as st
from rag.generator import generate_answer  # keep your existing generator

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
# Global Styles (WHITE + BLUE OCEAN THEME)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #ffffff;
        color: #0f172a;
    }

    /* Main content width */
    .main .block-container {
        max-width: 1100px;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Header card */
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
        margin-bottom: 0.6rem;
    }

    .hero p {
        color: #334155;
        font-size: 1rem;
    }

    /* Section titles */
    h2 {
        color: #1e3a8a;
        font-weight: 600;
        margin-top: 2rem;
    }

    /* Suggested question buttons */
    div.stButton > button {
        background-color: #f8fafc !important;
        color: #1d4ed8 !important;
        border: 1.5px solid #3b82f6 !important;
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

    /* Radio labels – FIXED VISIBILITY */
    div[role="radiogroup"] label span {
        color: #1e3a8a !important;
        font-weight: 500 !important;
        opacity: 1 !important;
        font-size: 0.95rem;
    }

    div[role="radiogroup"] label:hover span {
        color: #2563eb !important;
    }

    div[role="radiogroup"] input:checked + div span {
        color: #1d4ed8 !important;
        font-weight: 600 !important;
    }

    /* Answer card */
    .answer-card {
        border: 1px solid #3b82f6;
        background-color: #f8fafc;
        border-radius: 16px;
        padding: 20px;
        margin-top: 1.2rem;
    }

    /* Disclaimer */
    .disclaimer {
        margin-top: 14px;
        font-size: 0.8rem;
        color: #475569;
        border-left: 3px solid #3b82f6;
        padding-left: 12px;
    }

    /* Footer */
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
# Hero Section
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
# Language Selection
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

st.caption("🌐 Multilingual intelligence · Native-language queries supported")

# -------------------------------------------------
# Suggested Questions
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
        "భారతదేశంలో ప్రారంభ దశ AI స్టార్టప్‌లలో పెట్టుబడి పెట్టేవారు ఎవరు?",
        "భారతీయ FinTech స్టార్టప్‌లలో కొత్త పెట్టుబడి ధోరణులు ఏమిటి?",
        "గత 2 సంవత్సరాల్లో సమాన స్టార్టప్‌లలో పెట్టుబడి పెట్టిన VCs ఎవరు?",
        "ఫండింగ్ పొందిన స్టార్టప్‌లకు బలమైన PMF సంకేతాలు ఏమిటి?",
    ],
    "ml": [
        "ഇന്ത്യയിലെ പ്രാരംഭ ഘട്ട AI സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിക്കുന്നവർ ആരെല്ലാം?",
        "ഇന്ത്യൻ FinTech സ്റ്റാർട്ടപ്പുകളിൽ ഉയർന്ന് വരുന്ന നിക്ഷേപ പ്രവണതകൾ എന്തൊക്കെയാണ്?",
        "കഴിഞ്ഞ 2 വർഷങ്ങളിൽ സമാന സ്റ്റാർട്ടപ്പുകളിൽ നിക്ഷേപിച്ച VCs ആരെല്ലാം?",
        "ഫണ്ടിംഗ് നേടിയ സ്റ്റാർട്ടപ്പുകൾക്ക് ശക്തമായ PMF സൂചനകൾ എന്തൊക്കെയാണ്?",
    ],
    "kn": [
        "ಭಾರತದಲ್ಲಿ ಆರಂಭಿಕ ಹಂತದ AI ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡುವವರು ಯಾರು?",
        "ಭಾರತೀಯ FinTech ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಕಾಣಿಸಿಕೊಳ್ಳುತ್ತಿರುವ ಹೂಡಿಕೆ ಪ್ರವೃತ್ತಿಗಳು ಯಾವುವು?",
        "ಕಳೆದ 2 ವರ್ಷಗಳಲ್ಲಿ ಸಮಾನ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಿದ VCs ಯಾರು?",
        "ಹೂಡಿಕೆ ಪಡೆದ ಸ್ಟಾರ್ಟ್‌ಅಪ್‌ಗಳಿಗೆ ಬಲವಾದ PMF ಸೂಚನೆಗಳು ಯಾವುವು?",
    ],
}

lang_code = LANGUAGE_MAP[language]

st.markdown("## Suggested intelligence queries")

cols = st.columns(2)
selected_question = None

for i, q in enumerate(SUGGESTED_QUESTIONS[lang_code]):
    with cols[i % 2]:
        if st.button(q):
            selected_question = q

# -------------------------------------------------
# Question Input
# -------------------------------------------------
question = st.text_input(
    "Enter your question",
    value=selected_question if selected_question else "",
    placeholder="Ask about investors, funding patterns, or startup intelligence…"
)

# -------------------------------------------------
# Generate Answer
# -------------------------------------------------
if st.button("Get Answer") and question:
    with st.spinner("Analyzing sources and generating insight…"):
        answer = generate_answer(question, lang_code)

    st.markdown(f"<div class='answer-card'>{answer}</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="disclaimer">
        <strong>Disclaimer:</strong><br>
        Generated using a Retrieval-Augmented Generation (RAG) system over public
        startup, funding, and policy documents. For research and informational purposes only.
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("How the RAG model works"):
        st.markdown(
            """
            1. Relevant startup, funding, and policy documents are retrieved  
            2. Contextual chunks are ranked using semantic similarity  
            3. The answer is generated strictly from retrieved sources  
            4. Citations are preserved for transparency
            """
        )

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown(
    "<div class='footer'>© 2025 AiVerse · Retrieval-Augmented Intelligence</div>",
    unsafe_allow_html=True
)
