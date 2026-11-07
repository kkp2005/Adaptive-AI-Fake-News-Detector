"""Fine-tune BERT from a CSV with columns: text,label (0=REAL, 1=FAKE)."""
import argparse
from pathlib import Path

import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    Trainer, TrainingArguments
)

class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = list(labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(value[idx]) for key, value in self.encodings.items()}
        item["labels"] = torch.tensor(int(self.labels[idx]), dtype=torch.long)
        return item

    def __len__(self):
        return len(self.labels)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/news.csv")
    parser.add_argument("--output", default="backend/models/fake-news-bert")
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    if not {"text", "label"}.issubset(data.columns):
        raise ValueError("CSV must contain 'text' and 'label' columns.")
    data = data.dropna(subset=["text", "label"])
    data["text"] = data["text"].astype(str).str.strip()
    data["label"] = data["label"].astype(int)
    data = data[data["label"].isin([0, 1])]
    if len(data) < 20 or data["label"].nunique() != 2:
        raise ValueError("Use at least 20 labelled examples and include both labels. More data is strongly recommended.")

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        data["text"], data["label"], test_size=0.2, random_state=42, stratify=data["label"]
    )
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    train_enc = tokenizer(train_texts.tolist(), truncation=True, padding=True, max_length=512)
    val_enc = tokenizer(val_texts.tolist(), truncation=True, padding=True, max_length=512)
    train_ds = NewsDataset(train_enc, train_labels.tolist())
    val_ds = NewsDataset(val_enc, val_labels.tolist())

    model = AutoModelForSequenceClassification.from_pretrained(
        "bert-base-uncased", num_labels=2, id2label={0: "REAL", 1: "FAKE"}, label2id={"REAL": 0, "FAKE": 1}
    )
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    training_args = TrainingArguments(
        output_dir=str(output / "training-checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=4,
        dataloader_pin_memory=False,
        fp16=False,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=10,
        load_best_model_at_end=False,
        report_to="none",
    )
    trainer = Trainer(model=model, args=training_args, train_dataset=train_ds, eval_dataset=val_ds)
    trainer.train()
    trainer.save_model(str(output))
    tokenizer.save_pretrained(str(output))
    print(f"Saved fine-tuned model to: {output.resolve()}")

if __name__ == "__main__":
    main()
