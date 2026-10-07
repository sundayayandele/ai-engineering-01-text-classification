from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2, max_features=50_000)),
        ("classifier", LogisticRegression(max_iter=1_000, class_weight="balanced", random_state=42)),
    ])


@dataclass
class TextClassifier:
    pipeline: Pipeline

    @classmethod
    def load(cls, path: str | Path) -> "TextClassifier":
        return cls(joblib.load(path))

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, path)

    def predict(self, text: str, threshold: float = 0.5) -> tuple[str, float]:
        probability = float(self.pipeline.predict_proba([text])[0][1])
        return ("spam" if probability >= threshold else "ham", probability)
