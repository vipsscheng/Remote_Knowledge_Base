# 简单的技能复制脚本

# 设置变量
$skillName = "AI-Agent-Core-Skill"
$sourcePath = "$PSScriptRoot\.trae\skills\$skillName"
$targetIntl = "$env:USERPROFILE\.trae\skills\$skillName"
$targetCn = "$env:USERPROFILE\.trae-cn\skills\$skillName"

# 显示信息
Write-Host "Copying skill: $skillName"
Write-Host "Source: $sourcePath"
Write-Host "Target (Intl): $targetIntl"
Write-Host "Target (CN): $targetCn"

# 确保目标目录存在
New-Item -ItemType Directory -Path "$env:USERPROFILE\.trae\skills" -Force | Out-Null
New-Item -ItemType Directory -Path "$env:USERPROFILE\.trae-cn\skills" -Force | Out-Null

# 复制到国际版
if (Test-Path $sourcePath) {
    if (Test-Path $targetIntl) {
        Remove-Item -Path $targetIntl -Recurse -Force
    }
    Copy-Item -Path $sourcePath -Destination $targetIntl -Recurse -Force
    Write-Host "Copied to Trae International"
} else {
    Write-Host "Source path not found"
}

# 复制到国内版
if (Test-Path $sourcePath) {
    if (Test-Path $targetCn) {
        Remove-Item -Path $targetCn -Recurse -Force
    }
    Copy-Item -Path $sourcePath -Destination $targetCn -Recurse -Force
    Write-Host "Copied to Trae CN"
} else {
    Write-Host "Source path not found"
}

Write-Host "Done!"