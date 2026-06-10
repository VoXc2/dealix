# Dealix Gear Switcher - Quick model change
param([Parameter(Mandatory=$true)][ValidateSet(1,2,3)][int]$Gear)

$ErrorActionPreference = "Continue"
$envFile = ".\.env.local"
$gearNames = @{1 = "DAILY (DeepSeek)"; 2 = "POWER (Minimax M2.5)"; 3 = "ARCHITECT (Minimax M2.7)"}
$modelNames = @{1 = "deepseek/deepseek-chat"; 2 = "minimax/minimax-m2.5"; 3 = "minimax/minimax-m2.7"}

# Update .env.local
if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw -Encoding UTF8
    $content = $content -replace "ACTIVE_GEAR=.*", "ACTIVE_GEAR=$Gear"
    Set-Content $envFile -Value $content -Encoding UTF8 -NoNewline
}

# Update .aider.conf.yml
$aiderConf = ".\.aider.conf.yml"
if (Test-Path $aiderConf) {
    $content = Get-Content $aiderConf -Raw -Encoding UTF8
    $content = $content -replace "model:.*", "model: openrouter/$($modelNames[$Gear])"
    Set-Content $aiderConf -Value $content -Encoding UTF8 -NoNewline
}

Write-Host "`n  Switched to Gear $Gear : $($gearNames[$Gear])" -ForegroundColor Green
Write-Host "  Model: $($modelNames[$Gear])" -ForegroundColor Cyan
Write-Host "  Cost per 1M tokens:" -ForegroundColor DarkGray
$costs = @{1 = "$0.02/$0.10"; 2 = "$0.15/$1.15"; 3 = "$0.279/$1.20"}
Write-Host "  Input/Output: $($costs[$Gear])" -ForegroundColor DarkGray
Write-Host "`n  Run watchdog to start: .\scripts\watchdog.ps1 -Gear $Gear`n" -ForegroundColor Yellow
