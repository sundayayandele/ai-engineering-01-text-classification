# ADR-003: Cloud-neutral workload with provider-specific infrastructure

**Status:** Accepted

## Decision
Keep application containers and Kubernetes manifests cloud-neutral. Place Azure, AWS and GCP infrastructure in separate Terraform/OpenTofu roots.

## Consequences
The application can move between Kubernetes/OpenShift environments. Provider integrations remain explicit rather than hidden behind an abstraction that erases useful cloud differences. IaC validation is performed independently per provider.
