# Dealix Aider Launcher — Three Gear System
param(
    [ValidateSet(1, 2, 3)]
    [int]$Gear = 1,

    [switch]$NoGit,
    [switch]$AutoCommit
)

# UTF-8 fix
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# Load env
$envPath = ".\.env.local"
if (Test-Path $envPath) {
    Get-Content $envPath | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)\s*=\s*(.+)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}

# Select model based on gear
$modelMap = @{
    1 = $env:GEAR1_MODEL
    2 = $env:GEAR2_MODEL
    3 = $env:GEAR3_MODEL
}
$selectedModel = $modelMap[$Gear]
if (-not $selectedModel) { $selectedModel = "deepseek/deepseek-chat" }

$gearNames = @{1 = "DAILY (DeepSeek)"; 2 = "POWER (Minimax M2.5)"; 3 = "ARCHITECT (Minimax M2.7)"}
Write-Host "`n⚙️  GEAR $($Gear): $($gearNames[$Gear])" -ForegroundColor Green
Write-Host "🤖 Model: $selectedModel" -ForegroundColor Cyan
Write-Host "💡 Tip: Use /switch-model in Aider to change gear`n" -ForegroundColor DarkGray

# Build args
$args = @("--model", "openrouter/$selectedModel", "--map-tokens", "1024", "--subtree-only")
if (-not $AutoCommit) { $args += "--no-auto-commits" }
if ($NoGit) { $args += "--no-git" }

# Run
& aider @args