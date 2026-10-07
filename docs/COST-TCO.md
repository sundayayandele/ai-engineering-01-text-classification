# Deployment economics / TCO framework

Do not treat example prices as quotes. Vendor prices vary by region, commitment, egress and date. Use the supplied architecture to price the exact region at deployment time.

## Scenario A — local / on-prem / private cloud
Best when existing compute, data-control requirements or predictable utilization dominate. Cost model: hardware amortization + power + rack/colo + storage + backup + platform licenses/support + operator time. The classical baseline can run on a small CPU VM.

## Scenario B — self-hosted VPS
Best for demos and modest always-on traffic. Start with roughly 2–4 vCPU and 4–8 GB RAM, then benchmark. Cost model: VM + snapshots/backups + traffic + managed DNS/monitoring if used + engineering time.

## Scenario C — Azure / AWS / GCP
Best when managed networking, IAM, autoscaling, compliance integrations or global footprint outweigh higher unit cost. Price: compute/managed Kubernetes control plane where applicable + registry + load balancer + logs/metrics + storage + egress + support.

## Comparison dimensions
Monthly infrastructure cost; engineering/operations labor; availability target; recovery objective; scaling elasticity; security/compliance integrations; data residency; egress; lock-in; reserved/committed discounts.

## FinOps rule
Measure CPU-seconds/request, memory working set, requests/month and telemetry volume. Recalculate cost per 1,000 classifications. For a transformer extension, add accelerator-hours and model-storage/transfer costs.
