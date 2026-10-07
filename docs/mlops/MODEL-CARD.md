# Model card — baseline text classifier

## Intended use
Educational and reference implementation for binary SMS spam classification. It is not automatically suitable for email moderation, fraud, abuse enforcement or other domains.

## Model
TF-IDF unigram/bigram representation plus class-balanced Logistic Regression. Training is deterministic given the documented dataset and split seed.

## Data
UCI SMS Spam Collection. See `docs/datasets/DATASETS.md` for provenance and licensing.

## Metrics
Run `python scripts/train.py` to generate the current evaluation JSON. Record evaluation with the artifact/version promoted to an environment.

## Limitations
Language/domain shift, evolving spam tactics, short-message ambiguity and dataset age can reduce real-world performance. Probability output is not guaranteed to be calibrated for every deployment population.

## Risk
False positives can hide legitimate messages. Thresholds and review/exception processes must reflect the application's business impact.

## Monitoring
Service health and model quality are distinct. Monitor latency/errors/resources continuously; monitor model quality/drift when representative ground truth becomes available.
