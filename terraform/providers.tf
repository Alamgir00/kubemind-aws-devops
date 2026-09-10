provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "KubeMind-AI"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
