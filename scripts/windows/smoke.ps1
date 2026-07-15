$ErrorActionPreference = "Stop"

Write-Host "SledTrace smoke test"
Write-Host "Collector: http://localhost:4319"
Write-Host ""

$env:SLEDTRACE_COLLECTOR_URL = "http://localhost:4319"

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$sdkPythonDir = Join-Path $repoRoot "sdk/python"

Set-Location $sdkPythonDir

Write-Host "Step 1/2: Running warning rules demo..."
python -m examples.warning_rules_demo all

Write-Host ""
Write-Host "Step 2/2: Running local RAG trace demo..."
python -m examples.local_rag_demo.run_demo trace-all

Write-Host ""
Write-Host "Smoke test completed."
Write-Host "Now verify traces and warning cards in the dashboard."