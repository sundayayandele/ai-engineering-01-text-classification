# Threat model

## Assets
Model artifact and evaluation evidence; API availability; client text; deployment credentials; CI/CD integrity; telemetry; configuration and decision threshold.

## Trust boundaries
1. Internet/client → gateway/route.
2. Gateway → application namespace.
3. Application → model/artifact supply chain.
4. CI runner → registry/deployment platform.
5. Workload → telemetry platform.

## Representative threats and mitigations
| Threat | Impact | Controls |
|---|---|---|
| Oversized/adversarial requests | availability/cost | schema limits, gateway body/rate limits, timeouts |
| Raw text leakage | confidentiality | no raw-text metric labels, log minimization/redaction |
| Model replacement/tampering | integrity | immutable artifacts, provenance, controlled promotion |
| Dependency compromise | supply chain | pinned/reviewed dependencies, audit/scanning, minimal image |
| Container escape/privilege abuse | platform | non-root image, no privilege escalation, drop capabilities, RuntimeDefault seccomp |
| Credential theft | platform/data | workload identity, secret store, no Git secrets, least privilege |
| Excessive traffic | availability | HPA, quotas/rate limits, capacity alerts |
| Bad model promotion | business quality | evaluation gate, approval, canary and rollback |

## Residual risk
Text classification is probabilistic. Security controls do not remove model error. Product owners must define acceptable false-positive/false-negative risk and human review requirements.
