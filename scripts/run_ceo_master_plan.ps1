# CEO Master Plan — one-shot morning bundle (no external sends)
$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "== CEO Master Plan Morning =="
python scripts/bootstrap_founder_kpi_import.py
python scripts/founder_daily_five_metrics.py
python scripts/run_ceo_master_plan_status.py
python scripts/verify_first_paid_diagnostic_tracker.py
python scripts/ceo_production_trust_bundle.py
