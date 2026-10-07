from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from text_classifier.model import TextClassifier

app = FastAPI(title="Production Text Classification API", version="0.1.0")


class PredictRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)


class PredictResponse(BaseModel):
    label: str
    spam_probability: float


@lru_cache
def get_model() -> TextClassifier:
    path = Path(os.getenv("MODEL_PATH", "artifacts/model.joblib"))
    if not path.exists():
        raise RuntimeError(f"Model artifact not found: {path}. Run scripts/train.py first.")
    return TextClassifier.load(path)


@app.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def readiness() -> dict[str, str]:
    try:
        get_model()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"status": "ready"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    threshold = float(os.getenv("DECISION_THRESHOLD", "0.5"))
    label, probability = get_model().predict(request.text, threshold)
    return PredictResponse(label=label, spam_probability=probability)
