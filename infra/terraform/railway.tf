# Railway-hosted API service + Postgres + Redis per environment.
# Cerbos lives in its own module (see cerbos.tf).

resource "railway_service" "api" {
  for_each = toset(var.environments)

  name       = "${local.service_name}-api-${each.key}"
  project_id = var.railway_project_id

  # Build is driven by the existing Dockerfile.
  source_repo = "VoXc2/dealix"
  source_repo_branch = each.key == "prod" ? "main" : each.key
}

resource "railway_variable" "api" {
  for_each = railway_service.api

  service_id = each.value.id

  # The map below is the canonical set of env vars the API expects.
  # Empty strings keep the feature inert until the operator binds a
  # real value via Railway dashboard or Infisical sync.
  variables = {
    APP_ENV                  = each.key
    APP_URL                  = "https://${local.envs[each.key].domain}"
    UVICORN_WORKERS          = each.key == "prod" ? "2" : "1"
    ANTHROPIC_API_KEY        = var.anthropic_api_key
    OPENAI_API_KEY           = var.openai_api_key
    SENTRY_DSN               = each.key == "prod" ? var.sentry_dsn : ""
    BETTERSTACK_HEARTBEAT_URL = ""
    STRIPE_API_KEY           = ""
    WORKOS_API_KEY           = ""
    PLAIN_API_KEY            = ""
    KNOCK_API_KEY            = ""
    PORTKEY_API_KEY          = ""
    LAGO_API_KEY             = ""
    LOOPS_API_KEY            = ""
    INFISICAL_TOKEN          = ""
    INNGEST_SIGNING_KEY      = ""
    INNGEST_EVENT_KEY        = ""
    CERBOS_PDP_URL           = "http://cerbos.railway.internal:3592"
    LLM_MAX_USD_PER_REQUEST    = "0.50"
    LLM_MAX_USD_PER_TENANT_DAY = "25.00"
  }
}
