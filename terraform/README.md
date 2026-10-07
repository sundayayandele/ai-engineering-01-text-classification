# Terraform + OpenTofu

The IaC strategy is intentionally provider-separated:
- `azure/`: Azure reference deployment
- `aws/`: AWS reference deployment
- `gcp/`: GCP reference deployment

The application layer remains Kubernetes-compatible. Cloud modules should provision the surrounding platform (network, cluster/compute, registry, identity integration, observability hooks) rather than embedding application logic.

Both Terraform and OpenTofu are supported as design targets. Pin providers, use remote encrypted state with locking for teams, keep secrets out of state where possible, and run fmt/validate/security checks in CI.

Project 01 starts with architecture placeholders; validated cloud modules are a subsequent milestone because infrastructure code should not claim production readiness before plan/apply testing in the target accounts.
