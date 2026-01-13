import os
import json
import random
from pathlib import Path

from src.core.cleaner import clean_text, chunk_text

# -----------------------------
# CONFIG
# -----------------------------
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

TRAIN_FILE = PROCESSED_DIR / "train.jsonl"
EVAL_FILE = PROCESSED_DIR / "eval.jsonl"

TRAIN_RATIO = 0.8  # 80% train, 20% eval

INSTRUCTION = "Summarize the following Terms and Conditions and identify key risks."

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def run_formatter():
    print("📂 Reading raw data from:", RAW_DIR)

    all_samples = []

    for file in RAW_DIR.glob("*.txt"):
        print(f"📄 Processing {file.name}")

        with open(file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        if len(raw_text.strip()) < 500:
            print(f"⚠️ Skipping {file.name} (too short)")
            continue

        cleaned = clean_text(raw_text)
        chunks = chunk_text(cleaned)

        for chunk in chunks:
            sample = {
                "instruction": INSTRUCTION,
                "input": chunk,
                "output": ""  # Filled later by LLM / during training
            }
            all_samples.append(sample)

    print(f"✅ Total samples created: {len(all_samples)}")

    # -----------------------------
    # SHUFFLE & SPLIT
    # -----------------------------
    random.shuffle(all_samples)

    split_index = int(len(all_samples) * TRAIN_RATIO)
    train_samples = all_samples[:split_index]
    eval_samples = all_samples[split_index:]

    # -----------------------------
    # SAVE FILES
    # -----------------------------
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for item in train_samples:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open(EVAL_FILE, "w", encoding="utf-8") as f:
        for item in eval_samples:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print("🎉 Done!")
    print(f"📘 Train samples: {len(train_samples)} → {TRAIN_FILE}")
    print(f"📗 Eval samples : {len(eval_samples)} → {EVAL_FILE}")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_formatter()
