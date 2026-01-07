import sys
from src.core.url_extractor import extract_tc_text
from src.utils.generate_outputs import generate_output


def reduce_text(text: str, max_chars: int = 6000) -> str:
    """
    Limits text length to avoid overwhelming local LLMs.
    """
    return text[:max_chars]


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python -m src.utils.analyze_url <TERMS_URL>")
        return

    url = sys.argv[1]
    print(f"\n🔗 Fetching Terms & Conditions from:\n{url}\n")

    try:
        raw_text = extract_tc_text(url)
    except Exception as e:
        print(f"❌ Failed to fetch URL: {e}")
        return

    cleaned_text = reduce_text(raw_text)

    print("🤖 Analyzing content with local Mistral model...\n")

    result = generate_output(cleaned_text)

    print("✅ FINAL OUTPUT\n")
    print(result)


if __name__ == "__main__":
    main()
