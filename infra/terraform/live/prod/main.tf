# Production environment composition. Same module wiring as staging
# but with prod-only safety toggles (Sentry on, two API workers).
#
# Usage:
#   cp prod.auto.tfvars.example prod.auto.tfvars
#   terraform -chdir=infra/terraform/live/prod init
#   terraform -chdir=infra/terraform/live/prod plan
#   # human approval here.
#   terraform -chdir=infra/terraform/live/prod apply

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
    path = "terraform.tfstate"
  }
}

module "dealix" {
  source = "../../"

  environments         = ["prod"]
  railway_token        = var.railway_token
  railway_project_id   = var.railway_project_id
  cloudflare_api_token = var.cloudflare_api_token

  anthropic_api_key = var.anthropic_api_key
  openai_api_key    = var.openai_api_key
  sentry_dsn        = var.sentry_dsn
}

variable "railway_token"        { type = string; sensitive = true }
variable "railway_project_id"   { type = string }
variable "cloudflare_api_token" { type = string; sensitive = true }
variable "anthropic_api_key"    { type = string; sensitive = true; default = "" }
variable "openai_api_key"       { type = string; sensitive = true; default = "" }
variable "sentry_dsn"           { type = string; sensitive = true; default = "" }
