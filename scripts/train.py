import json
from pathlib import Path

from sklearn.model_selection import train_test_split
from ucimlrepo import fetch_ucirepo

from text_classifier.evaluation import evaluate
from text_classifier.model import TextClassifier, build_pipeline


def main() -> None:
    dataset = fetch_ucirepo(id=228)
    texts = dataset.data.features.iloc[:, 0].astype(str)
    labels = dataset.data.targets.iloc[:, 0].astype(str).str.lower().map({"ham": 0, "spam": 1})
    x_train, x_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    pipeline = build_pipeline()
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    probabilities = pipeline.predict_proba(x_test)[:, 1]
    report = evaluate(y_test, predictions, probabilities)

    artifact_dir = Path("artifacts")
    artifact_dir.mkdir(parents=True, exist_ok=True)
    TextClassifier(pipeline).save(artifact_dir / "model.joblib")
    (artifact_dir / "evaluation.json").write_text(
        json.dumps(report.as_dict(), indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report.as_dict(), indent=2))


if __name__ == "__main__":
    main()
