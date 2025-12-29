import streamlit as st
from rag.generator import generate_answer

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AiVerse RAG",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
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
# UI Styles
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    .header {
        color: #2563eb;
        font-size: 2.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subheader {
        color: #1e3a8a;
        font-size: 1em;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
    }
    .stRadio>div {
        flex-direction: row;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.markdown("<div class='header'>AiVerse – Intelligent Policy Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Ask questions from policy documents using AI-powered retrieval</div>", unsafe_allow_html=True)

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
    placeholder="Type your question here..."
)

# -----------------------------
# Submit Button
# -----------------------------
if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            lang_code = LANGUAGE_MAP.get(language, "en")
            answer = generate_answer(query, language=lang_code)
        st.markdown("### 📌 Answer")
        st.write(answer)
# -----------------------------
# Footer
# -----------------------------
st.markdown("---")  # horizontal separator
st.markdown(
    "<div style='text-align:center; color:#2563eb; font-size:0.85em;'>"
    "© 2025 AiVerse | Powered by LangChain & Open-Source AI models"
    "</div>",
    unsafe_allow_html=True
)
