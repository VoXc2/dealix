# Start Dealix local dev stack (Windows) — Postgres via Docker when available.
# Usage: powershell -File scripts/start_local_dev_stack.ps1
#        powershell -File scripts/start_local_dev_stack.ps1 -SkipFrontend

param(
    [switch]$SkipFrontend,
    [switch]$SkipDocker
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Find-Docker {
    $candidates = @(
        "docker",
        "${env:ProgramFiles}\Docker\Docker\resources\bin\docker.exe"
    )
    foreach ($c in $candidates) {
        if (Get-Command $c -ErrorAction SilentlyContinue) { return $c }
        if (Test-Path $c) { return $c }
    }
    return $null
}

if (-not (Test-Path (Join-Path $Root ".env"))) {
    Copy-Item (Join-Path $Root ".env.example") (Join-Path $Root ".env")
    Write-Host "Created .env from .env.example"
}

$docker = $null
if (-not $SkipDocker) {
    $docker = Find-Docker
    if ($docker) {
        Write-Host "== Docker: postgres, pgbouncer, redis, mongo =="
        & $docker compose up -d postgres pgbouncer redis mongo
    } else {
        Write-Host "WARN: Docker not found. Install Docker Desktop, then re-run."
        Write-Host "      API will start but DB calls fail until Postgres is up."
    }
}

$apiRunning = $false
try {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1:8000/docs" -UseBasicParsing -TimeoutSec 2
    if ($r.StatusCode -eq 200) { $apiRunning = $true }
} catch { }

if (-not $apiRunning) {
    Write-Host "== Starting API on :8000 (py -3) =="
    $apiCmd = @(
        "Set-Location '$Root'",
        '$env:APP_ENV="development"',
        '$env:ENVIRONMENT="development"',
        'py -3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload'
    ) -join "; "
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $apiCmd | Out-Null
    Start-Sleep -Seconds 3
}

if (-not $SkipFrontend) {
    $feRunning = $false
    try {
        Invoke-WebRequest -Uri "http://127.0.0.1:3000" -UseBasicParsing -TimeoutSec 3 | Out-Null
        $feRunning = $true
    } catch { }

    if (-not $feRunning) {
        Write-Host "== Starting frontend on :3000 =="
        $feCmd = "Set-Location '$Root\frontend'; npm run dev"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $feCmd | Out-Null
    }
}

Write-Host ""
Write-Host "URLs:"
Write-Host "  API docs:  http://localhost:8000/docs"
Write-Host "  Founder:   http://localhost:3000/ar/ops/founder"
Write-Host "  GTM home:  http://localhost:3000/ar"
Write-Host ""
Write-Host "Morning sell motion: powershell -File scripts/founder_morning.ps1"
