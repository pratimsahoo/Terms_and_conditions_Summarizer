import re

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text: str) -> str:
    """
    Basic cleaning for legal text:
    - remove extra whitespace
    - normalize newlines
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# -----------------------------
# CHUNK TEXT
# -----------------------------
def chunk_text(text: str, chunk_size: int = 800) -> list[str]:
    """
    Split long T&C text into chunks
    based on word count.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
