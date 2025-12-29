from pdf_loader import load_pdf
from csv_loader import load_csv
from web_loader import load_web
from clean_text import clean

def run():
    all_docs = []

    all_docs += load_pdf("data/raw/funding_report.pdf", "Funding_Report_2024")
    all_docs += load_csv("data/raw/investors.csv", "Investor_Database")
    all_docs += load_web("https://example.com/startup-policy")

    for doc in all_docs:
        doc["text"] = clean(doc["text"])

    return all_docs
