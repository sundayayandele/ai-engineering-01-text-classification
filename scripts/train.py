from pathlib import Path

from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from ucimlrepo import fetch_ucirepo

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
    print(classification_report(y_test, predictions, target_names=["ham", "spam"]))
    print(f"ROC-AUC: {roc_auc_score(y_test, probabilities):.4f}")
    TextClassifier(pipeline).save(Path("artifacts/model.joblib"))


if __name__ == "__main__":
    main()
