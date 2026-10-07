# Security architecture

## Threat model
Primary risks include abusive input, oversized payloads, API abuse, model/artifact tampering, dependency compromise, sensitive text leakage through logs, unauthorized model promotion and denial of service.

## Controls
- TLS at ingress/gateway; authentication/authorization in the enterprise profile.
- Input length validation and gateway rate limits.
- Non-root container and read-only filesystem where possible.
- Secrets injected by platform secret stores; never committed.
- Immutable image/model identifiers and provenance checks.
- Least-privilege service accounts and namespace/network policies.
- Dependency/container/IaC scanning in the production pipeline.
- Avoid raw-message logging; redact identifiers and define retention.
- Audit model promotion and configuration/threshold changes.
- Separate training permissions from serving permissions.

## Responsible operation
False positives can suppress legitimate communication. Track precision/recall by relevant cohorts/use cases, maintain an exception path, calibrate thresholds, monitor drift and preserve rollback capability.
