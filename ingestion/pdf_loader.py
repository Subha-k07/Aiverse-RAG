from PyPDF2 import PdfReader

def load_pdf(path, source_name):
    reader = PdfReader(path)
    docs = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and len(text.strip()) > 50:
            docs.append({
                "text": text,
                "metadata": {
                    "source": source_name,
                    "page": i + 1,
                    "type": "pdf"
                }
            })
    return docs
