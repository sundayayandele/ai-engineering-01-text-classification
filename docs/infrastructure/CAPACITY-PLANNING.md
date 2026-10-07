# Capacity planning worksheet

Do not size production from vCPU/RAM guesses alone. Use measured service demand.

## Inputs
- peak requests/second
- p50/p95 text length
- target p95/p99 latency
- safe measured RPS per pod
- CPU and memory at safe RPS
- model artifact memory
- failure-domain requirement
- rollout surge requirement
- growth/safety margin

## Replica calculation
A useful first bound is:

`steady_replicas = ceil(peak_rps / safe_rps_per_pod)`

Then add headroom for one replica/failure-domain loss and deployment surge. Validate the result with load testing.

## CPU baseline
For TF-IDF/logistic regression, benchmark on CPU first. GPU capacity is unnecessary unless a promoted transformer or throughput target proves otherwise.

## Transformer memory
Estimate:

`VRAM/RAM = model weights + framework/runtime + activations/KV or batch workspace + concurrency + safety margin`

Measure rather than relying solely on parameter-count arithmetic.

## Storage
Include immutable model artifacts, container layers, logs, metrics retention and backups. Training datasets and experiment artifacts have different lifecycle/retention requirements from serving pods.

## Network
Measure ingress payload, response, image/model pulls and telemetry. Hyperscaler egress and cross-zone traffic can materially affect TCO.
