# Staging environment composition — wires the base modules in
# `infra/terraform/` with staging-specific values.
#
# Usage:
#   cp staging.auto.tfvars.example staging.auto.tfvars
#   # fill in the keys / IDs the founder controls
#   terraform -chdir=infra/terraform/live/staging init
#   terraform -chdir=infra/terraform/live/staging plan
#   terraform -chdir=infra/terraform/live/staging apply

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

  backend "local" {
    # Swap to S3 + DynamoDB lock once the founder has an AWS account
    # for state. Local file is fine until then.
    path = "terraform.tfstate"
  }
}

module "dealix" {
  source = "../../"

  environments         = ["staging"]
  railway_token        = var.railway_token
  railway_project_id   = var.railway_project_id
  cloudflare_api_token = var.cloudflare_api_token

  anthropic_api_key = var.anthropic_api_key
  openai_api_key    = var.openai_api_key
  sentry_dsn        = "" # staging is noisy — keep Sentry off here.
}

variable "railway_token"        { type = string; sensitive = true }
variable "railway_project_id"   { type = string }
variable "cloudflare_api_token" { type = string; sensitive = true }
variable "anthropic_api_key"    { type = string; sensitive = true; default = "" }
variable "openai_api_key"       { type = string; sensitive = true; default = "" }
