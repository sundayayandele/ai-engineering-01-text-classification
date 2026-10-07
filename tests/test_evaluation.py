from text_classifier.evaluation import evaluate


def test_evaluation_report() -> None:
    report = evaluate([0, 0, 1, 1], [0, 0, 1, 0], [0.1, 0.2, 0.9, 0.4])
    assert 0 <= report.f1 <= 1
    assert report.confusion_matrix == [[2, 0], [1, 1]]
