#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TODO.md 任务管理脚本
用于自动管理TODO.md文件中的任务
"""

import os
import re
import sys
from datetime import datetime, timedelta

TODO_FILE = 'TODO.md'

def show_help():
    """显示帮助信息"""
    print("TODO.md 任务管理脚本")
    print("用法: python task-manager.py <action> [参数]")
    print()
    print("可用操作:")
    print("  help              显示此帮助信息")
    print("  add               添加新任务")
    print("  start             开始任务（移至进行中）")
    print("  complete          完成任务（移至已完成）")
    print("  list              列出所有任务")
    print("  status            显示任务状态统计")
    print()
    print("添加任务参数:")
    print("  task_desc         任务描述")
    print("  priority          优先级（高/中/低）")
    print("  assignee          负责人")
    print("  due_date          截止日期（YYYY-MM-DD）")
    print()
    print("开始/完成任务参数:")
    print("  task_id           任务ID（如 T001）")
    print()
    print("示例:")
    print("  添加任务: python task-manager.py add '实现CUDA内核' '高' '开发者' '2026-03-10'")
    print("  开始任务: python task-manager.py start T001")
    print("  完成任务: python task-manager.py complete T001")
    print("  列出任务: python task-manager.py list")
    print("  查看状态: python task-manager.py status")

def get_next_task_id(content):
    """生成下一个任务ID"""
    ids = re.findall(r'T(\d{3})', content)
    if not ids:
        return "T001"
    max_id = max(int(id_) for id_ in ids)
    next_id = max_id + 1
    return f"T{next_id:03d}"

def add_task(task_desc, priority="中", assignee="开发者", due_date=None):
    """添加新任务"""
    if not task_desc:
        print("错误: 必须提供任务描述!")
        return
    
    if not due_date:
        due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        print(f"警告: 未提供截止日期，使用默认值: {due_date}")
    
    # 读取文件内容
    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成任务ID
    task_id = get_next_task_id(content)
    
    # 构建新任务行
    new_task = f"| {task_id} | {task_desc} | {priority} | {assignee} | {due_date} | 待办 |\n"
    
    # 找到待办任务列表的位置并插入新任务
    pattern = r'(### 待办任务 \(Pending\)[\s\S]*?)(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(### 进行中任务)'
    replacement = r'\1\2\3' + new_task + r'\4'
    new_content = re.sub(pattern, replacement, content)
    
    # 更新最近更新时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_content = re.sub(r'(更新时间: ).*?(\r?\n)', r'\1' + now + r'\2', new_content)
    new_content = re.sub(r'(更新内容: ).*?(\r?\n)', r'\1添加了新任务 ' + task_id + r': ' + task_desc + r'\2', new_content)
    
    # 保存文件
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"任务已添加: {task_id} - {task_desc}")

def start_task(task_id):
    """开始任务"""
    if not task_id:
        print("错误: 必须提供任务ID!")
        return
    
    # 读取文件内容
    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 从待办列表中移除任务
    todo_pattern = rf'(\| {task_id} \|.*?\| 待办 \|\r?\n)'
    match = re.search(todo_pattern, content)
    if not match:
        print(f"错误: 任务 {task_id} 不存在或不在待办列表中!")
        return
    
    task_line = match.group(1)
    # 修改状态为进行中
    task_line = task_line.replace("待办", "进行中")
    
    # 从待办列表中移除
    new_content = re.sub(todo_pattern, "", content)
    
    # 插入到进行中列表
    in_progress_pattern = r'(### 进行中任务 \(In Progress\)[\s\S]*?)(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(### 已完成任务)'
    replacement = r'\1\2\3' + task_line + r'\4'
    new_content = re.sub(in_progress_pattern, replacement, new_content)
    
    # 更新最近更新时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_content = re.sub(r'(更新时间: ).*?(\r?\n)', r'\1' + now + r'\2', new_content)
    new_content = re.sub(r'(更新内容: ).*?(\r?\n)', r'\1开始任务 ' + task_id + r'\2', new_content)
    
    # 保存文件
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"任务已开始: {task_id}")

def complete_task(task_id):
    """完成任务"""
    if not task_id:
        print("错误: 必须提供任务ID!")
        return
    
    # 读取文件内容
    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 从进行中列表中移除任务
    in_progress_pattern = rf'(\| {task_id} \|.*?\| 进行中 \|\r?\n)'
    match = re.search(in_progress_pattern, content)
    if not match:
        print(f"错误: 任务 {task_id} 不存在或不在进行中列表中!")
        return
    
    task_line = match.group(1)
    # 修改状态为已完成，并将截止日期列改为完成日期
    task_line = task_line.replace("进行中", "已完成")
    task_line = task_line.replace("截止日期", "完成日期")
    
    # 更新完成日期为今天
    today = datetime.now().strftime("%Y-%m-%d")
    task_line = re.sub(rf'(\| {task_id} \|.*?\|)(.*?)(\| 已完成 \|)', r'\1' + today + r'\3', task_line)
    
    # 从进行中列表中移除
    new_content = re.sub(in_progress_pattern, "", content)
    
    # 插入到已完成列表
    completed_pattern = r'(### 已完成任务 \(Completed\)[\s\S]*?)(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(## 任务状态更新流程|$)'
    replacement = r'\1\2\3' + task_line + r'\4'
    new_content = re.sub(completed_pattern, replacement, new_content)
    
    # 更新最近更新时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_content = re.sub(r'(更新时间: ).*?(\r?\n)', r'\1' + now + r'\2', new_content)
    new_content = re.sub(r'(更新内容: ).*?(\r?\n)', r'\1完成任务 ' + task_id + r'\2', new_content)
    
    # 保存文件
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"任务已完成: {task_id}")

def list_tasks():
    """列出所有任务"""
    # 读取文件内容
    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== 待办任务 (Pending) ===")
    todo_pattern = r'### 待办任务 \(Pending\)[\s\S]*?(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(### 进行中任务)'
    match = re.search(todo_pattern, content)
    if match:
        tasks = match.group(2).strip()
        if tasks:
            print(tasks)
        else:
            print("无待办任务")
    
    print("\n=== 进行中任务 (In Progress) ===")
    in_progress_pattern = r'### 进行中任务 \(In Progress\)[\s\S]*?(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(### 已完成任务)'
    match = re.search(in_progress_pattern, content)
    if match:
        tasks = match.group(2).strip()
        if tasks:
            print(tasks)
        else:
            print("无进行中任务")
    
    print("\n=== 已完成任务 (Completed) ===")
    completed_pattern = r'### 已完成任务 \(Completed\)[\s\S]*?(\|----\|---------\|--------\|--------\|----------\|------\|\r?\n)([\s\S]*?)(## |$)'
    match = re.search(completed_pattern, content)
    if match:
        tasks = match.group(2).strip()
        if tasks:
            print(tasks)
        else:
            print("无已完成任务")

def show_status():
    """显示任务状态统计"""
    # 读取文件内容
    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计任务数量
    todo_count = len(re.findall(r'\| T\d{3} \|.*?\| 待办 \|', content))
    in_progress_count = len(re.findall(r'\| T\d{3} \|.*?\| 进行中 \|', content))
    completed_count = len(re.findall(r'\| T\d{3} \|.*?\| 已完成 \|', content))
    total_count = todo_count + in_progress_count + completed_count
    
    completion_rate = 0
    if total_count > 0:
        completion_rate = round((completed_count / total_count) * 100, 2)
    
    print("=== 项目状态 ===")
    print(f"总任务数: {total_count}")
    print(f"待办任务: {todo_count}")
    print(f"进行中任务: {in_progress_count}")
    print(f"已完成任务: {completed_count}")
    print(f"完成率: {completion_rate}%")
    
    # 显示最近更新
    last_update_pattern = r'更新时间: (.*?)\r?\n更新内容: (.*?)\r?\n'
    match = re.search(last_update_pattern, content)
    if match:
        update_time = match.group(1)
        update_content = match.group(2)
        print("\n最近更新:")
        print(f"时间: {update_time}")
        print(f"内容: {update_content}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    action = sys.argv[1]
    
    if action == "help":
        show_help()
    elif action == "add":
        if len(sys.argv) < 3:
            print("错误: 必须提供任务描述!")
            return
        task_desc = sys.argv[2]
        priority = sys.argv[3] if len(sys.argv) > 3 else "中"
        assignee = sys.argv[4] if len(sys.argv) > 4 else "开发者"
        due_date = sys.argv[5] if len(sys.argv) > 5 else None
        add_task(task_desc, priority, assignee, due_date)
    elif action == "start":
        if len(sys.argv) < 3:
            print("错误: 必须提供任务ID!")
            return
        task_id = sys.argv[2]
        start_task(task_id)
    elif action == "complete":
        if len(sys.argv) < 3:
            print("错误: 必须提供任务ID!")
            return
        task_id = sys.argv[2]
        complete_task(task_id)
    elif action == "list":
        list_tasks()
    elif action == "status":
        show_status()
    else:
        print(f"错误: 未知操作 '{action}'")
        show_help()

if __name__ == "__main__":
    main()
