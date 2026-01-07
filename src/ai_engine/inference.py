import json
import re
import requests
from src.ai_engine.prompts import SYSTEM_PROMPT

# -------------------------------------------------
# Ollama configuration
# -------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


# -------------------------------------------------
# Helper: Extract JSON safely from model output
# -------------------------------------------------
def extract_json(text: str) -> dict:
    """
    Extracts the first valid JSON object from the model response.
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group())


# -------------------------------------------------
# Core inference function
# -------------------------------------------------
def run_inference(input_text: str) -> dict:
    """
    Runs inference on Terms & Conditions text using local Mistral (Ollama).
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": SYSTEM_PROMPT + "\n\nINPUT:\n" + input_text,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    raw_output = response.json().get("response", "").strip()

    try:
        return extract_json(raw_output)
    except Exception:
        # Safe fallback (never crash the app)
        return {
            "summary": ["Unable to parse structured model output"],
            "risk_score": 5,
            "risk_level": "Medium",
            "key_risks": ["Unstructured or invalid model response"],
            "disclaimer": "This is not legal advice."
        }
