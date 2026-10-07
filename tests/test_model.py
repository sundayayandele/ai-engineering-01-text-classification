from text_classifier.model import TextClassifier, build_pipeline


def test_pipeline_can_classify() -> None:
    pipeline = build_pipeline()
    pipeline.fit(
        ["hello friend see you tomorrow", "free prize claim now", "meeting at noon", "winner call now"],
        [0, 1, 0, 1],
    )
    model = TextClassifier(pipeline)
    label, probability = model.predict("free winner prize")
    assert label in {"ham", "spam"}
    assert 0.0 <= probability <= 1.0
