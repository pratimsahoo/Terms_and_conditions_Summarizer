from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer
from unsloth import FastLanguageModel

def main():
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="mistral",
        max_seq_length=4096,
        load_in_4bit=True
    )

    dataset = load_dataset("json", data_files="data/processed/train.jsonl")

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        args=TrainingArguments(
            output_dir="models/checkpoints",
            per_device_train_batch_size=2,
            num_train_epochs=1
        )
    )

    trainer.train()
    model.save_pretrained("models/final_adapter")

if __name__ == "__main__":
    main()
