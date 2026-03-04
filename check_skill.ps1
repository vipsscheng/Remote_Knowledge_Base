Write-Host "Checking skill status..." -ForegroundColor Green
Write-Host "=" * 60

# 检查用户技能目录
$userSkillDir = "C:\Users\Administrator\.trae\skills\AI-Agent-Core-Skill"
Write-Host "User skill directory: $userSkillDir"
if (Test-Path $userSkillDir) {
    Write-Host "✓ Skill directory exists" -ForegroundColor Green
} else {
    Write-Host "✗ Skill directory not found" -ForegroundColor Red
}

# 检查技能配置文件
$skillJson = Join-Path $userSkillDir "skill.json"
Write-Host "`nChecking skill.json:" 
if (Test-Path $skillJson) {
    Write-Host "✓ skill.json exists" -ForegroundColor Green
    try {
        $config = Get-Content $skillJson | ConvertFrom-Json
        Write-Host "  Skill name: $($config.name)"
        Write-Host "  Version: $($config.version)"
        Write-Host "  Description: $($config.description)"
    } catch {
        Write-Host "✗ Invalid skill.json format" -ForegroundColor Red
    }
} else {
    Write-Host "✗ skill.json not found" -ForegroundColor Red
}

# 检查SKILL.md文件
$skillMd = Join-Path $userSkillDir "SKILL.md"
Write-Host "`nChecking SKILL.md:" 
if (Test-Path $skillMd) {
    Write-Host "✓ SKILL.md exists" -ForegroundColor Green
} else {
    Write-Host "✗ SKILL.md not found" -ForegroundColor Red
}

# 检查核心文件
Write-Host "`nChecking core files:" 
$coreFiles = @('start_skill.bat', 'md_installer.py')
foreach ($file in $coreFiles) {
    $filePath = Join-Path $userSkillDir $file
    if (Test-Path $filePath) {
        Write-Host "✓ $file exists" -ForegroundColor Green
    } else {
        Write-Host "✗ $file not found" -ForegroundColor Red
    }
}

# 检查依赖目录
Write-Host "`nChecking dependency directories:" 
$dirs = @('automation', 'knowledge_base')
foreach ($dir in $dirs) {
    $dirPath = Join-Path $userSkillDir $dir
    if (Test-Path $dirPath) {
        Write-Host "✓ $dir directory exists" -ForegroundColor Green
    } else {
        Write-Host "✗ $dir directory not found" -ForegroundColor Red
    }
}

Write-Host "`n" + "=" * 60
Write-Host "Skill check completed." -ForegroundColor Green
Write-Host "`nTo make the skill available in Trae IDE:" -ForegroundColor Yellow
Write-Host "1. Restart Trae IDE to refresh the skill list"
Write-Host "2. Check if the skill appears in the skill management interface"
Write-Host "3. If not, try manually adding the skill directory in Trae IDE settings"
