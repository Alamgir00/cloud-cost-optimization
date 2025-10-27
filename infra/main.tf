# Optional: Terraform skeleton to create S3 bucket and IAM role for CI.
# This is a placeholder and requires customization before use.
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  type = string
  default = "us-east-1"
}

resource "aws_s3_bucket" "reports" {
  bucket = "my-cost-optimization-reports-${random_id.bucket_id.hex}"
  acl    = "private"
}

resource "random_id" "bucket_id" {
  byte_length = 4
}

# Create IAM role/policy as needed for CI runners to read/write S3 and call EC2/CloudWatch/Cost APIs.

