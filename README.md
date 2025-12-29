AiVerse is an AI-powered Retrieval-Augmented Generation (RAG) application that enables users to ask natural-language questions over large collections of policy, startup, and governance documents.
It retrieves the most relevant information using vector search and generates grounded, source-backed answers through an intuitive web interface.
This project was built as part of a hackathon / learning initiative to demonstrate a production-style RAG pipeline using open-source tools.
Key Features
1.Semantic Search (FAISS) for fast and accurate document retrieval
2.Retrieval-Augmented Generation (RAG) architecture
3.Multi-language query support (English, Hindi, Tamil, Telugu, Malayalam, Kannada)
4.Source-aware answers derived from ingested documents
5.Clean, professional UI (White & Blue theme)
6.Cloud deployment using Streamlit Cloud
7.Fully open-source stack
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
WORKFLOW
User Query
   ↓
Streamlit UI (app.py)
   ↓
Query Translation (deep-translator)
   ↓
FAISS Vector Search (retriever.py)
   ↓
Relevant Document Chunks
   ↓
Answer Synthesis (generator.py)
   ↓
Final Answer (with sources)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
TECHO STACK 
Frontend
Streamlit – UI & interaction
Backend / AI
LangChain – RAG pipeline
FAISS – Vector database
Sentence-Transformers – Embeddings
deep-translator – Multilingual support
Language & Tools
Python 3.10+
Hugging Face models
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
How the RAG Pipeline Works
1.Documents are ingested (PDFs, CSVs, web pages)
2.Text is cleaned and chunked
3.Chunks are converted to embeddings
4.Embeddings are stored in FAISS
5.User queries are embedded and matched
6.Top relevant chunks are retrieved
7.A final answer is synthesized from retrieved context
Open-source libraries only
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Multi-Language Support
AiVerse supports user queries in multiple Indian languages.
The flow is:
User enters query in chosen language
Query is translated to English
Retrieval happens in English
Final answer is translated back to the selected language
This enables inclusive access to policy information.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Deployment
The application is deployed using Streamlit Cloud, enabling:
Free hosting for hackathons
Direct GitHub integration
Zero DevOps overhead

Live App:
https://aiverse-rag-assistant11.streamlit.app/