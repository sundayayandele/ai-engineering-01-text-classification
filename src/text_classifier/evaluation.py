from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass(frozen=True)
class EvaluationReport:
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    confusion_matrix: list[list[int]]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate(y_true, y_pred, y_probability) -> EvaluationReport:
    return EvaluationReport(
        accuracy=float(accuracy_score(y_true, y_pred)),
        precision=float(precision_score(y_true, y_pred, zero_division=0)),
        recall=float(recall_score(y_true, y_pred, zero_division=0)),
        f1=float(f1_score(y_true, y_pred, zero_division=0)),
        roc_auc=float(roc_auc_score(y_true, y_probability)),
        confusion_matrix=confusion_matrix(y_true, y_pred).tolist(),
    )
