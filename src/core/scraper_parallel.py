import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


def scrape_single_url(url: str) -> str:
    try:
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, "lxml")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        return " ".join(text.split())
    except Exception:
        return ""


def scrape_urls_parallel(urls: list[str], max_workers: int = 10) -> list[str]:
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scrape_single_url, url) for url in urls]

        for future in as_completed(futures):
            results.append(future.result())

    return results
