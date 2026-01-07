import requests
from bs4 import BeautifulSoup

from src.utils.url_normalizer import normalize_url

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}


def extract_tc_text(url: str) -> str:
    url = normalize_url(url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)

        if response.status_code == 403:
            raise ValueError(
                "This website blocks automated access (HTTP 403). "
                "Please copy‑paste the Terms & Conditions text manually."
            )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        if len(text) < 300:
            raise ValueError(
                "The provided URL does not appear to be a Terms & Conditions page. "
                "Please provide a legal or policy page URL."
            )

        return text

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch URL: {str(e)}")
