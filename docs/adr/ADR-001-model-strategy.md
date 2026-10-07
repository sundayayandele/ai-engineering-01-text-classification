# ADR-001: CPU-first classical baseline with transformer benchmark

**Status:** Accepted

## Context
Project 01 must teach end-to-end text classification while remaining inexpensive to run. The reference corpus is small enough that a sparse linear model is a strong engineering baseline.

## Decision
Use TF-IDF with Logistic Regression as the default deployable model. Treat a Hugging Face/PyTorch transformer as an explicit benchmark/extension. Promote it only when measured quality gains justify additional latency, memory, GPU/CPU cost and operational complexity.

## Consequences
The first deployment works on commodity CPU infrastructure, is easy to inspect and test, and creates a meaningful baseline. The architecture still permits a transformer model server later without changing the public API.
