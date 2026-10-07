# ADR-004: Secure-by-default container workload

**Status:** Accepted

## Decision
The reference workload disables automatic service-account token mounting, disallows privilege escalation, drops Linux capabilities, uses RuntimeDefault seccomp and a read-only root filesystem with explicit ephemeral writable storage.

## Consequences
The application must not assume root access or arbitrary filesystem writes. This improves portability to restricted Kubernetes/OpenShift environments and makes unsafe dependencies visible earlier.
