# Contributing

Use a feature branch and keep changes small enough to review. Before opening a pull request run:

```bash
pip install -e ".[dev]"
ruff check .
pytest -q
docker build -t text-classifier:local .
kubectl kustomize kubernetes/base >/dev/null
```

Architecture-affecting changes should include or update an ADR. Model changes require evaluation evidence. Never commit credentials, private endpoints, production data, generated model binaries or Terraform state.

A change is not production-ready merely because unit tests pass: consider security, observability, rollback, capacity and documentation.
