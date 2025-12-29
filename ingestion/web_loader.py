import requests
from bs4 import BeautifulSoup

def load_web(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    text = " ".join(p.get_text() for p in soup.find_all("p"))

    return [{
        "text": text,
        "metadata": {
            "source": url,
            "type": "web"
        }
    }]
