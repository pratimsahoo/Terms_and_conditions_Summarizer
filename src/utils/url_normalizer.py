from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """
    Normalize user-provided URLs:
    - example.com → https://example.com
    - www.example.com → https://www.example.com
    """
    url = url.strip()

    if not url:
        raise ValueError("URL is empty")

    parsed = urlparse(url)

    if not parsed.scheme:
        url = "https://" + url

    return url

