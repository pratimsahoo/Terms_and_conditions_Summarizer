import requests
from bs4 import BeautifulSoup


def extract_tc_text(url: str) -> str:
    """
    Fetches a webpage and extracts readable text content.
    Designed for Terms & Conditions / Privacy Policy pages.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; TOS-Summarizer/1.0)"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # Normalize whitespace
    text = " ".join(text.split())

    return text
