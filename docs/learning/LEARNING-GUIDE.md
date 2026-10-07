# Learning guide

## What you should learn
This project teaches the complete lifecycle rather than only model fitting: define a classification problem, establish a baseline, split data without leakage, select meaningful metrics, package preprocessing with the estimator, expose inference safely, test the software, containerize it, deploy it and operate it.

## Why accuracy is insufficient
Spam is the minority class. A classifier can appear accurate while missing spam. Evaluate precision, recall, F1, ROC-AUC and the confusion matrix. In a messaging product, a false positive may be more costly than a missed spam message, so threshold selection is a product/risk decision.

## Exercises
1. Train the baseline and record metrics.
2. Inspect false positives and false negatives.
3. Tune the decision threshold.
4. Compare unigram vs unigram+bigram TF-IDF.
5. Benchmark a transformer against the same frozen test split.
6. Measure p50/p95 inference latency and memory.
7. Decide whether the transformer deserves production promotion using both quality and cost evidence.
8. Deploy two replicas and simulate a pod failure.

## Portfolio evidence
Show the architecture, evaluation report, API request/response, passing CI, container deployment and one measured performance/cost comparison. Explain trade-offs rather than presenting a model score alone.
