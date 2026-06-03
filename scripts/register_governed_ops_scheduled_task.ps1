# Register Windows Task Scheduler jobs for governed ops (local machine).
# Requires: run as user with permission to create tasks.
# Usage: powershell -ExecutionPolicy Bypass -File scripts/register_governed_ops_scheduled_task.ps1

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Morning = Join-Path $Root "scripts\run_founder_full_autopilot.ps1"
$Evening = Join-Path $Root "scripts\founder_evening.ps1"

$MorningAction = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Morning`" -Mode morning"
$EveningAction = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Evening`""

# 08:00 Asia/Riyadh ≈ 05:00 UTC — adjust if machine TZ is not KSA
$MorningTrigger = New-ScheduledTaskTrigger -Daily -At "08:00"
$EveningTrigger = New-ScheduledTaskTrigger -Daily -At "18:00"

Register-ScheduledTask -TaskName "Dealix-Governed-Ops-Morning" `
    -Action $MorningAction -Trigger $MorningTrigger `
    -Description "Dealix governed morning: expand + founder day (draft-only)" -Force

Register-ScheduledTask -TaskName "Dealix-Governed-Ops-Evening" `
    -Action $EveningAction -Trigger $EveningTrigger `
    -Description "Dealix evening evidence reminder" -Force

Write-Host "REGISTERED: Dealix-Governed-Ops-Morning (08:00 daily)"
Write-Host "REGISTERED: Dealix-Governed-Ops-Evening (18:00 daily)"
Write-Host "Repo: $Root"
