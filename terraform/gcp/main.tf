provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "app" {
  location      = var.region
  repository_id = var.repository_id
  format        = "DOCKER"
}

output "repository_name" { value = google_artifact_registry_repository.app.name }
