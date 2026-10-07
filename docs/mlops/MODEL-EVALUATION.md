# Model evaluation and promotion

## Baseline versus transformer
The repository deliberately supports two candidate families:
1. TF-IDF + Logistic Regression — default, CPU-first.
2. DistilBERT fine-tuning — optional PyTorch/Hugging Face benchmark.

Use the **same deterministic stratified test split** when comparing candidates. Do not promote the transformer merely because it is newer.

## Promotion evidence
Record:
- precision, recall, F1, ROC-AUC where probabilities are comparable
- confusion matrix and false-positive/false-negative review
- p50/p95/p99 inference latency
- throughput at defined concurrency
- process/model memory
- image/artifact size
- training duration and compute
- estimated cost per 1,000 predictions
- robustness/error analysis

## Suggested gate
A production owner should define the gate from business risk. One example is: no regression in spam recall, materially improved precision/F1, p95 latency inside the SLO and an accepted cost increase. The repository intentionally does not hard-code a universal quality threshold.

## Lifecycle
Dataset provenance → train → evaluate → review → register/version → security scan → deploy candidate → smoke test → canary → monitor → promote/rollback.
