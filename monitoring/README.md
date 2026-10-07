# Observability

The golden project will expose application metrics suitable for Prometheus and preserve a vendor-neutral OpenTelemetry path for traces/log correlation.

Minimum production signals:
- request count and error count
- request duration histogram
- classifications by predicted label (avoid high-cardinality/raw-text labels)
- model version
- readiness failures
- process CPU/RAM
- saturation and replica availability

Model-quality monitoring is separate from service health. Where ground truth becomes available, monitor precision/recall/F1 and data/concept drift. Never put raw message text into metric labels.
