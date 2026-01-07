import json
import requests
import re
from pathlib import Path

# ======================================================
# OLLAMA CONFIG
# ======================================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

# ======================================================
# DATASET FILES (used when generating dataset)
# ======================================================
INPUT_FILE = Path("data/processed/train.jsonl")
OUTPUT_FILE = Path("data/processed/train_labeled.jsonl")

# ======================================================
# SYSTEM PROMPT (FROZEN)
# ======================================================
SYSTEM_PROMPT = """
You are a legal risk analysis engine.

You MUST return output in STRICT JSON format.
DO NOT include explanations, markdown, bullet points, or text outside JSON.

Analyze ONLY user-related risks such as:
- Liability limitations
- Account suspension or termination
- Refund or return restrictions
- Medical or legal disclaimers
- Data responsibility or user obligations

Return exactly this structure:

{
  "summary": ["...", "..."],
  "risk_score": 0,
  "risk_level": "Low | Medium | High",
  "key_risks": ["...", "..."],
  "disclaimer": "This is not legal advice."
}

Failure to follow this format is an error.
"""

# ======================================================
# JSON EXTRACTION (ROBUST)
# ======================================================
def extract_json(text: str) -> dict:
    """
    Extracts the first valid JSON object from model output.
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group())


# ======================================================
# MODEL INFERENCE
# ======================================================
def generate_output(tc_text: str) -> dict:
    payload = {
        "model": MODEL_NAME,
        "prompt": SYSTEM_PROMPT + "\n\nINPUT:\n" + tc_text,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    raw_output = response.json()["response"].strip()

    try:
        return extract_json(raw_output)
    except Exception:
        # Safe fallback (never crashes pipeline)
        return {
            "summary": ["Model returned unstructured output"],
            "risk_score": 5,
            "risk_level": "Medium",
            "key_risks": ["Unstructured or invalid model response"],
            "disclaimer": "This is not legal advice."
        }


# ======================================================
# DATASET GENERATION PIPELINE
# ======================================================
def run():
    print("📘 Generating labeled outputs using local Mistral model...\n")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as fout:

        for idx, line in enumerate(fin, start=1):
            item = json.loads(line)
            item["output"] = generate_output(item["input"])

            fout.write(json.dumps(item, ensure_ascii=False) + "\n")
            print(f"✅ Processed sample {idx}")

    print("\n🎉 DONE")
    print(f"📂 Output saved at: {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
