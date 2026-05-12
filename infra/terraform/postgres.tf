# Postgres database per environment, provisioned via Railway's
# managed Postgres add-on. Connection strings flow into the API service
# automatically via Railway's reference variables; we mirror them as
# DATABASE_URL to match what the app reads.

resource "railway_service" "postgres" {
  for_each = toset(var.environments)

  name       = "${local.service_name}-pg-${each.key}"
  project_id = var.railway_project_id
  # Railway provider exposes managed Postgres via a marketplace
  # template; the API at the time of this commit is in flux. Use the
  # generic resource and bind the image explicitly.
  source_image = "postgres:16-alpine"
}

resource "railway_variable" "postgres" {
  for_each = railway_service.postgres

  service_id = each.value.id

  variables = {
    POSTGRES_USER = "dealix"
    POSTGRES_DB   = "dealix"
    PGDATA        = "/var/lib/postgresql/data/pgdata"
  }
}

output "postgres_internal_hostnames" {
  value = {
    for env, svc in railway_service.postgres : env => "${svc.name}.railway.internal"
  }
}
