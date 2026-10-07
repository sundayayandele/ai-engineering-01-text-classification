# ADR-002: Prometheus metrics with OpenTelemetry-compatible evolution

**Status:** Accepted

## Decision
Expose low-cardinality Prometheus metrics from the API for immediate service observability. Keep raw user text out of labels. Preserve an architectural path to OpenTelemetry for distributed traces and correlated telemetry as the series becomes more distributed.

## Consequences
Project 01 remains easy to run locally while teaching production metrics. Later RAG/agent projects can introduce end-to-end tracing without forcing unnecessary complexity into the first project.
