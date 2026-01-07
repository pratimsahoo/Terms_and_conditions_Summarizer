import requests
from bs4 import BeautifulSoup


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
    """
    Extract visible text from a Terms & Conditions webpage.
    Handles bot-protected websites gracefully.
    """

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)

        # Explicit handling for blocked sites
        if response.status_code == 403:
            raise ValueError(
                "This website blocks automated access (HTTP 403). "
                "Please copy-paste the Terms & Conditions text manually."
            )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        if len(text) < 200:
            raise ValueError("Extracted content is too short to be valid.")

        return text

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch URL: {str(e)}")
