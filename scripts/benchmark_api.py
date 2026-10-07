from __future__ import annotations

import argparse
import concurrent.futures
import statistics
import time

import httpx


def call(url: str, text: str) -> tuple[float, int]:
    started = time.perf_counter()
    response = httpx.post(url, json={"text": text}, timeout=10)
    return time.perf_counter() - started, response.status_code


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, round((len(ordered) - 1) * p))
    return ordered[index]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000/predict")
    parser.add_argument("--requests", type=int, default=200)
    parser.add_argument("--concurrency", type=int, default=10)
    args = parser.parse_args()
    sample = "Congratulations! You have won a free prize. Reply now."
    started = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        results = list(pool.map(lambda _: call(args.url, sample), range(args.requests)))
    elapsed = time.perf_counter() - started
    latencies = [latency for latency, _ in results]
    failures = sum(status >= 400 for _, status in results)
    print(f"requests={args.requests} concurrency={args.concurrency} failures={failures}")
    print(f"throughput_rps={args.requests / elapsed:.2f}")
    print(f"mean_ms={statistics.mean(latencies) * 1000:.2f}")
    print(f"p50_ms={percentile(latencies, 0.50) * 1000:.2f}")
    print(f"p95_ms={percentile(latencies, 0.95) * 1000:.2f}")
    print(f"p99_ms={percentile(latencies, 0.99) * 1000:.2f}")


if __name__ == "__main__":
    main()
