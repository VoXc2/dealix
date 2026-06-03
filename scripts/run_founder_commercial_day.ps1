# Founder commercial morning — canonical (Windows)
param(
    [switch]$DryRun,
    [switch]$WithBusinessNow,
    [switch]$Full
)

$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Import-DealixDotEnv {
    param([string]$EnvPath = (Join-Path $Root ".env"))
    if (-not (Test-Path $EnvPath)) { return }
    Get-Content $EnvPath -Encoding UTF8 | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) { return }
        $eq = $line.IndexOf("=")
        if ($eq -lt 1) { return }
        $name = $line.Substring(0, $eq).Trim()
        $val = $line.Substring($eq + 1).Trim().Trim('"').Trim("'")
        $current = [Environment]::GetEnvironmentVariable($name, "Process")
        if ($name -and -not [string]::IsNullOrEmpty($current)) { return }
        Set-Item -Path "env:$name" -Value $val
    }
}
Import-DealixDotEnv
if (-not $env:DEALIX_ADMIN_API_KEY -and $env:ADMIN_API_KEYS) {
    $env:DEALIX_ADMIN_API_KEY = ($env:ADMIN_API_KEYS -split ",")[0].Trim()
}
if (-not $env:DEALIX_API_BASE) {
    if ($env:DEALIX_API_URL) { $env:DEALIX_API_BASE = $env:DEALIX_API_URL }
    elseif ($env:NEXT_PUBLIC_API_URL) { $env:DEALIX_API_BASE = $env:NEXT_PUBLIC_API_URL }
}

function Invoke-DealixPy {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    if ($env:PY) { & $env:PY @Args } else { & py -3 @Args }
}
# UTC date — matches bash run_founder_commercial_day.sh and digest index
$Date = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd")

if ($Full) {
    $WithBusinessNow = $true
    $env:DEALIX_SYNC_EVIDENCE = "1"
}

if ($DryRun) {
    Invoke-DealixPy scripts/founder_revenue_day_runner.py --dry-run
    exit $LASTEXITCODE
}

Write-Host "== Dealix Founder Commercial Day (canonical) =="

Write-Host "`n== 0a/7 Agent work packets (today) =="
try { Invoke-DealixPy scripts/print_agent_work_packets.py --cadence daily } catch { Write-Host "  (agent packets warning — continuing)" }

Write-Host "`n== 0b/7 GTM public surfaces (repo) =="
try { Invoke-DealixPy scripts/verify_gtm_public_surfaces.py --skip-live } catch { Write-Host "  (gtm surfaces warning — continuing)" }

$ProdApi = if ($env:DEALIX_API_BASE) { $env:DEALIX_API_BASE } else { "https://api.dealix.me" }
Write-Host "`n== 0c/7 Production gates (Railway + live API) =="
try { Invoke-DealixPy scripts/run_founder_production_gates.py --api-base $ProdApi } catch { Write-Host "  (production gates warning — continuing)" }

Write-Host "`n== Expand stack (targeting + social + content) =="
Invoke-DealixPy scripts/expand_commercial_operating_stack.py --daily

$dailyArgs = @()
$TopN = 15
if (-not $env:DEALIX_ADMIN_API_KEY) { $dailyArgs += "--skip-api" } else { $dailyArgs += "--api-only" }
Write-Host "`n== 0/7 Dealix daily ops (bridge + health) =="
Invoke-DealixPy scripts/run_dealix_daily_ops.py @dailyArgs

Write-Host "`n== 1/7 Founder daily brief =="
Invoke-DealixPy scripts/dealix_founder_daily_brief.py --out "data/founder_briefs/brief_$Date.md"

Write-Host "`n== 2/7 KPI commercial status =="
Invoke-DealixPy scripts/bootstrap_founder_kpi_import.py
Invoke-DealixPy scripts/apply_kpi_founder_commercial.py --status

if ($WithBusinessNow -and (Test-Path "scripts/run_business_now.ps1")) {
    Write-Host "`n== optional: Business NOW =="
    & powershell -File scripts/run_business_now.ps1
}

Write-Host "`n== 3/8 War Room sync =="
Invoke-DealixPy scripts/commercial_war_room_sync.py

