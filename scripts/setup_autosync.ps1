# Setup git hooks path to use .githooks
git config core.hooksPath .githooks
Write-Host "Set core.hooksPath to .githooks"
# Ensure hooks are executable on Unix systems
if (Get-Command chmod -ErrorAction SilentlyContinue) {
  chmod +x .githooks/post-commit || $null
}
Write-Host "Done. Post-commit hook will run on commits and push to origin."
