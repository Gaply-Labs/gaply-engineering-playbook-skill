param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet('claude-project','claude-global','codex-project','codex-global')]
    [string]$Mode,
    [Parameter(Mandatory=$false, Position=1)]
    [string]$TargetProject = (Get-Location).Path
)

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Source = Join-Path $RepoRoot 'gaply-engineering-playbook'

if (-not (Test-Path (Join-Path $Source 'SKILL.md'))) {
    throw "Canonical skill not found at $Source"
}

switch ($Mode) {
    'claude-project' { $DestinationRoot = Join-Path $TargetProject '.claude\skills' }
    'claude-global'  { $DestinationRoot = Join-Path $HOME '.claude\skills' }
    'codex-project'  { $DestinationRoot = Join-Path $TargetProject '.agents\skills' }
    'codex-global'   { $DestinationRoot = Join-Path $HOME '.agents\skills' }
}

New-Item -ItemType Directory -Force -Path $DestinationRoot | Out-Null
$Destination = Join-Path $DestinationRoot 'gaply-engineering-playbook'
if (Test-Path $Destination) {
    Remove-Item -Recurse -Force $Destination
}
Copy-Item -Recurse -Force $Source $Destination
Write-Host "Installed: $Destination"
