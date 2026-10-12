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

## Hands-on learner labs — Docker Desktop, Rancher Desktop, Podman Desktop, Postman and GitHub runners

**Two tracks remain:** Educational/Portfolio labs below; Enterprise/Production is the documented reference architecture and must be independently validated before deployment.

### Hardware and resource sizing

| Profile | CPU | RAM | Free disk |
|---|---|---|---|
| Single API container | 1 vCPU | 1 GiB | 5–10 GiB |
| Recommended desktop host | 2–4 logical CPUs | 8 GiB (16 GiB preferred) | 15–25 GiB |
| Desktop container engine VM (Windows/macOS) | 2–4 CPUs | 4 GiB minimum, 6–8 GiB comfortable | 15–25 GiB |
| Two-replica local simulation | 2 CPU total | 2 GiB total container limits, plus engine/host overhead | 15–25 GiB |

These are initial **learning estimates**, not measured production requirements. No GPU needed. For enterprise sizing and costs see [capacity planning](docs/infrastructure/CAPACITY-PLANNING.md) and [TCO](docs/COST-TCO.md).

### Step 1 — Fork, clone and prepare your model

Fork this repository, clone **your fork** and create a `learner/desktop-lab` branch. Install Git and Python 3.12:

```bash
git clone https://github.com/YOUR_USERNAME/ai-engineering-01-text-classification.git
cd ai-engineering-01-text-classification
git switch -c learner/desktop-lab
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python scripts/train.py
pytest -q
```

Windows PowerShell: `py -3.12 -m venv .venv` then `.venv\\Scripts\\Activate.ps1`. Confirm `artifacts/model.joblib` exists. Project 01's Dockerfile copies the trained artifact during build, so train first, then rebuild when weights change.

### Step 2A — Docker Desktop

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/), start the Linux container engine and allocate at least **2 CPUs, 4 GiB RAM and 15 GiB disk** where supported (WSL2 limits may be configured separately). Verify `docker version` and `docker compose version`, then:

```bash
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml ps
docker compose -f docker-compose.yml logs --tail=50
```

For a local-only lab, change the Compose port binding from `8000:8000` to `127.0.0.1:8000:8000` before starting, to avoid listening on all host interfaces.

### Step 2B — Rancher Desktop

Install [Rancher Desktop](https://rancherdesktop.io/), select **dockerd (moby)** engine, start the app, configure the VM resources (2+ CPUs, 4+ GiB RAM), and verify `docker version` and `docker compose version`. Use the **same Compose commands from Step 2A**. Optional Kubernetes is a learning cluster, not multi-node HA.

### Step 2C — Podman Desktop

Install [Podman Desktop](https://podman-desktop.io/), complete onboarding, and on Windows/macOS start a **Podman machine**. Confirm `podman version` and `podman info`. From the repository root:

```bash
podman build -t project01-text-classifier:local .
podman run -d --name project01-api -p 127.0.0.1:8000:8000 --cpus 1 --memory 1g -e MODEL_PATH=/app/artifacts/model.joblib project01-text-classifier:local
podman ps
podman logs project01-api
podman stats --no-stream project01-api
```

Podman machine host-volume sharing depends on OS and VM settings. See the detailed guide for troubleshooting, SELinux and Windows paths.

### Step 3 — Postman API test

1. Verify `GET http://127.0.0.1:8000/health/live` and `GET http://127.0.0.1:8000/health/ready` return HTTP 200.
2. Open `http://127.0.0.1:8000/docs` to inspect the API.
3. In **Postman**, create **POST** `http://127.0.0.1:8000/predict` → **Body → raw → JSON** and paste:

```json
{"text":"Congratulations! Claim your free prize now"}
```

4. Click **Send**; expect HTTP 200 with prediction fields. Capture logs and screenshots as portfolio evidence.
5. Cleanup: `docker compose -f docker-compose.yml down` (Docker/Rancher) or `podman rm -f project01-api` (Podman).

### Step 4 — GitHub-hosted runner lab (no desktop installation)

1. Fork the repository; create branch `learner/github-runner-lab` and enable **Actions** in your fork after reviewing the workflows.
2. Commit a small code change or open a pull request; inspect the **ci** run and record the SHA, logs and result.
3. Project 01's existing CI checks lint/tests and builds a container, but does not verify a live trained inference service end-to-end. Use the local lab above for that additional evidence.
4. Check GitHub's current Actions free-runner eligibility, minutes and billing settings. A hosted runner is temporary, not persistent hosting or genuine HA.

**Detailed step-by-step guide:** [Desktop containers, Postman and GitHub runner lab](docs/learning/DESKTOP-CONTAINERS-AND-RUNNERS-LAB.md).

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

## Architectural Diagram Overview
![Architecture Diagram](Architecturfal%20Diagrams.png)
