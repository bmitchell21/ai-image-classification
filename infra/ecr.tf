# Filter out local zones, which are not currently supported 
# with managed node groups
data "aws_availability_zones" "available" {
  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}

resource "aws_ecr_repository" "k8s-ai-processer" {
  name                 = "k8s-ai-image-processer"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.aws_ecr_key.arn
  }
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_kms_key" "aws_ecr_key" {
  description = "ECR KMS Key"
  policy = jsonencode({
    Id = "K8sECRPolicy"
    Statement = [
      {
        Action = "kms:*"
        Effect = "Allow"
        Principal = {
          AWS = "*"
        }

        Resource = "*"
      },
    ]
    Version = "2012-10-17"
  })
}