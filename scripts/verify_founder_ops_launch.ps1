# Founder ops launch readiness (Windows)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Py = if ($env:PY) { $env:PY } else { "python" }

Write-Host "== Founder ops launch verify =="

& $Py -c @"
from dealix.revenue_ops_autopilot.config_loader import routing_thresholds
assert routing_thresholds()['qualified_a_min'] >= 10
print('config_loader: OK')
"@

& $Py -c @"
from dealix.revenue_ops_autopilot.webhook_handlers import handle_calendly_webhook
r = handle_calendly_webhook({'event': 'invitee.created', 'payload': {'email': 'test@example.sa', 'name': 'Test'}})
assert r.get('handled') is True
print('calendly_webhook: OK')
"@

$env:APP_ENV = "test"
& $Py -m pytest tests/test_revenue_ops_autopilot.py tests/test_founder_commercial_digest.py -q --no-cov

Write-Host "FOUNDER_OPS_LAUNCH_VERIFY: OK"
