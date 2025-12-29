import csv

def load_csv(path, source_name):
    docs = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = " | ".join([f"{k}: {v}" for k, v in row.items()])
            docs.append({
                "text": text,
                "metadata": {
                    "source": source_name,
                    "type": "csv"
                }
            })
    return docs
