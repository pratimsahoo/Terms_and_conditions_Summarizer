import json
import re
import requests
from src.ai_engine.prompts import SYSTEM_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


def extract_json(text: str) -> dict:
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())


def run_inference(input_text: str) -> dict:
    payload = {
        "model": MODEL_NAME,
        "prompt": SYSTEM_PROMPT + "\n\nINPUT:\n" + input_text,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    raw = response.json().get("response", "")

    try:
        return extract_json(raw)
    except Exception:
        return {
            "summary": ["Unable to parse structured model output"],
            "risk_score": 5,
            "risk_level": "Medium",
            "key_risks": ["Unstructured or invalid model response"],
            "disclaimer": "This is not legal advice."
        }
