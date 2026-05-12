variable "railway_token" {
  description = "Railway API token. Source from the operator's env (do NOT commit)."
  type        = string
  sensitive   = true
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token, scoped to dealix.me zone."
  type        = string
  sensitive   = true
}

variable "railway_project_id" {
  description = "Railway project ID (UUID)."
  type        = string
}

variable "environments" {
  description = "Environments to provision."
  type        = list(string)
  default     = ["staging", "prod"]
}

variable "anthropic_api_key" {
  description = "Anthropic API key. Per-environment binding only."
  type        = string
  sensitive   = true
  default     = ""
}

variable "openai_api_key" {
  description = "OpenAI API key. Per-environment binding only."
  type        = string
  sensitive   = true
  default     = ""
}

variable "sentry_dsn" {
  description = "Production Sentry DSN."
  type        = string
  sensitive   = true
  default     = ""
}
