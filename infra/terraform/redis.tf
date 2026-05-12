# Redis per environment for the rate limiter + Inngest dev runner +
# realtime SSE pub/sub.

resource "railway_service" "redis" {
  for_each = toset(var.environments)

  name        = "${local.service_name}-redis-${each.key}"
  project_id  = var.railway_project_id
  source_image = "redis:7-alpine"
}

output "redis_internal_hostnames" {
  value = {
    for env, svc in railway_service.redis : env => "${svc.name}.railway.internal"
  }
}
