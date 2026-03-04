#!/usr/bin/env pwsh

# TODO.md 任务管理脚本
# 用于自动管理TODO.md文件中的任务

param(
    [string]$Action = "help",
    [string]$TaskId,
    [string]$TaskDesc,
    [string]$Priority = "中",
    [string]$Assignee = "开发者",
    [string]$DueDate
)

$TodoFile = "./TODO.md"

# 检查TODO.md文件是否存在
if (-not (Test-Path $TodoFile)) {
    Write-Host "错误: TODO.md 文件不存在!" -ForegroundColor Red
    exit 1
}

# 读取TODO.md文件内容
$Content = Get-Content $TodoFile -Raw

function Show-Help {
    Write-Host "TODO.md 任务管理脚本"
    Write-Host "用法: .\todo-manager.ps1 -Action <action> [参数]"
    Write-Host ""
    Write-Host "可用操作:"
    Write-Host "  help              显示此帮助信息"
    Write-Host "  add               添加新任务"
    Write-Host "  start             开始任务（移至进行中）"
    Write-Host "  complete          完成任务（移至已完成）"
    Write-Host "  list              列出所有任务"
    Write-Host "  status            显示任务状态统计"
    Write-Host ""
    Write-Host "添加任务参数:"
    Write-Host "  -TaskDesc <描述>   任务描述"
    Write-Host "  -Priority <优先级> 优先级（高/中/低）"
    Write-Host "  -Assignee <负责人> 负责人"
    Write-Host "  -DueDate <日期>    截止日期（YYYY-MM-DD）"
    Write-Host ""
    Write-Host "开始/完成任务参数:"
    Write-Host "  -TaskId <ID>       任务ID（如 T001）"
    Write-Host ""
    Write-Host "示例:"
    Write-Host "  添加任务: .\todo-manager.ps1 -Action add -TaskDesc '实现CUDA内核' -Priority '高' -DueDate '2026-03-10'"
    Write-Host "  开始任务: .\todo-manager.ps1 -Action start -TaskId 'T001'"
    Write-Host "  完成任务: .\todo-manager.ps1 -Action complete -TaskId 'T001'"
    Write-Host "  列出任务: .\todo-manager.ps1 -Action list"
    Write-Host "  查看状态: .\todo-manager.ps1 -Action status"
}

function Get-NextTaskId {
    # 提取所有任务ID，找到最大的数字，然后加1
    $Ids = [regex]::Matches($Content, 'T(\d{3})') | ForEach-Object { [int]$_.Groups[1].Value }
    if ($Ids.Count -eq 0) {
        return "T001"
    }
    $MaxId = $Ids | Measure-Object -Maximum | Select-Object -ExpandProperty Maximum
    $NextId = $MaxId + 1
    return "T{0:D3}" -f $NextId
}

function Add-Task {
    if (-not $TaskDesc) {
        Write-Host "错误: 必须提供任务描述!" -ForegroundColor Red
        return
    }
    
    if (-not $DueDate) {
        $DueDate = (Get-Date).AddDays(7).ToString("yyyy-MM-dd")
        Write-Host "警告: 未提供截止日期，使用默认值: $DueDate" -ForegroundColor Yellow
    }
    
    $TaskId = Get-NextTaskId
    
    # 构建新任务行
    $NewTask = "| $TaskId | $TaskDesc | $Priority | $Assignee | $DueDate | 待办 |"
    
    # 找到待办任务列表的位置并插入新任务
    $Pattern = '(### 待办任务 \(Pending\)[\s\S]*?)(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(### 进行中任务)' 
    $Replacement = "`$1`$2`$3$NewTask`r`n`$4"
    
    $Global:Content = [regex]::Replace($Content, $Pattern, $Replacement)
    
    # 更新最近更新时间
    $Now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Global:Content = [regex]::Replace($Global:Content, '(更新时间: ).*?(\r?\n)', "`$1$Now`$2")
    $Global:Content = [regex]::Replace($Global:Content, '(更新内容: ).*?(\r?\n)', "`$1添加了新任务 $TaskId: $TaskDesc`$2")
    
    # 保存文件
    Set-Content $TodoFile $Global:Content
    Write-Host "任务已添加: $TaskId - $TaskDesc" -ForegroundColor Green
}

function Start-Task {
    if (-not $TaskId) {
        Write-Host "错误: 必须提供任务ID!" -ForegroundColor Red
        return
    }
    
    # 从待办列表中移除任务
    $TodoPattern = "(\| $TaskId \|.*?\| 待办 \|\r?\n)"
    if ([regex]::IsMatch($Content, $TodoPattern)) {
        $TaskLine = [regex]::Match($Content, $TodoPattern).Groups[1].Value
        
        # 修改状态为进行中
        $TaskLine = $TaskLine -replace "待办", "进行中"
        
        # 从待办列表中移除
        $Global:Content = [regex]::Replace($Content, $TodoPattern, "")
        
        # 插入到进行中列表
        $InProgressPattern = '(### 进行中任务 \(In Progress\)[\s\S]*?)(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(### 已完成任务)' 
        $Replacement = "`$1`$2`$3$TaskLine`$4"
        $Global:Content = [regex]::Replace($Global:Content, $InProgressPattern, $Replacement)
        
        # 更新最近更新时间
        $Now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $Global:Content = [regex]::Replace($Global:Content, '(更新时间: ).*?(\r?\n)', "`$1$Now`$2")
        $Global:Content = [regex]::Replace($Global:Content, '(更新内容: ).*?(\r?\n)', "`$1开始任务 $TaskId`$2")
        
        # 保存文件
        Set-Content $TodoFile $Global:Content
        Write-Host "任务已开始: $TaskId" -ForegroundColor Green
    } else {
        Write-Host "错误: 任务 $TaskId 不存在或不在待办列表中!" -ForegroundColor Red
    }
}

