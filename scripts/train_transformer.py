"""Optional Hugging Face/PyTorch benchmark.

Install with:
    pip install -e ".[transformer]"

This is deliberately separate from the CPU-first production baseline so the
default installation stays small and inexpensive.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)
from ucimlrepo import fetch_ucirepo

MODEL_NAME = "distilbert-base-uncased"


def compute_metrics(eval_pred) -> dict[str, float]:
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        "accuracy": float(accuracy_score(labels, predictions)),
        "precision": float(precision_score(labels, predictions, zero_division=0)),
        "recall": float(recall_score(labels, predictions, zero_division=0)),
        "f1": float(f1_score(labels, predictions, zero_division=0)),
    }


def main() -> None:
    raw = fetch_ucirepo(id=228)
    texts = raw.data.features.iloc[:, 0].astype(str).tolist()
    labels = (
        raw.data.targets.iloc[:, 0]
        .astype(str)
        .str.lower()
        .map({"ham": 0, "spam": 1})
        .astype(int)
        .tolist()
    )
    train_text, test_text, train_labels, test_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)

    train_ds = Dataset.from_dict({"text": train_text, "label": train_labels}).map(
        tokenize, batched=True
    )
    test_ds = Dataset.from_dict({"text": test_text, "label": test_labels}).map(
        tokenize, batched=True
    )
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    output = Path("artifacts/transformer")
    args = TrainingArguments(
        output_dir=str(output),
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        num_train_epochs=3,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        report_to=[],
        seed=42,
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=test_ds,
        processing_class=tokenizer,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    metrics = trainer.evaluate()
    output.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(output / "model"))
    tokenizer.save_pretrained(str(output / "model"))
    (output / "evaluation.json").write_text(
        json.dumps(metrics, indent=2, default=float) + "\n", encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2, default=float))


if __name__ == "__main__":
    main()
