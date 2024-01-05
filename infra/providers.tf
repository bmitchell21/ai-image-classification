terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.57.0"
    }
  }
  backend "s3" {
    profile = "k8scrzy"
    bucket = "spathsolutions-tfbackend"
    key    = "aws/k8s"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
  profile = "k8scrzy"
}

