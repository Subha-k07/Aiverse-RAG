import streamlit as st
from rag.generator import generate_answer

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="AiVerse RAG",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------- Custom CSS --------------------
st.markdown(
    """
    <style>
    /* Body background & text */
    .reportview-container {
        background-color: #ffffff;
        color: #1e293b;
    }

    /* Header styling */
    h1 {
        color: #2563eb;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        height: 40px;
        width: 120px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    /* Language radio buttons */
    .stRadio > label {
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- Header --------------------
st.markdown("<h1>AiVerse – Intelligent Policy Assistant</h1>", unsafe_allow_html=True)
st.caption("Ask questions from policy documents using AI-powered retrieval")

# -------------------- Language Selector --------------------
language = st.radio(
    "Select language:",
    ["English", "தமிழ்", "हिन्दी", "తెలుగు", "മലയാളം", "ಕನ್ನಡ"],
    horizontal=True
)

# -------------------- User Query Input --------------------
query = st.text_input(
    "Enter your question:",
    placeholder="Type your question here..."
)

# -------------------- Process Query --------------------
if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            try:
                answer = generate_answer(query, language=language)
                if answer:
                    st.markdown("### 📌 Answer")
                    st.success(answer)
                else:
                    st.warning("No answer found. Try rephrasing your question.")
            except Exception as e:
                st.error(f"Error: {e}")

# -------------------- Footer --------------------
st.markdown("---")
st.caption("© 2025 AiVerse | Powered by LangChain & Open-Source AI models")
