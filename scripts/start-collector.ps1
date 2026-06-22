$ErrorActionPreference = "Stop"

Write-Host "Starting RAGLens collector..."
Write-Host "Expected URL: http://localhost:4319"
Write-Host ""

$repoRoot = Split-Path -Parent $PSScriptRoot
$collectorDir = Join-Path $repoRoot "collector\go"

if (-not (Test-Path $collectorDir)) {
	Write-Error "Collector directory not found: $collectorDir"
}

Set-Location $collectorDir

go run ./cmd/raglens-collector