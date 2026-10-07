provider "aws" { region = var.region }

resource "aws_ecr_repository" "app" {
  name                 = var.project
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration { scan_on_push = true }
}

output "repository_url" { value = aws_ecr_repository.app.repository_url }
