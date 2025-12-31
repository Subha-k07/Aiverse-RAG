
# AiVerse – AI Investment Intelligence Analyst

AiVerse is a multilingual, Retrieval-Augmented Generation (RAG) system designed to deliver **source-grounded investment intelligence** from fragmented startup, funding, and policy data. It acts as an AI analyst that helps founders, investors, and researchers extract actionable insights from unstructured documents.

The system is optimized for hackathon and real-world use, focusing on explainability, multilingual access, and clean user experience.

---

## Problem Statement

The startup ecosystem generates vast amounts of information across funding articles, policy documents, investor reports, and news platforms. This data is:

* Highly fragmented
* Largely unstructured
* Time-consuming to analyze manually

Founders struggle to identify the right investors and trends, while VCs face difficulty synthesizing signals across multiple sources.

---

## Solution Overview

AiVerse solves this by combining semantic retrieval with large language models to provide:

* Analyst-style answers grounded in real documents
* Multilingual query support
* Transparent, traceable insights
* A single-page, clean interface suitable for rapid exploration

---

## Key Features

* Retrieval-Augmented Generation (RAG) architecture
* Multilingual support (English, Tamil, Hindi, Telugu, Malayalam, Kannada)
* Suggested intelligence queries per language
* Source-grounded answers (no hallucinated insights)
* Clean, single-page Streamlit UI
* Mobile-friendly and desktop-optimized layout
* Designed for startup, VC, and policy intelligence use cases

---

## How the RAG System Works

1. User submits a query in any supported language
2. Query is normalized and translated if required
3. Relevant documents are retrieved using semantic search
4. Retrieved evidence is passed to the LLM
5. The model generates a concise, analyst-style response
6. Output is presented with contextual grounding and disclaimers

This ensures responses remain factual, explainable, and aligned with the underlying data.

---

## Tech Stack

**Frontend**

* Streamlit
* Custom CSS for theming and layout control

**Backend**

* Python
* Retrieval-Augmented Generation pipeline
* Embedding-based semantic search
* LLM-based answer synthesis

**Data Sources**

* Startup funding articles
* Policy documents
* Public investment reports
* News and ecosystem analysis

---

## Project Structure

```
project-root/
│
├── app.py                     # Streamlit application
├── rag/
│   ├── generator.py           # RAG answer generation logic
│   ├── retriever.py           # Semantic retrieval layer
│   └── embeddings.py          # Vector embedding utilities
│
├── ingestion/
│   ├── pdf_loader.py          # PDF ingestion
│   ├── csv_loader.py          # CSV ingestion
│   ├── web_loader.py          # Web data ingestion
│   └── clean_text.py          # Text preprocessing
│
├── raw/
│   ├── funding_articles/      # Source funding data
│   └── policy_documents/      # Source policy data
│
└── README.md
```

---

## Installation and Setup

1. Clone the repository

   ```
   git clone <https://github.com/Subha-k07/Aiverse-RAG>
   cd AIVERSE-RAG
   ```

2. Create and activate a virtual environment

   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies

   ```
   pip install -r requirements.txt
   ```

4. Run the Streamlit app

   ```
   streamlit run app.py
   ```

---

## Usage

* Select a language from the multilingual options
* Choose a suggested query or enter a custom question
* Click "Get Answer" to receive an analyst-style insight
* Review the grounded response and disclaimer
* Explore how the RAG system works using the expandable section

---

## Use Cases

* Startup founders identifying relevant investors
* VC analysts researching market trends
* Policy researchers analyzing ecosystem signals
* Hackathon demos for AI + RAG applications
* Educational demonstrations of retrieval-based LLM systems

---

## Disclaimer

AiVerse provides AI-generated insights based on publicly available data processed through a Retrieval-Augmented Generation system. The output is intended strictly for research and informational purposes and should not be considered financial, legal, or investment advice.

---

## Future Enhancements

* Source citation links in answers
* Investor and startup entity profiling
* Confidence scoring per insight
* Dynamic document ingestion
* Advanced filtering by sector and stage

---

## License

This project is released for educational and hackathon use.
Refer to individual data sources for their respective usage licenses.

---


