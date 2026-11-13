# Oh My Anti - 1-Click Global Installer for Windows
[CmdletBinding()]
param(
    [string]$GeminiConfigPath = "$HOME\.gemini\config",
    [string]$CliConfigPath = "$HOME\.gemini\antigravity-cli"
)

$ErrorActionPreference = "Stop"
Write-Host "Installing Oh My Anti to $GeminiConfigPath and $CliConfigPath..." -ForegroundColor Cyan

$pluginsDir = Join-Path $GeminiConfigPath "plugins\oh-my-anti"
$skillsDir = Join-Path $GeminiConfigPath "skills"
$rulesDir = Join-Path $GeminiConfigPath "rules"

New-Item -ItemType Directory -Force $pluginsDir | Out-Null
New-Item -ItemType Directory -Force $skillsDir | Out-Null
New-Item -ItemType Directory -Force $rulesDir | Out-Null
New-Item -ItemType Directory -Force $CliConfigPath | Out-Null

$scriptRoot = $PSScriptRoot

# 1. Copy plugin definition and resources
Copy-Item -Path (Join-Path $scriptRoot "plugin.json") -Destination $pluginsDir -Force
Copy-Item -Path (Join-Path $scriptRoot "agents") -Destination $pluginsDir -Recurse -Force
Copy-Item -Path (Join-Path $scriptRoot "resources") -Destination $pluginsDir -Recurse -Force
Copy-Item -Path (Join-Path $scriptRoot "templates") -Destination $pluginsDir -Recurse -Force
Copy-Item -Path (Join-Path $scriptRoot "scripts") -Destination $pluginsDir -Recurse -Force
Copy-Item -Path (Join-Path $scriptRoot "skills") -Destination $pluginsDir -Recurse -Force

# 2. Link or copy skills globally
$skills = Get-ChildItem -Path (Join-Path $scriptRoot "skills") -Directory
foreach ($s in $skills) {
    $targetSkill = Join-Path $skillsDir $s.Name
    if (Test-Path $targetSkill) { Remove-Item -Recurse -Force $targetSkill }
    Copy-Item -Path $s.FullName -Destination $targetSkill -Recurse -Force
    Write-Host "  -> Installed skill: $($s.Name)" -ForegroundColor Green
}

# 3. Copy global rules
Copy-Item -Path (Join-Path $scriptRoot "rules\AGENTS.md") -Destination (Join-Path $rulesDir "AGENTS.md") -Force
Write-Host "  -> Installed global intent rules: AGENTS.md" -ForegroundColor Green

# 4. Configure CLI Settings & Statusline (OMP parity)
Copy-Item -Path (Join-Path $scriptRoot "statusline.py") -Destination $CliConfigPath -Force
Copy-Item -Path (Join-Path $scriptRoot "statusline.bat") -Destination $CliConfigPath -Force
Copy-Item -Path (Join-Path $scriptRoot "statusline.sh") -Destination $CliConfigPath -Force
Copy-Item -Path (Join-Path $scriptRoot "settings.json") -Destination $CliConfigPath -Force
Write-Host "  -> Configured high verbosity & OMP-style statusline in settings.json" -ForegroundColor Green

Write-Host "Oh My Anti successfully installed! All skills, subagents, and OMP-style UI are ready." -ForegroundColor Green
