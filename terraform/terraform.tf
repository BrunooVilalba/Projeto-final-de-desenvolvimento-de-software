terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Uncomment for Terraform Cloud
  # cloud {
  #   organization = "estudaai"
  #   workspaces {
  #     name = "estudaai-production"
  #   }
  # }
}
