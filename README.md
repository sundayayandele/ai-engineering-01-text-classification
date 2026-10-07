# Production NLP Text Classification

> Project 01 of **20 Production AI Engineering Projects — From ML Foundations to Enterprise Agentic AI**

Build, evaluate, secure, package and deploy a production-oriented text classification service. The reference use case is SMS spam detection using the UCI SMS Spam Collection.

## Two tracks

**Learning / Portfolio:** TF-IDF + Logistic Regression, reproducible training, evaluation, FastAPI inference, pytest, Docker.

**Enterprise / Production:** transformer extension, model registry pattern, Kubernetes/OpenShift, observability, security controls, IaC, capacity planning, HA reference architecture and deployment economics.

## Architecture

This repository documents three required views plus C4:
- Enterprise architecture: TOGAF 10 viewpoints + ArchiMate-inspired business/application/technology layers.
- Logical architecture: channels → API → classification service → model → telemetry.
- Technical architecture: ingress/API pods/model artifact/metrics/logging, with Kubernetes/OpenShift deployment.
- C4: System Context, Container and Component views.

See [Architecture](docs/architecture/ARCHITECTURE.md), [Infrastructure](docs/infrastructure/INFRASTRUCTURE.md), [Security](docs/security/SECURITY.md), and [ADRs](docs/adr/ADR-001-model-strategy.md).

## Dataset

Reference dataset: **UCI SMS Spam Collection**, 5,574 labeled SMS messages, DOI `10.24432/C5CC84`, licensed **CC BY 4.0**. Data is downloaded at runtime and is not committed. See [DATASETS.md](docs/datasets/DATASETS.md).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/train.py
uvicorn app.main:app --reload
```

Then:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Congratulations! Claim your free prize now"}'
```

Health endpoints: `/health/live`, `/health/ready`. API docs: `/docs`.

## Repository map

```text
app/                    FastAPI serving layer
src/text_classifier/    data, training and inference package
scripts/                training utilities
tests/                  unit/API tests
docs/                    architecture, infra, security, datasets, TCO, ADRs
diagrams/source/         editable Mermaid diagrams
docker/                  container assets
kubernetes/              cloud-neutral manifests
openshift/               OpenShift overlays/notes
terraform/               Terraform/OpenTofu cloud examples
.github/workflows/       CI
```

## Model strategy

The default baseline intentionally uses TF-IDF + Logistic Regression: fast on CPU, interpretable, inexpensive and appropriate for a small labeled corpus. A transformer is an extension, not a forced dependency. Production promotion should be evidence-based: compare precision/recall/F1, false-positive cost, latency, memory, throughput and drift before replacing the baseline.

## Quality gates

CI runs formatting/linting, unit/API tests and a lightweight training smoke test. Production promotion additionally requires dataset/version provenance, evaluation evidence, security review, container scanning, model approval and deployment rollback readiness.

## Deployment paths

1. Local Python
2. Docker / Docker Compose
3. Kubernetes
4. Red Hat OpenShift
5. Terraform/OpenTofu reference deployments for Azure, AWS and GCP

The application remains cloud-neutral; cloud modules are optional deployment examples.

## Infrastructure & economics

Three economic scenarios are documented in [COST-TCO.md](docs/COST-TCO.md):
- local/on-prem/private cloud
- self-hosted VPS
- Azure/AWS/GCP

Numbers are planning assumptions, not vendor quotes. Benchmark the real model and workload before procurement.

## Responsible AI & security

Spam classification can produce harmful false positives. The reference architecture supports confidence thresholds, auditability, monitoring, human review for sensitive workflows, rate limiting, authentication at the gateway, TLS, least privilege and secrets outside Git.

## Roadmap

- [x] Golden repository structure
- [x] Classical baseline
- [x] FastAPI serving layer
- [x] Architecture + ADR foundation
- [x] Docker/Kubernetes/OpenShift baseline
- [x] Terraform/OpenTofu starter modules
- [ ] Transformer benchmark
- [ ] MLflow/model-registry integration
- [ ] Prometheus/Grafana dashboard
- [ ] Load-test evidence and calibrated production sizing
- [ ] Cloud deployment validation

## License

Code in this repository is intended to be released under the MIT License. Dataset licensing is separate; see `docs/datasets/DATASETS.md`.

## Series

This repository is the **golden reference** for the remaining 19 projects. Patterns are reused only where appropriate; later projects expand the platform for CV, speech, semantic search, RAG, agents, fine-tuning and enterprise model serving.
