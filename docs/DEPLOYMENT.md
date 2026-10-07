# Deployment guide

## Promotion path
Local → Docker → Kubernetes → OpenShift → cloud/private-cloud environment.

A production release is an immutable pair: **application image digest + approved model artifact/version**. Avoid mutable `latest` tags in real production promotion.

## Local
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/train.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Validate `/health/live`, `/health/ready`, `/metrics` and `/predict`.

## Container
Build only after the model artifact exists:
```bash
docker build -t text-classifier:local .
docker run --read-only --tmpfs /tmp -p 8000:8000 text-classifier:local
```

## Kubernetes
```bash
kubectl apply -k kubernetes/base
kubectl rollout status deployment/text-classifier
```
For production, replace the image reference with an immutable digest and integrate an approved artifact distribution mechanism.

## OpenShift
```bash
oc apply -k openshift
oc get deploy,pods,svc,route
```

## Release verification
1. CI quality/tests green.
2. Dependency and filesystem security scans green or formally reviewed.
3. IaC formatting/validation green.
4. Model evaluation approved.
5. Image and model identifiers recorded.
6. Smoke test readiness and prediction.
7. Observe latency/error/replica metrics.
8. Canary before broad production traffic where risk warrants it.
9. Roll back image/model pair if SLO or quality guardrails fail.
