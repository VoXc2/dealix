terraform {
  required_version = ">= 1.7.0"

  required_providers {
    railway = {
      source  = "terraform-community-providers/railway"
      version = "~> 0.5"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.40"
    }
  }

  # Use a remote backend in production; local for now so the founder
  # can `terraform plan` without ceremony. Swap to S3 + DynamoDB lock
  # or Terraform Cloud workspace when a deploy cadence justifies it.
  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "railway" {
  token = var.railway_token
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

locals {
  service_name = "dealix"
  envs = {
    staging = {
      domain = "api.staging.dealix.me"
      replicas = 1
    }
    prod = {
      domain = "api.dealix.me"
      replicas = 2
    }
  }
}