Write-Host "`n== 4/8 War Room CSV import =="
if ($env:DEALIX_ADMIN_API_KEY) {
    if (-not $env:DEALIX_API_BASE) { $env:DEALIX_API_BASE = $env:DEALIX_API_URL }
    if (-not $env:DEALIX_API_BASE) { $env:DEALIX_API_BASE = "http://localhost:8000" }
    Invoke-DealixPy scripts/import_war_room_targets.py --apply --via-api
    if ($LASTEXITCODE -ne 0) { Invoke-DealixPy scripts/import_war_room_targets.py --apply }
} else {
    Invoke-DealixPy scripts/import_war_room_targets.py --apply
}

Write-Host "`n== 5/8 Commercial digest =="
$sync = @()
if ($env:DEALIX_SYNC_EVIDENCE -eq "1") { $sync += "--sync-evidence"; $sync += "--pull-evidence" }
Invoke-DealixPy scripts/founder_commercial_digest.py --out "data/founder_briefs/commercial_$Date.md" @sync

Write-Host "`n== 5b/9 War Room touch drafts =="
Invoke-DealixPy scripts/generate_war_room_touch_drafts.py --top-n $TopN

Write-Host "`n== 6/9 Social queue =="
Invoke-DealixPy scripts/social_queue_today.py

Write-Host "`n== 7/10 SOAEN + doctrine =="
Invoke-DealixPy scripts/founder_soaen_daily.py --out "data/founder_briefs/soaen_$Date.md"

Write-Host "`n== 8/10 AEO + verdict =="
Invoke-DealixPy scripts/founder_revenue_day_runner.py --skip-substeps

Write-Host "`n== 9/12 Social queue expand (16w) =="
Invoke-DealixPy scripts/expand_social_queue_12w.py --cycle-weeks 28

Write-Host "`n== 10/12 Soft Launch meeting packs =="
Invoke-DealixPy scripts/prepare_soft_launch_meetings.py --top-n 10

Write-Host "`n== 11/14 Motion A pipeline (P0 close path) =="
Invoke-DealixPy scripts/founder_motion_a_pipeline.py --top-n $TopN
Invoke-DealixPy scripts/founder_all_motions_pipeline.py --top-n 5

Write-Host "`n== 12/14 First paid Diagnostic tracker =="
Invoke-DealixPy scripts/verify_first_paid_diagnostic_tracker.py

Write-Host "`n== 13/14 Content approval queue (dry-run) =="
Invoke-DealixPy scripts/queue_content_drafts_for_approval.py --dry-run

$dow = (Get-Date).DayOfWeek.value__
if ($dow -eq 5) {
    Write-Host "`n== 14/14 Weekly scorecard (Friday) =="
    Invoke-DealixPy scripts/founder_weekly_scorecard.py
} else {
    Write-Host "`n== 14/14 Weekly scorecard (skip - run Friday or: founder_weekly_scorecard.py) =="
}

Write-Host "`n== Evening (founder) =="
Write-Host "  powershell -File scripts/founder_evening.ps1"
Write-Host "  Or append: founder_evening.ps1 -Append -Company '...' -EventType message_sent_manual"

Write-Host "`n== Operating evidence (if none today) =="
Invoke-DealixPy scripts/log_founder_commercial_day_evidence.py

Write-Host "`n== 15/17 Value Plan snapshot =="
Invoke-DealixPy scripts/export_value_plan_snapshot.py

Write-Host "`n== 16/17 Full autonomous ops =="
Invoke-DealixPy scripts/run_full_commercial_ops_autopilot.py --execute

Write-Host "`n== 17/17 GTM + comprehensive =="
Invoke-DealixPy scripts/verify_gtm_stack.py
Invoke-DealixPy scripts/founder_comprehensive_plan_status.py

Write-Host "`n== Commercial value map =="
Invoke-DealixPy scripts/commercial_value_map_status.py --write-md --top-n $TopN

Write-Host "`nFOUNDER_COMMERCIAL_DAY: OK"
Write-Host "Ops UI: /ar/ops/founder | /ar/ops/war-room | /ar/ops/approvals"
Write-Host "Index: data/founder_briefs/index.json"
Write-Host "Soft launch: py -3 scripts/verify_commercial_launch_ready.py"
Write-Host "Docs: docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md"
