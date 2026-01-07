from src.utils.generate_outputs import generate_output
from src.core.url_extractor import extract_tc_text


def analyze_text(text: str) -> dict:
    """
    Analyze raw Terms & Conditions text.
    """
    return generate_output(text)


def analyze_url(url: str, max_chars: int = 6000) -> dict:
    """
    Analyze Terms & Conditions from a URL.
    """
    text = extract_tc_text(url)
    text = text[:max_chars]
    return generate_output(text)
