import streamlit as st
from rag.generator import generate_answer

st.set_page_config(
    page_title="AiVerse RAG",
    page_icon="🧠",
    layout="centered"
)

# Header
st.markdown(
    "<h1 style='color:#2563eb;'>AiVerse – Intelligent Policy Assistant</h1>",
    unsafe_allow_html=True
)

st.caption("Ask questions from policy documents using AI-powered retrieval")

# Language selector
language = st.radio(
    "Select language",
    ["English", "தமிழ்", "हिन्दी", "తెలుగు", "മലയാളം", "ಕನ್ನಡ"],
    horizontal=True
)

query = st.text_input(
    "Enter your question",
    placeholder="Type your question here..."
)

if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = generate_answer(query, language=language)
        st.markdown("### 📌 Answer")
        st.write(answer)
