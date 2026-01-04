import json
import time
import requests
from pathlib import Path

# =============================
# OLLAMA CONFIG
# =============================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"   # Mistral-7B-Instruct via Ollama

# =============================
# PATHS
# =============================
INPUT_FILE = Path("data/processed/train.jsonl")
OUTPUT_FILE = Path("data/processed/train_labeled.jsonl")

# =============================
# PROMPT
# =============================
SYSTEM_PROMPT = """
You are a legal expert.

Analyze the following Terms and Conditions text and return a STRICT JSON object with:
- summary: 3 to 6 bullet points in simple language
- risk_score: integer between 0 and 10
- risk_level: Low, Medium, or High
- key_risks: list of key user risks
- disclaimer: "This is not legal advice."

Return ONLY valid JSON. Do not add explanations.
"""

# =============================
# LOCAL MODEL CALL
# =============================
def generate_output(tc_text: str) -> dict:
    payload = {
        "model": MODEL_NAME,
        "prompt": SYSTEM_PROMPT + "\n\n" + tc_text,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    text = response.json()["response"].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "summary": ["Unable to parse model response"],
            "risk_score": 5,
            "risk_level": "Medium",
            "key_risks": ["Parsing error"],
            "disclaimer": "This is not legal advice."
        }

# =============================
# MAIN PIPELINE
# =============================
def run():
    print("📘 Generating labeled outputs using local Mistral-7B model...")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"❌ Missing input file: {INPUT_FILE}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as fout:

        for idx, line in enumerate(fin, start=1):
            item = json.loads(line)

            item["output"] = generate_output(item["input"])
            fout.write(json.dumps(item, ensure_ascii=False) + "\n")

            print(f"✅ Processed sample {idx}")
            time.sleep(0.5)  # safe for local inference

    print("🎉 DONE")
    print(f"📂 Labeled dataset saved at: {OUTPUT_FILE}")

# =============================
# ENTRY POINT
# =============================
if __name__ == "__main__":
    run()
