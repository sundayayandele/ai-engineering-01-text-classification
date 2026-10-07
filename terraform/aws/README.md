# AWS reference
Target architecture: VPC/subnets → EKS (or ECS/App Runner-style smaller option where appropriate) → ECR → load balancer → CloudWatch/Prometheus integration → IAM roles for workloads + Secrets Manager. Validate regional SKU availability and price before deployment.
