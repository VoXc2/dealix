# ═══════════════════════════════════════════════════════
# DEALIX WATCHDOG v3.0 — The system that never sleeps
# ═══════════════════════════════════════════════════════
param(
    [ValidateSet(1, 2, 3)]
    [int]$Gear = 1,
    [switch]$NoCreditCheck
)

$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# Load .env.local
$envFile = ".\.env.local"
if (Test-Path $envFile) {
    Get-Content $envFile -Encoding UTF8 | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)\s*=\s*(.+)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}

# Model selection
$gearNames = @{1 = "DAILY (DeepSeek)"; 2 = "POWER (Minimax M2.5)"; 3 = "ARCHITECT (Minimax M2.7)"}
$modelMap = @{1 = $env:GEAR1_MODEL; 2 = $env:GEAR2_MODEL; 3 = $env:GEAR3_MODEL}
$selectedModel = $modelMap[$Gear]
if (-not $selectedModel) { $selectedModel = "deepseek/deepseek-chat" }

# Credit check
if (-not $NoCreditCheck) {
    Write-Host "`n  Checking OpenRouter credits..." -ForegroundColor Cyan
    try {
        $pyResult = py -3 scripts/credit-guard.py 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  [WARN] Credit check failed. Continuing anyway..." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  [WARN] Credit check skipped" -ForegroundColor Yellow
    }
}

# Git check
$gitOk = $false
try { $null = git rev-parse --git-dir 2>$null; $gitOk = $true } catch {}

# Main loop
$restartCount = 0
while ($true) {
    $restartCount++
    Clear-Host
    
    Write-Host ""
    Write-Host "  ========================================" -ForegroundColor Magenta
    Write-Host "    DEALIX WATCHDOG v3.0" -ForegroundColor Magenta
    Write-Host "    Restart #$restartCount" -ForegroundColor DarkGray
    Write-Host "  ========================================" -ForegroundColor Magenta
    Write-Host "  Gear:   $($gearNames[$Gear])" -ForegroundColor Green
    Write-Host "  Model:  $selectedModel" -ForegroundColor Cyan
    Write-Host "  Git:    $(if ($gitOk) {'OK'} else {'SKIPPED (using --no-git)'})" -ForegroundColor $(if ($gitOk) {'Green'} else {'Yellow'})
    Write-Host "  ========================================" -ForegroundColor Magenta
    Write-Host "  Press Ctrl+C TWICE to stop" -ForegroundColor DarkGray
    Write-Host ""
    
    # Build arguments
    $aiderArgs = @("--model", "openrouter/$selectedModel", "--map-tokens", "1024", "--subtree-only", "--no-auto-commits")
    if (-not $gitOk) { $aiderArgs += "--no-git" }
    
    # Run Aider
    try {
        & aider @aiderArgs
        $exitCode = $LASTEXITCODE
        Write-Host "`n  Aider exited with code: $exitCode" -ForegroundColor Yellow
    } catch {
        Write-Host "`n  Aider crashed: $_" -ForegroundColor Red
    }
    
    # Auto-restart
    Write-Host "  Restarting in 3 seconds..." -ForegroundColor Yellow
    Write-Host "  (Press Ctrl+C to stop)`n" -ForegroundColor DarkGray
    Start-Sleep -Seconds 3
}
