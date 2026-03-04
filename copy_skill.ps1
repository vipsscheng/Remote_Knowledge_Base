# 测试技能复制脚本
# 用于手动复制技能到Trae国际版和国内版目录

$skillName = 'AI-Agent-Core-Skill'
$skillSource = Join-Path -Path $PSScriptRoot -ChildPath '.trae' -AdditionalChildPath 'skills', $skillName

# Trae国际版目录
$traeDir = Join-Path -Path $env:USERPROFILE -ChildPath '.trae'
$skillsDir = Join-Path -Path $traeDir -ChildPath 'skills'
$skillTargetIntl = Join-Path -Path $skillsDir -ChildPath $skillName

# Trae国内版目录
$traeCnDir = Join-Path -Path $env:USERPROFILE -ChildPath '.trae-cn'
$skillsCnDir = Join-Path -Path $traeCnDir -ChildPath 'skills'
$skillTargetCn = Join-Path -Path $skillsCnDir -ChildPath $skillName

Write-Host "Testing skill copy functionality..."
Write-Host "Skill source: $skillSource"
Write-Host "Skill source exists: $(Test-Path $skillSource)"

# 确保目标目录存在
Write-Host "\nEnsuring target directories exist..."
foreach ($directory in @($skillsDir, $skillsCnDir)) {
    if (-not (Test-Path $directory)) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
        Write-Host "Created directory: $directory"
    } else {
        Write-Host "Directory already exists: $directory"
    }
}

# 复制技能到国际版
if (Test-Path $skillSource) {
    if (Test-Path $skillTargetIntl) {
        Remove-Item -Path $skillTargetIntl -Recurse -Force
    }
    Copy-Item -Path $skillSource -Destination $skillTargetIntl -Recurse -Force
    Write-Host "\nCopied skill to Trae International: $skillTargetIntl"
} else {
    Write-Host "\nSkill source not found!"
}

# 复制技能到国内版
if (Test-Path $skillSource) {
    if (Test-Path $skillTargetCn) {
        Remove-Item -Path $skillTargetCn -Recurse -Force
    }
    Copy-Item -Path $skillSource -Destination $skillTargetCn -Recurse -Force
    Write-Host "\nCopied skill to Trae CN: $skillTargetCn"
} else {
    Write-Host "\nSkill source not found!"
}

Write-Host "\nTest completed!"