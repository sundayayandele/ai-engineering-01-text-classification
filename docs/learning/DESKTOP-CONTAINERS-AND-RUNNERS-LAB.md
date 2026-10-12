# Project 01 — Desktop container and API lab

**Educational / Portfolio track** for SMS spam text classification. These commands are tailored to this repository. Do not interpret a local single-node run as production HA.

## Host sizing (planning minimums, not benchmarks)

| Profile | CPU | RAM | Free disk | Notes |
|---|---|---|---|---|
| Lightweight API container | 1 vCPU | 1 GiB | 5–10 GiB | Application container; CPU inference |
| Comfortable desktop lab | 2–4 logical CPUs | 8 GiB host RAM (16 GiB preferred) | 15–25 GiB | Includes desktop VM, image layers, training dependencies |
| Two-replica pilot simulation | 2–4 CPU total | 4 GiB assigned to container engine | 15–25 GiB | Same laptop/VM is **not** genuine HA |
| Enterprise baseline | See capacity plan | See capacity plan | Include registry, logs, backups | Validate with real traffic |

For Docker Desktop, Rancher Desktop or Podman Desktop on Windows/macOS, allocate **at least 2 CPUs, 4 GiB RAM and 15 GiB disk** to the container VM where settings permit; 4 CPUs and 6–8 GiB VM RAM are more comfortable. Leave sufficient RAM for the host OS. These are suggested *desktop allocations*, not per-container resource requirements. No GPU required.

## 1. Clone your own learner branch

Fork [the upstream repository](https://github.com/sundayayandele/ai-engineering-01-text-classification), then:

```bash
git clone https://github.com/YOUR_USERNAME/ai-engineering-01-text-classification.git
cd ai-engineering-01-text-classification
git switch -c learner/desktop-lab
```

## 2. Install dependencies and train locally

Install Git and Python 3.12. In macOS/Linux/WSL/Git Bash:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python scripts/train.py
pytest -q
```

On Windows PowerShell use `py -3.12 -m venv .venv` and `.venv\Scripts\Activate.ps1`. Verify that `artifacts/model.joblib` exists before starting a container.

Training downloads the UCI SMS Spam Collection from its public source. Internet access is needed for the first training run. The Dockerfile copies artifacts at build time, so retrain and rebuild if the model changes.

## 3A. Docker Desktop

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/), start it and select Linux containers.
2. Check Settings → Resources and ensure adequate CPU, memory and disk (on WSL2, limits may be controlled via WSL settings).
3. Confirm `docker version` and `docker compose version`.
4. From the repository root run:

```bash
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml ps
docker compose -f docker-compose.yml logs --tail=50
```

**Local-only networking:** The repository's Compose file exposes port 8000. For a machine shared with other users, change the host port binding to `127.0.0.1:8000:8000` before starting, so it is not exposed on all host interfaces.

## 3B. Rancher Desktop

1. Install [Rancher Desktop](https://rancherdesktop.io/) and start it.
2. Select the **dockerd (moby)** container engine, not containerd, for the unmodified `docker compose` commands.
3. In Preferences/Settings configure CPU, RAM and disk where available; enable the Docker-compatible CLI.
4. Verify `docker version` and `docker compose version`.
5. Run the **same Docker Compose commands in step 3A**.
6. Optional: enable Rancher Desktop Kubernetes for learning, but the repository Kubernetes manifests may need a local image, model artifact volume and ingress/storage setup. One laptop is not a multi-node HA environment.

## 3C. Podman Desktop

1. Install [Podman Desktop](https://podman-desktop.io/), complete onboarding and install Podman if prompted.
2. On Windows/macOS, create and start a **Podman machine**; on Linux use the rootless Podman engine.
3. Check `podman version` and `podman info`. Ensure machine resources and file sharing are sufficient.
4. From the repository root:

```bash
podman build -t project01-text-classifier:local .
```

Project 01 copies `artifacts/` into the image when building. Train before building. Then run:

```bash
podman run -d --name project01-api -p 127.0.0.1:8000:8000 \
  --cpus 1 --memory 1g \
  --security-opt no-new-privileges \
  -e MODEL_PATH=/app/artifacts/model.joblib \
  project01-text-classifier:local
```

Inspect `podman ps`, `podman logs project01-api` and `podman stats --no-stream project01-api`. To stop, run `podman rm -f project01-api`.

**Note:** Podman Compose requires an installed Compose provider and may behave differently from Docker Compose. The explicit `podman build` and `podman run` commands are the primary lab instructions.

## 4. API testing with Postman

1. Open http://127.0.0.1:8000/health/live — expect HTTP 200.
2. Open http://127.0.0.1:8000/health/ready — expect HTTP 200 if the model loaded.
3. Open http://127.0.0.1:8000/docs — review FastAPI OpenAPI.
4. In Postman create **POST** `http://127.0.0.1:8000/predict`.
5. Under **Body → raw → JSON**, enter:

```json
{"text":"Congratulations! Claim your free prize now"}
```

6. Set `Content-Type: application/json` (Postman sets this for raw JSON) and select **Send**.
7. Expect HTTP 200 with label and spam_probability. Capture the request/response as lab evidence.

Alternatively, on macOS/Linux/Git Bash:

```bash
curl -i http://127.0.0.1:8000/health/ready
curl -i -X POST http://127.0.0.1:8000/predict -H 'Content-Type: application/json' -d '{"text":"Congratulations! Claim your free prize now"}'
```

## 5. Logs, resource evidence and cleanup

```bash
docker stats --no-stream
docker compose -f docker-compose.yml logs --tail=100
docker compose -f docker-compose.yml down
```

For Podman, use `podman stats --no-stream project01-api` and `podman rm -f project01-api` instead. Record test results, CPU/RAM/disk, branch and commit SHA. Do not commit datasets, model binaries or secrets.

## 6. GitHub-hosted runners

1. Fork this public repository and create branch `learner/github-runner-lab`.
2. Review workflows in `.github/workflows/`; enable Actions in your fork if GitHub asks.
3. Push a change or open a pull request to trigger `ci`.
4. Inspect the CI quality/test jobs and container build. The existing CI does **not** train the model or verify a live container prediction end-to-end; perform the local lab for that evidence.
5. Record the run URL and commit SHA. Standard runners for eligible public repositories are generally free under GitHub's published terms; verify current billing/quotas.
6. GitHub runners are temporary and cannot provide persistent hosting or real multi-node HA.

See [the existing learning guide](LEARNING-GUIDE.md).

## Troubleshooting

| Issue | Fix |
|---|---|
| Docker/Podman daemon unavailable | Start desktop engine or Podman machine; run `docker version` / `podman info` |
| Port 8000 already in use | Stop competing service or change host-side port |
| Readiness 503 | Verify trained model artifact, container logs and expected artifact path |
| Container build fails | Check free disk and engine memory; ensure model is trained first where required |
| Podman bind-mount denied | Check machine file sharing, SELinux label and rootless permissions |
| Postman returns 422 | Use **Body → raw → JSON** and correct `predict` schema |
| Unreliable results | Synthetic data (Project 02) or a small reference dataset (Project 01) cannot establish enterprise production performance |

## Enterprise / Production boundary

For actual HA use multiple worker nodes/failure domains, authenticated TLS ingress, image scanning, signed model artifacts, monitoring, secrets management, rollback and workload-based sizing. See [capacity planning](../infrastructure/CAPACITY-PLANNING.md), [deployment](../DEPLOYMENT.md) and [TCO](../COST-TCO.md).