function Complete-Task {
    if (-not $TaskId) {
        Write-Host "错误: 必须提供任务ID!" -ForegroundColor Red
        return
    }
    
    # 从进行中列表中移除任务
    $InProgressPattern = "(\| $TaskId \|.*?\| 进行中 \|\r?\n)"
    if ([regex]::IsMatch($Content, $InProgressPattern)) {
        $TaskLine = [regex]::Match($Content, $InProgressPattern).Groups[1].Value
        
        # 修改状态为已完成，并将截止日期列改为完成日期
        $TaskLine = $TaskLine -replace "进行中", "已完成"
        $TaskLine = $TaskLine -replace "截止日期", "完成日期"
        
        # 更新完成日期为今天
        $Today = Get-Date -Format "yyyy-MM-dd"
        $TaskLine = [regex]::Replace($TaskLine, '(\| $TaskId \|.*?\|)(.*?)(\| 已完成 \|)', "`$1$Today`$3")
        
        # 从进行中列表中移除
        $Global:Content = [regex]::Replace($Content, $InProgressPattern, "")
        
        # 插入到已完成列表
        $CompletedPattern = '(### 已完成任务 \(Completed\)[\s\S]*?)(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(## 任务状态更新流程|$)' 
        $Replacement = "`$1`$2`$3$TaskLine`$4"
        $Global:Content = [regex]::Replace($Global:Content, $CompletedPattern, $Replacement)
        
        # 更新最近更新时间
        $Now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $Global:Content = [regex]::Replace($Global:Content, '(更新时间: ).*?(\r?\n)', "`$1$Now`$2")
        $Global:Content = [regex]::Replace($Global:Content, '(更新内容: ).*?(\r?\n)', "`$1完成任务 $TaskId`$2")
        
        # 保存文件
        Set-Content $TodoFile $Global:Content
        Write-Host "任务已完成: $TaskId" -ForegroundColor Green
    } else {
        Write-Host "错误: 任务 $TaskId 不存在或不在进行中列表中!" -ForegroundColor Red
    }
}

function List-Tasks {
    Write-Host "=== 待办任务 (Pending) ===" -ForegroundColor Cyan
    $TodoPattern = '### 待办任务 \(Pending\)[\s\S]*?(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(### 进行中任务)'
    $Match = [regex]::Match($Content, $TodoPattern)
    if ($Match.Success) {
        $Tasks = $Match.Groups[2].Value.Trim()
        if ($Tasks) {
            Write-Host $Tasks
        } else {
            Write-Host "无待办任务" -ForegroundColor Gray
        }
    }
    
    Write-Host "`n=== 进行中任务 (In Progress) ===" -ForegroundColor Yellow
    $InProgressPattern = '### 进行中任务 \(In Progress\)[\s\S]*?(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(### 已完成任务)'
    $Match = [regex]::Match($Content, $InProgressPattern)
    if ($Match.Success) {
        $Tasks = $Match.Groups[2].Value.Trim()
        if ($Tasks) {
            Write-Host $Tasks
        } else {
            Write-Host "无进行中任务" -ForegroundColor Gray
        }
    }
    
    Write-Host "`n=== 已完成任务 (Completed) ===" -ForegroundColor Green
    $CompletedPattern = '### 已完成任务 \(Completed\)[\s\S]*?(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(## |$)'
    $Match = [regex]::Match($Content, $CompletedPattern)
    if ($Match.Success) {
        $Tasks = $Match.Groups[2].Value.Trim()
        if ($Tasks) {
            Write-Host $Tasks
        } else {
            Write-Host "无已完成任务" -ForegroundColor Gray
        }
    }
}

function Show-Status {
    # 统计任务数量
    $TodoCount = [regex]::Matches($Content, '\| T\d{3} \|.*?\| 待办 \|').Count
    $InProgressCount = [regex]::Matches($Content, '\| T\d{3} \|.*?\| 进行中 \|').Count
    $CompletedCount = [regex]::Matches($Content, '\| T\d{3} \|.*?\| 已完成 \|').Count
    $TotalCount = $TodoCount + $InProgressCount + $CompletedCount
    
    $CompletionRate = 0
    if ($TotalCount -gt 0) {
        $CompletionRate = [math]::Round(($CompletedCount / $TotalCount) * 100, 2)
    }
    
    Write-Host "=== 项目状态 ===" -ForegroundColor Cyan
    Write-Host "总任务数: $TotalCount"
    Write-Host "待办任务: $TodoCount"
    Write-Host "进行中任务: $InProgressCount"
    Write-Host "已完成任务: $CompletedCount"
    Write-Host "完成率: $CompletionRate%"
    
    # 显示最近更新
    $LastUpdatePattern = '更新时间: (.*?)\r?\n更新内容: (.*?)\r?\n'
    $Match = [regex]::Match($Content, $LastUpdatePattern)
    if ($Match.Success) {
        $UpdateTime = $Match.Groups[1].Value
        $UpdateContent = $Match.Groups[2].Value
        Write-Host "`n最近更新:"
        Write-Host "时间: $UpdateTime"
        Write-Host "内容: $UpdateContent"
    }
}

# 执行指定的操作
switch ($Action) {
    "help" {
        Show-Help
    }
    "add" {
        Add-Task
    }
    "start" {
        Start-Task
    }
    "complete" {
        Complete-Task
    }
    "list" {
        List-Tasks
    }
    "status" {
        Show-Status
    }
    default {
        Write-Host "错误: 未知操作 '$Action'" -ForegroundColor Red
        Show-Help
    }
}
