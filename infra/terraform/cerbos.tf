# Cerbos PDP sidecar — runs the policies in /cerbos/policies as a
# separate Railway service so the API can call it over HTTP at
# CERBOS_PDP_URL (set in railway.tf).

resource "railway_service" "cerbos" {
  for_each = toset(var.environments)

  name        = "${local.service_name}-cerbos-${each.key}"
  project_id  = var.railway_project_id
  source_image = "ghcr.io/cerbos/cerbos:0.39.0"
  # Mount the repo's cerbos/policies directory; Railway pulls from the
  # same git source as the API service.
  source_repo = "VoXc2/dealix"
  source_repo_branch = each.key == "prod" ? "main" : each.key
}

resource "railway_variable" "cerbos" {
  for_each = railway_service.cerbos

  service_id = each.value.id

  variables = {
    CERBOS_LOG_LEVEL = "info"
  }
}
