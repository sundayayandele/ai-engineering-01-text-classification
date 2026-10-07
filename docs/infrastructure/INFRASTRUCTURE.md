# Infrastructure sizing and setup

Sizing below is a **starting hypothesis**. Benchmark the actual artifact, payload distribution, concurrency and SLO before production procurement.

| Tier | Purpose | CPU | RAM | Storage | Replicas |
|---|---|---:|---:|---:|---:|
| Local | development | 2 vCPU | 4 GB | 5 GB | 1 |
| Lab/VPS | integration/demo | 2–4 vCPU | 4–8 GB | 20 GB | 1 |
| Small prod | CPU inference | 2–4 vCPU per pod | 4–8 GB/node minimum | 40+ GB | 2+ |
| Enterprise | HA platform | benchmark-derived | benchmark-derived | registry/log dependent | 2+ across zones |

No GPU is required for the classical baseline. A transformer benchmark must add model weights, framework overhead, batch/concurrency memory and safety margin before selecting CPU/GPU capacity.

## Local
1. Install Python 3.12.
2. Create a virtual environment and `pip install -e ".[dev]"`.
3. Run `python scripts/train.py`.
4. Run tests and start Uvicorn.

## Docker
Train the artifact first, then `docker compose up --build`. For enterprise use, fetch an immutable artifact during a controlled build/deploy process rather than hand-copying models.

## Kubernetes
Apply `kubernetes/base/`. The baseline requests 250m CPU/256Mi memory and limits at 1 CPU/1Gi. These are bootstrap values only. Load test and revise them.

## OpenShift
Use the Kubernetes manifests as the base and the OpenShift Route example for exposure. Keep the image compatible with arbitrary non-root UIDs; production should use an approved registry and platform security policies.

## Production sizing method
1. Define p50/p95 payload size and target p95 latency.
2. Benchmark one pod at increasing concurrency.
3. Identify saturation CPU/RAM and safe throughput.
4. Set requests near observed steady-state usage plus margin; limits protect the node without causing avoidable throttling/OOM.
5. Calculate replicas = peak RPS / safe RPS per pod, then add failure and rollout headroom.
6. Validate with load tests and one-node/one-zone failure scenarios.

## Operational prerequisites
DNS, TLS certificate, container registry, artifact store/registry, centralized logs/metrics, secrets manager, backup policy for persistent control-plane data, vulnerability scanning and alerting.
